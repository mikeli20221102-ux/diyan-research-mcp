# diyan-research-mcp · 分发提交清单

## 已完成（自动）

| 渠道 | 状态 | 链接 |
|---|---|---|
| GitHub 仓库 | 公开 | https://github.com/mikeli20221102-ux/diyan-research-mcp |
| PyPI | 0.1.1 | https://pypi.org/project/diyan-research-mcp/ |
| Official MCP Registry | active | https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.mikeli20221102-ux/diyan-research-mcp |
| punkpeye/awesome-mcp-servers | PR 开着 | https://github.com/punkpeye/awesome-mcp-servers/pull/11409 |
| docker/mcp-registry | PR 开着 | https://github.com/docker/mcp-registry/pull/4607 |
| appcypher/awesome-mcp-servers | PR 开着 | （见下方创建后链接） |

## 等同步，不用交

- **Glama**：会扫公开 GitHub，通常几天内出现
- **PulseMCP**：从官方 Registry 日/周同步；可发邮件催：`hello@pulsemcp.com`

## 需要你网页提交（复制粘贴即可）

### 1) mcp.so
打开：https://mcp.so/submit

- Repository URL: `https://github.com/mikeli20221102-ux/diyan-research-mcp`
- Name: `diyan-research-mcp` / `企业研究证据链`
- Description: `面向企业投研与产业研究团队的只读研究 MCP，提供研究框架、冻结快照与历史因子摘要，每条结论附来源、数据截至日与证伪条件，不输出交易建议。`
- Tags: `research`, `finance`, `enterprise`, `evidence`, `python`
- Category: Search / Finance / Research（选最接近的）
- Install: `uvx diyan-research-mcp`
- Env: `DIYAN_API_KEY`（required）

### 2) Cursor Directory
打开：https://cursor.directory/mcp/new （GitHub 登录）

- Name: `Diyan Research Evidence Chain`
- Description: `Read-only enterprise research MCP: frameworks, frozen snapshots, sourced results. No trading advice.`
- Link to install instructions: `https://github.com/mikeli20221102-ux/diyan-research-mcp`
- Logo: 桌面 `diyan-logo.png`
- Company: 深圳瞳桦文化传媒有限公司（若有选项）

### 3) mcpservers.org
打开：https://mcpservers.org/submit

- GitHub: `https://github.com/mikeli20221102-ux/diyan-research-mcp`
- 同上英文简介

### 4) PulseMCP 催同步（可选）
发邮件到 `hello@pulsemcp.com`：

```
Subject: Please index diyan-research-mcp from Official MCP Registry

Hello,

We published to the Official MCP Registry:
- Name: io.github.mikeli20221102-ux/diyan-research-mcp
- Version: 0.1.1
- Repo: https://github.com/mikeli20221102-ux/diyan-research-mcp
- PyPI: https://pypi.org/project/diyan-research-mcp/

Could you please index it on PulseMCP when convenient?

Thanks,
深圳瞳桦文化传媒有限公司 / Li Shichao
```

### 5) Smithery（后端起来后再交）
打开：https://smithery.ai/new

当前形态是 stdio + 自有后端，没有公网 HTTPS MCP 端点时先别交。
后端上线后填：
- Server URL: `https://<your-host>/mcp`
- Name: `@tonghua/diyan-research-mcp`（或你的 org）
- Config schema 里要 `DIYAN_API_KEY`

### 6) 国内托管类（企业账号）
- 腾讯云 MCP 广场：入驻表（你正在填）https://wj.qq.com/s2/23327353/7684/
- 阿里云百炼 MCP：控制台自定义服务
- 百度 MCP World / 魔搭：各自控制台

## Q08 配置（腾讯广场）

```json
{
  "mcpServers": {
    "diyan-research-mcp": {
      "command": "uvx",
      "args": ["diyan-research-mcp"],
      "env": {
        "DIYAN_API_KEY": "",
        "DIYAN_TRANSPORT": "stdio"
      }
    }
  }
}
```
