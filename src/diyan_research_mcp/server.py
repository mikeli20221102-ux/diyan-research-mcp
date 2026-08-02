"""企业研究证据链 MCP 的入口。

启动：
    python -m diyan_research_mcp.server

本进程是无状态转发壳：不落盘研究数据、不写审计日志、不保存租户状态，三者
都由研究数据服务负责。传输方式通过 DIYAN_TRANSPORT 指定，托管环境一般用
sse，本地调试可用 stdio。
"""
from __future__ import annotations

import os

from mcp.server.fastmcp import FastMCP

from .backend import BackendError, call
from .config import ConfigError
from .policy import PolicyError, require_safe_query, safe_research_output

FRAMEWORKS = ("enterprise", "business", "finance", "people", "brand")
MIN_EXCERPT_CHARS = 200
MAX_EXCERPT_CHARS = 8_000
SUPPORTED_TRANSPORTS = ("stdio", "sse", "streamable-http")

mcp = FastMCP(
    "diyan-research-mcp",
    instructions=(
        "这是企业研究证据链服务，只服务于授权企业的内部投研、战略和产业研究人员。"
        "只提供研究框架、冻结快照与历史因子摘要，不提供实时行情、交易、仓位或收益承诺。"
        "输出必须保留来源、数据截至日与证伪条件。"
    ),
)


class ToolError(RuntimeError):
    """入参未通过本地校验。"""


def _fail(exc: Exception) -> dict[str, str]:
    if isinstance(exc, PolicyError):
        error_type = "policy"
    elif isinstance(exc, ConfigError):
        error_type = "config"
    elif isinstance(exc, BackendError):
        error_type = "backend"
    else:
        error_type = "request"
    return {"error": str(exc), "error_type": error_type}


def _envelope(payload: dict) -> dict:
    return safe_research_output(
        payload.get("result", {}),
        source=payload.get("source", "diyan-research-backend"),
        as_of=payload.get("as_of"),
        usage=payload.get("usage"),
    )


@mcp.tool()
def framework_excerpt(framework: str, query: str = "", max_chars: int = 4000) -> dict:
    """读取经过批准的研究框架片段。framework 为 enterprise/business/finance/people/brand。"""
    try:
        if framework not in FRAMEWORKS:
            raise ToolError(f"不支持的框架：{framework}。可选：{'、'.join(FRAMEWORKS)}。")
        if not MIN_EXCERPT_CHARS <= max_chars <= MAX_EXCERPT_CHARS:
            raise ToolError(f"max_chars 必须介于 {MIN_EXCERPT_CHARS} 和 {MAX_EXCERPT_CHARS}。")
        payload = call(
            "GET",
            f"/frameworks/{framework}",
            params={"query": query.strip(), "max_chars": max_chars},
        )
        return _envelope(payload)
    except (ToolError, ConfigError, BackendError) as exc:
        return _fail(exc)


@mcp.tool()
def stock_snapshot_latest() -> dict:
    """读取最新冻结的股票研究快照，不代表实时市场状态。"""
    try:
        return _envelope(call("GET", "/snapshots/stock/latest"))
    except (ConfigError, BackendError) as exc:
        return _fail(exc)


@mcp.tool()
def hypothesis_get(hypothesis_id: str) -> dict:
    """读取通过交付证据门槛的冻结假设；不返回未验证假设。"""
    try:
        identifier = hypothesis_id.strip()
        if not identifier.startswith("stock-") or "/" in identifier or "\\" in identifier:
            raise ToolError("hypothesis_id 格式不正确。")
        return _envelope(call("GET", f"/hypotheses/{identifier}"))
    except (ToolError, ConfigError, BackendError) as exc:
        return _fail(exc)


@mcp.tool()
def cognition_radar_read() -> dict:
    """读取历史主题研究雷达摘要，并标注其非实时性。"""
    try:
        return _envelope(call("GET", "/radar/cognition/latest"))
    except (ConfigError, BackendError) as exc:
        return _fail(exc)


@mcp.tool()
def ic_backtest_summary() -> dict:
    """读取冻结的因子历史 IC 摘要；不提供原始行情或面板。"""
    try:
        return _envelope(call("GET", "/factors/ic-summary"))
    except (ConfigError, BackendError) as exc:
        return _fail(exc)


@mcp.tool()
def research_analyze_safe(symbol: str, question: str, market: str = "A") -> dict:
    """调用受控研究接口，删除交易字段并附加研究辅助边界。"""
    try:
        safe_question = require_safe_query(question)
        code = symbol.strip()
        if not code:
            raise ToolError("必须提供研究标的。")
        payload = call(
            "POST",
            "/research/analyze",
            json_body={
                "symbol": code,
                "market": market.strip().upper(),
                "question": safe_question,
            },
        )
        return _envelope(payload)
    except (ToolError, PolicyError, ConfigError, BackendError) as exc:
        return _fail(exc)


def _transport() -> str:
    transport = os.getenv("DIYAN_TRANSPORT", "sse").strip().lower()
    if transport not in SUPPORTED_TRANSPORTS:
        raise SystemExit(
            f"DIYAN_TRANSPORT 只能是 {'、'.join(SUPPORTED_TRANSPORTS)} 之一，当前为 {transport}。"
        )
    return transport


if __name__ == "__main__":
    mcp.run(transport=_transport())
