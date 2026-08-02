"""输出边界控制。

这一层留在壳内而不是只放在后端，是为了让交易类表述即使在后端出错或被篡改
的情况下也无法离开进程。
"""
from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

RESEARCH_DISCLAIMER = "研究辅助，仅限客户内部使用；不构成投资建议、交易指令或收益承诺。"

FORBIDDEN_OUTPUT_KEYS = {
    "action",
    "actions",
    "final_action",
    "final_shares",
    "shares",
    "position",
    "position_size",
    "buy",
    "sell",
    "trade",
    "order",
    "follow",
    "qmt",
    "paper_trade",
}

FORBIDDEN_TERMS = (
    "买入",
    "卖出",
    "加仓",
    "减仓",
    "清仓",
    "建仓",
    "重仓",
    "持仓",
    "跟单",
    "下单",
    "股数",
    "保本",
    "收益承诺",
    "强烈信号",
    "简单决策窗口",
)

MAX_QUERY_CHARS = 2_000


class PolicyError(ValueError):
    """请求试图越过只做研究的边界。"""


def require_safe_query(text: str) -> str:
    query = text.strip()
    if not query:
        raise PolicyError("必须提供研究问题。")
    if len(query) > MAX_QUERY_CHARS:
        raise PolicyError(f"研究问题不能超过 {MAX_QUERY_CHARS} 个字符。")
    if any(term in query for term in FORBIDDEN_TERMS):
        raise PolicyError("该请求包含交易或收益承诺表述，企业研究 MCP 不处理此类请求。")
    return query


def _sanitize(value: Any) -> Any:
    if isinstance(value, Mapping):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            if str(key).lower() in FORBIDDEN_OUTPUT_KEYS:
                continue
            cleaned[str(key)] = _sanitize(item)
        return cleaned
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    if isinstance(value, str):
        sanitized = value
        for term in FORBIDDEN_TERMS:
            sanitized = sanitized.replace(term, "[已移除]")
        return sanitized
    return value


def safe_research_output(
    payload: Mapping[str, Any],
    *,
    source: str,
    as_of: str | None = None,
    usage: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """剥掉交易字段，附上不可绕过的研究边界。"""
    envelope: dict[str, Any] = {
        "research_boundary": {
            "disclaimer": RESEARCH_DISCLAIMER,
            "source": source,
            "as_of": as_of or datetime.now(UTC).isoformat(),
            "transaction_fields_removed": True,
        },
        "result": _sanitize(payload),
    }
    if usage is not None:
        envelope["usage"] = dict(usage)
    return envelope
