# 研究数据服务契约

转发壳对服务端的全部要求。服务端是租户身份、档位、配额与审计的唯一裁定方。

## 鉴权

每个请求携带 `Authorization: Bearer <DIYAN_API_KEY>`。壳不解析这个凭据，也不从中推断任何身份；服务端负责把它映射到租户与档位。

## 端点

| 方法 | 路径 | 入参 |
|---|---|---|
| GET | `/frameworks/{framework}` | query string：`query`、`max_chars` |
| GET | `/snapshots/stock/latest` | 无 |
| GET | `/hypotheses/{hypothesis_id}` | 路径参数 |
| GET | `/radar/cognition/latest` | 无 |
| GET | `/factors/ic-summary` | 无 |
| POST | `/research/analyze` | JSON：`symbol`、`market`、`question` |

`framework` 取值限于 `enterprise`、`business`、`finance`、`people`、`brand`，壳已在本地校验。`hypothesis_id` 形如 `stock-001`，壳已挡掉路径穿越字符。

## 成功响应

```json
{
  "result": {},
  "source": "registry/snapshots/stock-2026-07-31.json",
  "as_of": "2026-07-31",
  "usage": { "tier": "pro", "used": 128, "limit": 5000, "resets_at": "2026-09-01T00:00:00Z" }
}
```

`result` 之外的三个字段都可省略：缺 `source` 时壳回落到 `diyan-research-backend`，缺 `as_of` 时回落到当前时间，缺 `usage` 时响应里不出现 `usage` 段。

服务端不得在 `result` 里放置买卖、仓位、股数一类字段。壳会剥掉它们，但那是兜底，不是许可。

## 错误状态

| 状态码 | 壳呈现给使用者的含义 |
|---|---|
| 401 | 凭据无效或过期 |
| 403 | 当前档位不含该工具 |
| 404 | 资源不存在，或未过交付证据门槛 |
| 413 | 请求体超限 |
| 429 | 本周期配额用尽 |

其余 4xx/5xx 统一呈现为「研究数据服务返回错误：<状态码>」。响应体里的内部信息不会透出给使用者。

## 分档

档位由凭据决定，壳不参与。建议免费档只开 `framework_excerpt` 与 `stock_snapshot_latest`，其余返回 403 并在响应体里说明升级路径。

## 审计

调用审计在服务端记录，壳不落盘。日志只记哈希与元数据，不记客户原文。
