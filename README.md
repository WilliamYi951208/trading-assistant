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

### 3. 启动 Webhook 接收器

```bash
pip install tradingview-ta
python scripts/webhook_receiver.py
```

默认监听 `http://127.0.0.1:8787`。

> ⚠️ **接收器默认无鉴权**。如需暴露到公网（如配合 ngrok / VPS），请务必在配置里设置 `webhook_secret`，接收器会校验请求体中的 `secret` 字段。

### 4. （可选）ATAS 数据导出

`atas-indicator/` 是一个 ATAS 平台自定义指标的 C# 源码，编译后可把实时 OHLCV / Delta / Footprint 导出供助手读取。用 .NET 编译：

```bash
cd atas-indicator
dotnet build -c Release
```

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
