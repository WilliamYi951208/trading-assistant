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

## Data Ingestion: Two Automatic Modes

The assistant doesn't rely on you pasting bars by hand — it grabs each newly closed bar and analyzes it immediately. Pick either pipeline (or run both); both drop data into `output_dir/bars/` for the Agent to read.

### Mode A: TradingView Webhook (only needs OHLCV + EMA, lowest barrier)

Data flow: **TradingView alert → Pine script builds JSON → HTTP POST to the local receiver → written to the bars dir → Agent analyzes**.

**Step 1: Start the local receiver**

```bash
pip install tradingview-ta
python scripts/webhook_receiver.py
```

Listens on `http://127.0.0.1:8787` by default. Each received bar is written to `output_dir/bars/` (a day-rotated `bars-YYYY-MM-DD.jsonl` plus a rolling `recent-20-bars.json`).

**Step 2: Expose the receiver to the internet**

TradingView alerts can only POST to a public address, so the local port must be tunneled out. ngrok is the simplest:

```bash
ngrok http 8787
```

Note the `https://xxxx.ngrok-free.dev` URL it gives you. If you have a VPS, see `scripts/deploy-vps.sh` to deploy it there and skip launching ngrok every time.

> ⚠️ **The receiver has no authentication by default.** Once it's public, be sure to set `webhook_secret` in `config.json` — the receiver will then validate the `secret` field in the request body and drop requests without the correct key.

**Step 3: Attach the Pine script in TradingView**

1. Open a TradingView chart and switch to the **GC 5-minute timeframe**.
2. Open the Pine editor, paste the full contents of `scripts/tradingview-codex-5m-webhook.pine`, save, and "Add to chart". The script plots an EMA20 and fires an alert on **each confirmed 5m bar close**, with the payload being the assembled JSON (symbol / OHLC / volume / ema20 / bar_index, etc.).
3. Click **Alerts → Create Alert** on the chart:
   - For Condition, pick this indicator (`Codex 5m Webhook - GC Scalp`), trigger on **alert() function calls only**;
   - Set frequency to **Once Per Bar Close**;
   - Tick **Webhook URL** and enter your Step 2 address + `/webhook`, e.g. `https://xxxx.ngrok-free.dev/webhook`;
   - Leave the Message empty — the script already sends the JSON via `alert()` internally.
4. Once the alert is created, data is pushed automatically on every 5m bar close.

> 💡 If you set a `webhook_secret`, the request body needs to carry `secret`. The easiest way is to deploy to a VPS and inject it at the forwarding layer; for a plain ngrok direct connection you can temporarily leave the secret empty and only use it on a local/trusted network.

**Step 4: Run it in the Agent**

Tell the Agent "start trading" (开始做单) — it runs `scripts/poll-new-bar.py` to watch the bars dir, and on every new bar it reads the data and emits a trade recommendation.

### Mode B: ATAS Indicator Export (with Order Flow, richest data)

If you use ATAS for charting, this pipeline additionally captures **Delta / MaxDelta-MinDelta / Footprint** order-flow data — a fuller analysis surface than plain webhook.

Data flow: **ATAS custom indicator → writes local JSON/MD on each bar close → polling script detects the new bar → wakes the Agent to analyze**.

**Step 1: Compile the indicator**

`atas-indicator/` is the C# source for a custom ATAS platform indicator. Build the DLL with .NET:

```bash
cd atas-indicator
dotnet build -c Release
```

> The ATAS indicator depends on the platform's bundled `ATAS.Indicators` assembly, so it must be built on a machine that has ATAS installed. The build output lands under `bin/Release/`.

**Step 2: Load the indicator in ATAS**

Drop the compiled `ClaudeDataExport.dll` into the ATAS indicators folder (usually `Documents\ATAS\Indicators`) and restart ATAS. Add the **Claude Data Export** indicator on a GC 5m chart and set the parameters as needed:

- **Output Directory**: the data export directory (defaults to `G:\PriceAction\交易日志\atas` — change it to your own path);
- **EMA Period**: the EMA period for trend detection (default 20);
- **Recent Bars Count**: how many bars to keep in the rolling file (default 20).

On each bar close the indicator writes two files: `recent-20-bars.json` (structured OHLCV + Delta data) and `latest-atas-brief.md` (a brief with local pre-analysis).

**Step 3: Run it in the Agent**

Tell the Agent "start trading" (开始做单) — it runs `scripts/poll-atas-bar.py` to watch the ATAS export dir, and when it detects a new bar (via a change in `bar_index`) it wakes up to analyze and emit a recommendation.

> Note: Mode B's export directory must match the `BRIEF_FILE` path in `poll-atas-bar.py` (set both to your actual path).

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
