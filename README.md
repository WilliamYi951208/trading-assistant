# Trading Assistant — 期货日内交易助手

[English](README.en.md) | 简体中文

基于 **Al Brooks 价格行为 (Price Action) + SMC + Order Flow + Volume Profile** 四套体系的 GC（黄金期货）5 分钟日内交易助手。支持实时数据获取、自动盘面分析，并以 Agent Skill 形式跨 Claude Code / Codex / OpenClaw 即插即用。

> ⚠️ **免责声明**：本项目仅用于交易方法论学习与个人工具搭建，不构成任何投资建议。期货交易风险极高，盈亏自负。

## 功能概览

- **多体系分析**：价格行为（信号棒 / H-L 计数 / Always In / 交易者方程）、SMC（FVG / Order Block / BOS-CHoCH / 流动性）、Order Flow（Delta / Footprint / DOM）、Volume Profile（POC / VAH-VAL / HVN-LVN）。按现有数据用什么分析什么，不数据瘫痪。
- **两种数据源**：
  - **Webhook 模式** — TradingView alert 推送 K 线到本地接收器
  - **ATAS 模式** — 通过自带 ATAS 指标导出实时 OHLCV / Delta / Footprint
- **自动输出**：每根新 K 生成结构化交易建议（做/不做/等、方向、入场、止损、止盈、手数、理由）。

## 目录结构

```
trading-assistant/
├── README.md
├── SKILL.md                    # Skill 定义（Agent 读取的主文件）
├── SKILL-LITE.md               # 精简版 Skill（webhook 快速模式用）
├── WEBHOOK_FAST_MODE.md        # Webhook 快速模式说明
├── OPENCLAW_INTEGRATION.md     # OpenClaw 集成指南
├── smc-reference.md            # SMC 参考手册
├── vp-reference.md             # Volume Profile 参考手册
├── skill/                      # 可直接安装的 Agent Skill
│   ├── SKILL.md
│   └── references/             # Order Flow / SMC / VP 实战手册
├── scripts/                    # 数据采集与服务脚本
│   ├── webhook_receiver.py     # Webhook 接收器（HTTP 服务）
│   ├── fetch_data.py           # MCP 数据拉取
│   ├── poll-*.py               # 新 K 轮询
│   ├── config.json             # 主配置（模板）
│   ├── config.vps.json         # VPS 部署配置（模板）
│   ├── deploy-vps.sh           # VPS 部署脚本
│   └── *.ps1 / *.bat           # Windows 启动脚本
└── atas-indicator/             # ATAS 数据导出指标（C# 源码）
    ├── ClaudeDataExport.cs
    └── ClaudeDataExport.csproj
```

## 快速开始

### 1. 安装 Skill

把 `skill/` 目录拷到你的 Agent skills 目录，例如：

```bash
# Claude Code
cp -r skill ~/.claude/skills/trading-assistant

# OpenClaw
cp -r skill ~/.agents/skills/trading-assistant
```

### 2. 配置

复制配置模板并填入你自己的值：

```bash
cp scripts/config.json scripts/config.local.json
```

```json
{
  "output_dir": "你的输出目录",
  "data_source": "webhook",
  "mcp_symbol": "GOLD",
  "mcp_timeframe": "5m",
  "host": "127.0.0.1",
  "port": 8787,
  "webhook_secret": "填入你自己的密钥"
}
```

> 🔐 **安全提醒**：仓库中的 `config.json` / `config.vps.json` 是模板，`webhook_secret` 等字段为占位符。部署时务必替换成你自己的密钥，且不要把含真实密钥的配置提交回仓库。

## 数据采集：两种自动获取方式

助手不靠人工贴 K 线，而是自动拿到每根新收盘 K 后立即分析。两套链路二选一（也可同时用），都是把数据落到 `output_dir/bars/` 供 Agent 读取。

### 方式 A：TradingView Webhook（只需 OHLCV + EMA，门槛最低）

数据流：**TradingView 警报 → Pine 脚本拼 JSON → HTTP 推到本地接收器 → 写入 bars 目录 → Agent 分析**。

**第 1 步：启动本地接收器**

```bash
pip install tradingview-ta
python scripts/webhook_receiver.py
```

默认监听 `http://127.0.0.1:8787`，收到的每根 K 会写入 `output_dir/bars/`（按日轮转的 `bars-YYYY-MM-DD.jsonl` + 滚动的 `recent-20-bars.json`）。

**第 2 步：把接收器暴露到公网**

TradingView 的警报只能 POST 到公网地址，所以本地端口要穿透出去。用 ngrok 最简单：

```bash
ngrok http 8787
```

记下它给的 `https://xxxx.ngrok-free.dev` 地址。若你有 VPS，也可参考 `scripts/deploy-vps.sh` 部署到服务器，省去每次开 ngrok。

> ⚠️ **接收器默认无鉴权。** 一旦暴露到公网，务必在 `config.json` 里设置 `webhook_secret`，接收器会校验请求体里的 `secret` 字段，丢弃不带正确密钥的请求。

**第 3 步：在 TradingView 挂 Pine 脚本**

1. 打开 TradingView 图表，切到 **GC 的 5 分钟周期**。
2. 打开 Pine 编辑器，把 `scripts/tradingview-codex-5m-webhook.pine` 全文粘进去，保存并「添加到图表」。脚本会画一条 EMA20，并在每根 5m K **收盘确认**时触发一条警报，警报内容是拼好的 JSON（含 symbol / OHLC / volume / ema20 / bar_index 等）。
3. 点图表上的 **警报（Alarm）→ 新建警报**：
   - 条件（Condition）选这个指标（`Codex 5m Webhook - GC Scalp`），触发选 **alert() function calls only**；
   - 频率选 **Once Per Bar Close**；
   - 勾选 **Webhook URL**，填你第 2 步的地址 + `/webhook`，例如 `https://xxxx.ngrok-free.dev/webhook`；
   - 消息（Message）留空即可，脚本内部已经用 `alert()` 把 JSON 发出去了。
4. 创建警报后，每根 5m K 收盘就会自动推一次数据。

> 💡 若设置了 `webhook_secret`，需要让请求体带上 `secret`。最省事的做法是部署到 VPS 并在转发层注入；纯 ngrok 直连场景可临时把 secret 留空，仅在本机/可信网络使用。

**第 4 步：在 Agent 里开跑**

对 Agent 说「开始做单」，它会调用 `scripts/poll-new-bar.py` 监听 bars 目录，一旦有新 K 就自动读取并输出交易建议。

### 方式 B：ATAS 指标导出（带 Order Flow，数据最全）

如果你用 ATAS 看盘，这条链路能多拿到 **Delta / MaxDelta-MinDelta / Footprint** 等订单流数据，分析维度比纯 webhook 更全。

数据流：**ATAS 自定义指标 → 每根 K 收盘写本地 JSON/MD → 轮询脚本检测新 K → 唤醒 Agent 分析**。

**第 1 步：编译指标**

`atas-indicator/` 是一个 ATAS 平台自定义指标的 C# 源码。用 .NET 编译出 DLL：

```bash
cd atas-indicator
dotnet build -c Release
```

> ATAS 指标依赖平台自带的 `ATAS.Indicators` 程序集，需在本机装有 ATAS 的环境下编译。编译产物在 `bin/Release/` 下。

**第 2 步：在 ATAS 里加载指标**

把编译出的 `ClaudeDataExport.dll` 放进 ATAS 的指标目录（通常是 `Documents\ATAS\Indicators`），重启 ATAS。在 GC 的 5m 图表上添加 **Claude Data Export** 指标，按需设置参数：

- **Output Directory**：数据导出目录（默认 `G:\PriceAction\交易日志\atas`，请改成你自己的路径）；
- **EMA Period**：趋势判断用的 EMA 周期（默认 20）；
- **Recent Bars Count**：滚动保留的 K 线数量（默认 20）。

指标会在每根 K 收盘时写两个文件：`recent-20-bars.json`（含 OHLCV + Delta 的结构化数据）和 `latest-atas-brief.md`（含本地预分析的简报）。

**第 3 步：在 Agent 里开跑**

对 Agent 说「开始做单」，它会调用 `scripts/poll-atas-bar.py` 监听 ATAS 导出目录，检测到新 K（靠 `bar_index` 变化）就唤醒分析并输出建议。

> 注意：方式 B 的导出目录要和 `poll-atas-bar.py` 里的 `BRIEF_FILE` 路径一致（两边都改成你的实际路径）。

## API 端点（Webhook 接收器）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/webhook` | 接收 TradingView K 线推送 |
| POST | `/start` | 开始输出分析 |
| POST | `/stop` | 停止输出分析 |
| GET  | `/status` | 查询运行状态 |
| GET  | `/health` | 健康检查 |
| GET  | `/latest-brief` | 最新分析简报 |
| GET  | `/decision-pack` | 完整决策包 JSON |

## 交易方法论

四套体系融合，核心原则是「按有什么数据用什么，不数据瘫痪」：

- **PA + SMC** 永远可用（只需 OHLCV + EMA）
- **Order Flow** 在有 Footprint / Delta 数据时叠加
- **Volume Profile** 在有成交量分布时叠加

详见 `SKILL.md` 与 `skill/references/` 下的实战手册。

## 配置项说明

| 字段 | 说明 |
|------|------|
| `output_dir` | 分析结果输出目录 |
| `data_source` | `webhook` / `mcp` / `hybrid` |
| `mcp_symbol` | 标的，如 `GOLD` |
| `mcp_timeframe` | 周期，如 `5m` |
| `host` / `port` | 接收器监听地址 |
| `webhook_secret` | Webhook 鉴权密钥（留空则不校验，公网部署务必填写） |

## License

MIT — 见 [LICENSE](LICENSE)。
