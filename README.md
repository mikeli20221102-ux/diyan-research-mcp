# diyan-research-mcp · 企业研究证据链

面向企业投研与产业研究团队的只读研究 MCP，提供研究框架、冻结快照与历史因子摘要，每条结论附来源、数据截至日与证伪条件，不输出交易建议。

## 这个仓库里没有数据

本仓库只包含转发壳，职责是三件事：校验入参、携带租户凭据调用研究数据服务、在返回前剥掉交易类字段。研究框架、冻结快照、假设台账和因子摘要都存放在服务端，不随代码分发。

```
AI 客户端  ──MCP──▶  diyan-research-mcp（本仓库）  ──HTTPS──▶  研究数据服务
                     入参校验 / 凭据转发 / 输出过滤        数据、租户、档位、配额、审计
```

这样分层有三个后果，都是有意为之：

- 壳可以公开审阅，因为它不含任何专有数据，也不含任何密钥。
- 租户身份、档位和配额一律由服务端裁定，壳不做信任判断，也就无法被绕过。
- 输出过滤留在壳内而不是只放在服务端，即便服务端出错或被篡改，交易类表述也无法离开进程。

## 工具

| 工具 | 说明 |
|---|---|
| `framework_excerpt` | 读取研究框架片段，可选 enterprise / business / finance / people / brand |
| `stock_snapshot_latest` | 读取最新冻结的股票研究快照 |
| `hypothesis_get` | 读取通过交付证据门槛的冻结假设 |
| `cognition_radar_read` | 读取历史主题研究雷达摘要 |
| `ic_backtest_summary` | 读取冻结的因子历史 IC 摘要 |
| `research_analyze_safe` | 调用受控研究接口做单标的研判 |

工具是否可用取决于凭据对应的档位。免费档开放研究框架与部分冻结快照，其余返回 `error_type: backend` 并说明需要付费租户凭据。

## 配置

唯一必填项是 `DIYAN_API_KEY`，在 MCP 详情页填写即可。其余变量见 `.env.example`，只在自建部署或联调时需要。

凭据缺失时进程仍会正常启动，但每次工具调用都会返回明确的配置错误。这是刻意的：托管环境可能在使用者填写凭据之前就拉起进程，启动即崩溃会让详情页上的服务看起来是坏的。

## 本地运行

```bash
python -m pip install -r requirements.txt
export PYTHONPATH=src
export DIYAN_API_KEY=<你的租户凭据>
export DIYAN_TRANSPORT=stdio
python -m diyan_research_mcp.server
```

测试不需要网络和凭据：

```bash
python -m unittest discover -s tests -v
```

## 边界

- 只读。没有任何写入、下单、部署或数据导出能力。
- 不返回实时行情。快照与摘要都是冻结产物，每条结果都带 `as_of`。
- 不生成买卖、仓位、股数、跟单或收益承诺。含此类表述的提问在发出请求前就会被拒绝。
- 不读取使用者的本地文件、本地数据库或非必要环境变量。

## 服务端契约

如需自建后端，接口定义见 [`docs/BACKEND_CONTRACT.md`](docs/BACKEND_CONTRACT.md)。

## 许可与归属

由深圳瞳桦文化传媒有限公司开发与维护。MIT 许可，见 [`LICENSE`](LICENSE)。
