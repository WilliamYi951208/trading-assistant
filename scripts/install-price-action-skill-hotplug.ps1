$ErrorActionPreference = "Stop"

$targets = @(
  "C:\Users\Windows\.codex\skills\价格行为助手\SKILL.md",
  "C:\Users\Windows\.agents\skills\price-action-assistant\SKILL.md"
)

$markerStart = "<!-- CODEx_PRICE_ACTION_HOTPLUG_CONTEXT_START -->"
$markerEnd = "<!-- CODEx_PRICE_ACTION_HOTPLUG_CONTEXT_END -->"

$block = @"
$markerStart

## 热插拔交易上下文与 Webhook 快速模式

当用户使用本价格行为助手进行 GC 5分钟 scalp、prop firm 账户管理、TradingView webhook、半自动读 K、或说“开始做单”时，必须优先恢复便携上下文，而不是依赖当前对话历史。

默认便携上下文目录：

`C:\Users\Windows\Documents\Codex\2026-05-12\c-users-windows-agents-skills-price`

优先读取这些文件：

1. `portable-trading-context.md`：跨对话/跨工具的核心交易上下文。
2. `account-status.md`：账户阶段与目标。
3. `WEBHOOK_FAST_MODE.md`：TradingView webhook 快速分析规则。
4. `webhook-data/latest-codex-brief.md`：最新 5m K 的最小决策包。
5. 必要时再读 `webhook-data/latest-decision-pack.json` 和 `webhook-data/bars.jsonl`。

不要默认读取整段旧对话来恢复状态。旧对话只用于复盘；盘中新 K 判断以便携上下文和最新 webhook brief 为准。

### 当前账户默认假设

- TakeProfitTrader / TPT：按 PRO 账户管理。目标是保护账号、建立 buffer，重点防 intraday trailing drawdown，不再按 evaluation 冲刺。
- Alpha Futures：按 Qualified/Pro 管理。先完成提款资格和 $200+ 盈利日，再稳步堆利润池；长期目标尽量接近 $15,000 单次出金上限。
- 双账号共同规则：默认 GC 1 手；2 手只用于 A+ 干净强趋势机会，并且需要用户明确确认。

### Webhook 快速输出要求

TradingView 5m K 到达本地后，优先读取 `webhook-data/latest-codex-brief.md`，最多 30 秒内给出中文执行建议。输出必须包含：

```text
结论：做 / 不做 / 等
方向：
触发/入场：
止损/失效：
TP：
仓位：
理由：
```

如果没有清楚优势，直接给“等”，不要硬凑交易。用户在新 K 之间讨论计划时，不主动插入无关自动化；只有新 K 改变计划、触发候选 setup、或影响持仓管理时才提醒。

所有订单必须由用户手动执行。助手不得自动下单、改单、撤单。

$markerEnd
"@

foreach ($target in $targets) {
  if (-not (Test-Path -LiteralPath $target)) {
    Write-Warning "Missing: $target"
    continue
  }

  $content = Get-Content -LiteralPath $target -Raw -Encoding UTF8
  $pattern = [regex]::Escape($markerStart) + ".*?" + [regex]::Escape($markerEnd)

  if ($content -match $pattern) {
    $content = [regex]::Replace($content, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $block }, "Singleline")
  } else {
    $content = $content.TrimEnd() + "`r`n`r`n" + $block + "`r`n"
  }

  Set-Content -LiteralPath $target -Value $content -Encoding UTF8
  Write-Host "Updated: $target"
}

Write-Host "Done. Price action assistant hotplug context installed."
