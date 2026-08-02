# diyan-research-mcp · Enterprise Research Evidence Chain

A read-only research MCP for enterprise investment and industry research teams. It serves research frameworks, frozen snapshots and historical factor summaries. Every result carries its source, its as-of date and its falsification conditions. It never produces trading advice.

## This repository contains no data

This repository is only the forwarding shell. It does three things: validate arguments, call the research data service with the tenant credential, and strip transaction fields before returning. The research frameworks, frozen snapshots, hypothesis ledger and factor summaries live on the server side and are not distributed with the code.

```
AI client  ──MCP──▶  diyan-research-mcp (this repo)  ──HTTPS──▶  research data service
                     validation / credential relay / output filter    data, tenancy, tier, quota, audit
```

Three consequences of this split, all intentional:

- The shell can be reviewed publicly, because it holds no proprietary data and no secrets.
- Tenant identity, tier and quota are decided by the server. The shell makes no trust decisions, so none can be bypassed.
- Output filtering stays in the shell rather than only on the server, so trading language cannot leave the process even if the backend misbehaves.

## Tools

| Tool | Purpose |
|---|---|
| `framework_excerpt` | Read a research framework excerpt: enterprise / business / finance / people / brand |
| `stock_snapshot_latest` | Read the latest frozen equity research snapshot |
| `hypothesis_get` | Read a frozen hypothesis that passed the delivery evidence threshold |
| `cognition_radar_read` | Read the historical thematic research radar summary |
| `ic_backtest_summary` | Read the frozen factor IC history summary |
| `research_analyze_safe` | Run a single-name enquiry through the controlled research endpoint |

Tool availability depends on the tier attached to your credential. The free tier exposes research frameworks and part of the frozen snapshots; the rest returns `error_type: backend` with an explanation.

## Configuration

`DIYAN_API_KEY` is the only required value. Fill it in on the MCP detail page. Everything else in `.env.example` is only needed for self-hosting or integration testing.

When the credential is missing the process still starts normally, but every tool call returns an explicit configuration error. This is deliberate: a hosted environment may launch the process before an operator supplies a credential, and a server that refuses to boot looks broken on the listing page.

## Running locally

```bash
python -m pip install -r requirements.txt
export PYTHONPATH=src
export DIYAN_API_KEY=<your tenant credential>
export DIYAN_TRANSPORT=stdio
python -m diyan_research_mcp.server
```

Tests need neither network nor credentials:

```bash
python -m unittest discover -s tests -v
```

## Boundaries

- Read-only. No write, order placement, deployment or data export capability.
- No real-time market data. Snapshots and summaries are frozen artifacts and every result carries an `as_of` field.
- No buy/sell calls, position sizes, share counts, copy-trading or return promises. Questions containing such phrasing are rejected before any request is sent.
- Does not read the user's local files, local databases or unnecessary environment variables.

## Backend contract

To run your own backend, see [`docs/BACKEND_CONTRACT.md`](https://github.com/mikeli20221102-ux/diyan-research-mcp/blob/main/docs/BACKEND_CONTRACT.md).

## License and ownership

Developed and maintained by Shenzhen Tonghua Culture Media Co., Ltd. MIT licensed, see [`LICENSE`](https://github.com/mikeli20221102-ux/diyan-research-mcp/blob/main/LICENSE).
