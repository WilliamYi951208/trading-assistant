# Trading Assistant — Intraday Futures Trading Assistant

English | [简体中文](README.md)

An intraday trading assistant for GC (gold futures) on the 5-minute timeframe, built on four analysis frameworks: **Al Brooks Price Action + SMC + Order Flow + Volume Profile**. It supports real-time data ingestion and automated chart analysis, and ships as a plug-and-play Agent Skill for Claude Code / Codex / OpenClaw.

> ⚠️ **Disclaimer**: This project is for learning trading methodology and building personal tooling only. It does not constitute investment advice. Futures trading carries high risk — you are solely responsible for your own gains and losses.

## Features

- **Multi-framework analysis**: Price Action (signal bars / H-L counting / Always In / trader's equation), SMC (FVG / Order Block / BOS-CHoCH / liquidity), Order Flow (Delta / Footprint / DOM), and Volume Profile (POC / VAH-VAL / HVN-LVN). Use whatever the available data supports — no analysis paralysis.
- **Two data sources**:
  - **Webhook mode** — TradingView alerts push bars to a local receiver
  - **ATAS mode** — export real-time OHLCV / Delta / Footprint via the bundled ATAS indicator
- **Automated output**: generates a structured trade recommendation on every new bar (take/skip/wait, direction, entry, stop loss, take profit, position size, rationale).

## Project Structure

```
trading-assistant/
├── README.md                   # Chinese README
├── README.en.md                # This file
├── SKILL.md                    # Skill definition (main file the Agent reads)
├── SKILL-LITE.md               # Lite Skill (for webhook fast mode)
├── WEBHOOK_FAST_MODE.md        # Webhook fast mode notes
├── OPENCLAW_INTEGRATION.md     # OpenClaw integration guide
├── smc-reference.md            # SMC reference manual
├── vp-reference.md             # Volume Profile reference manual
├── skill/                      # Installable Agent Skill
│   ├── SKILL.md
│   └── references/             # Order Flow / SMC / VP field manuals
├── scripts/                    # Data collection & service scripts
│   ├── webhook_receiver.py     # Webhook receiver (HTTP service)
│   ├── fetch_data.py           # MCP data pull
│   ├── poll-*.py               # New-bar polling
│   ├── config.json             # Main config (template)
│   ├── config.vps.json         # VPS deployment config (template)
│   ├── deploy-vps.sh           # VPS deployment script
│   └── *.ps1 / *.bat           # Windows launch scripts
└── atas-indicator/             # ATAS data export indicator (C# source)
    ├── ClaudeDataExport.cs
    └── ClaudeDataExport.csproj
```

## Quick Start

### 1. Install the Skill

Copy the `skill/` directory into your Agent's skills folder, e.g.:

```bash
# Claude Code
cp -r skill ~/.claude/skills/trading-assistant

# OpenClaw
cp -r skill ~/.agents/skills/trading-assistant
```

### 2. Configure

Copy the config template and fill in your own values:

```bash
cp scripts/config.json scripts/config.local.json
```

```json
{
  "output_dir": "your output directory",
  "data_source": "webhook",
  "mcp_symbol": "GOLD",
  "mcp_timeframe": "5m",
  "host": "127.0.0.1",
  "port": 8787,
  "webhook_secret": "set your own secret here"
}
```

> 🔐 **Security note**: The `config.json` / `config.vps.json` files in this repo are templates; fields like `webhook_secret` are placeholders. Replace them with your own secrets when deploying, and never commit configs containing real secrets back to the repo.

### 3. Start the Webhook Receiver

```bash
pip install tradingview-ta
python scripts/webhook_receiver.py
```

Listens on `http://127.0.0.1:8787` by default.

> ⚠️ **The receiver has no authentication by default.** If you expose it to the public internet (e.g. via ngrok / a VPS), be sure to set `webhook_secret` in the config — the receiver will then validate the `secret` field in each request body.

### 4. (Optional) ATAS Data Export

`atas-indicator/` is the C# source for a custom ATAS platform indicator. Once compiled, it exports real-time OHLCV / Delta / Footprint for the assistant to read. Build it with .NET:

```bash
cd atas-indicator
dotnet build -c Release
```

## API Endpoints (Webhook Receiver)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/webhook` | Receive TradingView bar pushes |
| POST | `/start` | Start emitting analysis |
| POST | `/stop` | Stop emitting analysis |
| GET  | `/status` | Query runtime status |
| GET  | `/health` | Health check |
| GET  | `/latest-brief` | Latest analysis brief |
| GET  | `/decision-pack` | Full decision pack JSON |

## Trading Methodology

Four frameworks combined, with the core principle "use whatever data you have — no analysis paralysis":

- **PA + SMC** are always available (only need OHLCV + EMA)
- **Order Flow** layers in when Footprint / Delta data is available
- **Volume Profile** layers in when volume distribution is available

See `SKILL.md` and the field manuals under `skill/references/` for details.

## Configuration Reference

| Field | Description |
|-------|-------------|
| `output_dir` | Output directory for analysis results |
| `data_source` | `webhook` / `mcp` / `hybrid` |
| `mcp_symbol` | Instrument, e.g. `GOLD` |
| `mcp_timeframe` | Timeframe, e.g. `5m` |
| `host` / `port` | Receiver listen address |
| `webhook_secret` | Webhook auth secret (empty = no validation; always set it for public deployments) |

## License

MIT — see [LICENSE](LICENSE).
