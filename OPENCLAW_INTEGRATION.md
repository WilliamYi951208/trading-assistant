# Price Action Trading Assistant — OpenClaw 集成指南

**更新时间**：2026-05-18

本文档说明如何在 OpenClaw 中使用 Price Action Trading Assistant。

## 快速开始

### 1. 安装 tradingview-mcp-server

```bash
pip install tradingview-mcp-server
```

### 2. 配置 OpenClaw MCP Server

编辑 `~/.openclaw/openclaw.json`（或 Windows 上的 `%USERPROFILE%\.openclaw\openclaw.json`），添加：

```json
{
  "mcpServers": {
    "tradingview": {
      "command": "python",
      "args": ["-m", "tradingview_mcp.server"]
    }
  }
}
```

### 3. 安装 Price Action Skill

将本项目的 skill 注册到 OpenClaw：

```bash
# Windows PowerShell
cd "c:\Users\Windows\Documents\Codex\2026-05-12\c-users-windows-agents-skills-price"
.\install-price-action-skill-hotplug.ps1
```

或手动复制：

```bash
# 复制到 OpenClaw skills 目录
cp -r . ~/.agents/skills/price-action-assistant/
```

### 4. 配置数据源

编辑 `config.json`，设置数据源模式：

```json
{
  "output_dir": "G:\\PriceAction\\交易日志",
  "data_source": "mcp",
  "mcp_symbol": "GOLD",
  "mcp_exchange": "TVC",
  "mcp_timeframe": "5m",
  "mcp_poll_interval": 300,
  "webhook_data_dir": "webhook-data",
  "log_prefix": "trade-log",
  "webhook_secret": "",
  "host": "127.0.0.1",
  "port": 8787,
  "methodology": "price_action",
  "methodology_note": "当前使用 Al Brooks Price Action，后续可扩展 SMC 等"
}
```

**数据源模式**：
- `"data_source": "webhook"` — 使用 TradingView webhook 推送（需要 ngrok）
- `"data_source": "mcp"` — 使用 tradingview-mcp 主动拉取（推荐）
- `"data_source": "hybrid"` — 两者都支持

## 使用方式

### 在 OpenClaw 中启动交易助手

**方式 1：直接对话**

```
你：开始做单
助手：[调用 /start API，开始自动分析]
```

**方式 2：使用 MCP 工具**

OpenClaw 会自动识别你的交易相关问题，并调用 tradingview-mcp 的工具：

```
你：GC 现在什么价格？
助手：[调用 MCP coin_analysis 获取实时数据]

你：给我分析一下 GC 5m 的价格行为
助手：[获取数据 → 应用价格行为分析 → 输出建议]
```

### 数据获取方式

#### MCP 模式（推荐）

使用 `fetch_data.py` 脚本主动获取数据：

```bash
# 获取 GC 5m 数据
python fetch_data.py GC1!

# 获取其他标的
python fetch_data.py AAPL NASDAQ 5m
python fetch_data.py BTCUSDT BINANCE 5m
```

支持的黄金标的格式：
- `GC1!` → 自动映射为 `GOLD @ TVC`
- `GC` → 自动映射为 `GOLD @ TVC`
- `GOLD` → `GOLD @ TVC`
- `XAUUSD` → `XAUUSD @ OANDA`

#### Webhook 模式

保持原有的 TradingView alert → webhook 流程：

1. 启动接收器：`python webhook_receiver.py`
2. 配置 ngrok：`ngrok http 8787`
3. 在 TradingView 中设置 alert，URL 指向 ngrok 地址

## 工作流程

### MCP 模式工作流

```
用户说"开始做单"
  ↓
OpenClaw 调用 POST http://127.0.0.1:8787/start
  ↓
每 5 分钟（可配置）：
  - 调用 fetch_data.py 获取 GC 数据
  - POST 到 webhook_receiver.py 的 /webhook 端点
  - 生成分析到 G:\PriceAction\交易日志\latest-codex-brief.md
  ↓
OpenClaw 读取 brief 并输出交易建议
  ↓
用户说"停" → 调用 POST http://127.0.0.1:8787/stop
```

### Webhook 模式工作流

```
TradingView 5m K 收盘
  ↓
发送 webhook 到 http://your-ngrok-url/webhook
  ↓
webhook_receiver.py 接收并生成分析
  ↓
OpenClaw 读取 brief 并输出交易建议
```

## 输出文件

所有分析结果统一输出到 `G:\PriceAction\交易日志\`：

- `latest-codex-brief.md` — 最新分析（Markdown）
- `latest-decision-pack.json` — 完整决策包（JSON）
- `session-state.json` — 运行状态
- `bars/bars-YYYY-MM-DD.jsonl` — K 线历史
- `bars/recent-20-bars.json` — 最近 20 根 K 线
- `trade-log-YYYY-MM-DD.md` — 交易日志

## API 端点

**控制端点**：
- `POST /start` — 开始输出分析
- `POST /stop` — 停止输出分析
- `GET /status` — 查询状态

**数据端点**：
- `GET /health` — 健康检查
- `GET /latest-brief` — 最新分析
- `GET /decision-pack` — 完整决策包
- `POST /webhook` — 接收数据（webhook 或 MCP 都用这个）

## 故障排查

### MCP Server 无法启动

```bash
# 检查 tradingview-mcp-server 是否安装
pip show tradingview-mcp-server

# 测试 MCP Server
python -m tradingview_mcp.server --help
```

### 数据获取失败

```bash
# 测试数据获取脚本
python fetch_data.py GC1!

# 如果失败，尝试其他格式
python fetch_data.py GOLD TVC 5m
python fetch_data.py XAUUSD OANDA 5m
```

### webhook_receiver.py 无法启动

```bash
# 检查端口是否被占用
netstat -ano | findstr :8787

# 检查配置文件
cat config.json

# 检查输出目录权限
ls "G:/PriceAction/交易日志/"
```

## 高级配置

### 自定义轮询间隔

在 `config.json` 中设置：

```json
{
  "mcp_poll_interval": 300
}
```

单位：秒。默认 300 秒（5 分钟）。

### 多标的支持

修改 `config.json` 添加多个标的：

```json
{
  "mcp_symbols": [
    {"symbol": "GOLD", "exchange": "TVC", "timeframe": "5m"},
    {"symbol": "AAPL", "exchange": "NASDAQ", "timeframe": "5m"}
  ]
}
```

### 切换交易方法论

在 `config.json` 中修改：

```json
{
  "methodology": "smc",
  "methodology_note": "Smart Money Concepts"
}
```

然后在分析逻辑中根据 `methodology` 字段选择不同的分析方法。

## 参考文档

- [AGENT_BOOTSTRAP.md](G:/PriceAction/交易日志/AGENT_BOOTSTRAP.md) — 跨 Agent 统一入口
- [portable-trading-context.md](portable-trading-context.md) — 完整交易上下文
- [WEBHOOK_FAST_MODE.md](WEBHOOK_FAST_MODE.md) — Webhook 模式说明
- [tradingview-mcp GitHub](https://github.com/atilaahmettaner/tradingview-mcp) — MCP Server 文档

---

**最后更新**：2026-05-18  
**支持的 Agent**：OpenClaw, Claude Code, Codex  
**数据源**：tradingview-mcp (MCP) / TradingView webhook
