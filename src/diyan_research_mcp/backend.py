"""研究数据服务的 HTTP 客户端。

壳内不保存任何研究数据。租户身份、档位和配额一律由后端裁定，壳只转发凭据
并把后端的判定原样呈现。
"""
from __future__ import annotations

from typing import Any

import httpx

from . import __version__
from .config import load_backend_config

STATUS_MESSAGES = {
    401: "访问凭据无效或已过期，请在 MCP 详情页更新后重新连接。",
    403: "当前档位不包含该工具。免费档开放研究框架与部分冻结快照，其余需要付费租户凭据。",
    404: "未找到该资源，或它未通过交付证据门槛。",
    413: "请求体超出服务端限制。",
    429: "本周期调用配额已用尽，配额重置时间见 usage 字段。",
}


class BackendError(RuntimeError):
    """面向调用方的失败信息，不泄露内部配置。"""


def raise_for_status(status_code: int) -> None:
    if status_code < 400:
        return
    raise BackendError(
        STATUS_MESSAGES.get(status_code, f"研究数据服务返回错误：{status_code}")
    )


def call(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = load_backend_config()
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Accept": "application/json",
        "User-Agent": f"diyan-research-mcp/{__version__}",
    }
    try:
        response = httpx.request(
            method,
            f"{config.base_url}/{path.lstrip('/')}",
            params=params,
            json=json_body,
            headers=headers,
            timeout=config.timeout,
        )
    except httpx.TimeoutException as exc:
        raise BackendError("研究数据服务响应超时。") from exc
    except httpx.HTTPError as exc:
        raise BackendError("研究数据服务当前不可用。") from exc

    raise_for_status(response.status_code)
    try:
        payload = response.json()
    except ValueError as exc:
        raise BackendError("研究数据服务返回了无法解析的响应。") from exc
    if not isinstance(payload, dict):
        raise BackendError("研究数据服务返回了非预期的响应结构。")
    return payload
