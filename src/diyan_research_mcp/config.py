"""运行期配置。

所有取值都在调用时读取，而不是导入时读取：广场可能在使用者填写凭据之前就
拉起进程，一个启动即崩溃的服务在详情页上看起来就是坏的。
"""
from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_BACKEND_URL = "https://api.diyan.example/v1"
DEFAULT_TIMEOUT_SECONDS = 30.0
MAX_TIMEOUT_SECONDS = 120.0


class ConfigError(RuntimeError):
    """凭据缺失导致本次调用无法进行。"""


@dataclass(frozen=True)
class BackendConfig:
    base_url: str
    api_key: str
    timeout: float


def load_backend_config() -> BackendConfig:
    api_key = os.getenv("DIYAN_API_KEY", "").strip()
    if not api_key:
        raise ConfigError(
            "未配置访问凭据。请在 MCP 详情页填写 DIYAN_API_KEY 后重新连接 Server。"
        )
    base_url = os.getenv("DIYAN_BACKEND_URL", DEFAULT_BACKEND_URL).strip().rstrip("/")
    if not base_url.startswith("https://"):
        raise ConfigError("研究数据服务地址必须使用 HTTPS。")
    return BackendConfig(base_url=base_url, api_key=api_key, timeout=_timeout())


def _timeout() -> float:
    raw = os.getenv("DIYAN_TIMEOUT_SECONDS", "").strip()
    if not raw:
        return DEFAULT_TIMEOUT_SECONDS
    try:
        value = float(raw)
    except ValueError:
        return DEFAULT_TIMEOUT_SECONDS
    if not 1.0 <= value <= MAX_TIMEOUT_SECONDS:
        return DEFAULT_TIMEOUT_SECONDS
    return value
