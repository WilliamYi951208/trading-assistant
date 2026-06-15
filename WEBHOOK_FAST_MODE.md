# TradingView Webhook Fast Mode

目标：TradingView 5m K 线到达本地后，Codex 在 30 秒内给出执行优先建议；盘中讨论时不被无意义自动化打断。

## 当前架构

1. TradingView Pine 在每根 5m K 收盘时发送 JSON webhook。
2. 本地 `webhook_receiver.py` 接收并落盘：
   - `webhook-data/latest-bars.json`
   - `webhook-data/bars.jsonl`
3. 接收器同步生成快速决策包：
   - `webhook-data/latest-decision-pack.json`
   - `webhook-data/latest-codex-brief.md`
   - `webhook-data/session-context.json`

## Codex 快速分析输入

跨对话/跨工具时，先加载：

```text
portable-trading-context.md
```

自动化或新对话优先只读：

```text
webhook-data/latest-codex-brief.md
```

必要时再读：

```text
webhook-data/latest-decision-pack.json
webhook-data/bars.jsonl
account-status.md
```

不要默认读取整段旧对话。旧对话只用于复盘，不用于每根新 K 的快速判断。交易经验和账户规则以 `portable-trading-context.md` 为准。

## 输出格式

每根新 K 只输出一段简短建议：

```text
结论：做 / 不做 / 等
方向：
触发/入场：
止损/失效：
TP：
仓位：
理由：
```

如果没有清楚优势，直接说：

```text
结论：等。理由：...
```

## 盘中讨论规则

- 新 K 到达前，如果用户正在讨论计划，不主动插入无关自动化。
- 新 K 到达后，只有当它改变计划或触发候选 setup，才提醒。
- 如果只是“同一观点继续成立”，一句话即可。
- 不自动下单、不改单、不撤单，只给用户手动执行建议。

## 当前账户假设

- TakeProfitTrader / TPT：PRO 阶段，优先保护账户和建立 buffer。
- Alpha Futures：Qualified/Pro 管理目标，长期希望接近 $15,000 单次出金上限；先完成提款资格和利润池。
- 默认 GC 1 手；2 手只用于 A+ 干净强趋势机会，并且需要用户确认。

## 自动化建议

如果使用 Codex heartbeat，频率最多 1 分钟一次。提示词应极短：

```text
Check webhook-data/latest-decision-pack.json. If latest_bar.identity equals webhook-data/last-reported-bar.txt, DONT_NOTIFY. If new, update state and NOTIFY using webhook-data/latest-codex-brief.md. Keep it concise: 做/不做/等, direction, trigger, stop, TP, size, reason. Do not read old conversation unless needed. No auto execution.
```

更理想的未来版本：由本地接收器在收到 webhook 后触发一个事件，而不是 Codex 轮询。
