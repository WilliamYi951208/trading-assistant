# Order Flow 实战手册

> 基于 ATAS 平台的 Order Flow 分析，聚焦 GC 黄金期货 5m scalp。
> 本手册所有概念均以实战为导向，帮助在关键价位做出快速判断。

---

## 一、Delta 分析

### 1.1 Delta 定义

Delta = 主动买成交量（Aggressive Buys）- 主动卖成交量（Aggressive Sells）。主动买指以 Ask 价成交（买方吃卖方挂单），主动卖指以 Bid 价成交（卖方吃买方挂单）。Delta 衡量的是这根 K 线内"谁更急迫"——急迫方愿意付出滑点代价去成交。

### 1.2 单根 K 的 Delta 判读

| K 线方向 | Delta 方向 | 含义 | 实战意义 |
|---------|-----------|------|---------|
| 阳线 | Delta > 0 | **正常多头**（Normal Bullish） | 价格涨、主动买盘推动，趋势健康，无需特别关注 |
| 阳线 | Delta < 0 | **吸筹/被动买盘**（Passive Buying / Absorption） | 价格涨但主动卖单更多，说明有大量限价买单在吃住抛压。这是机构吸货的典型痕迹——表面看空实际被接住，后续往往有更大幅度的上涨 |
| 阴线 | Delta > 0 | **抛压/被动卖盘**（Passive Selling / Distribution） | 价格跌但主动买单更多，说明有大量限价卖单在派发。机构在出货——表面有人买，但每次买都被更大的卖方吃掉，后续往往继续下跌 |
| 阴线 | Delta < 0 | **正常空头**（Normal Bearish） | 价格跌、主动卖盘推动，趋势健康，无需特别关注 |

**实战要点**：重点关注"不正常"的两种组合（阳线负 Delta、阴线正 Delta），它们往往出现在反转前或者趋势延续中的蓄力阶段。

### 1.3 Delta 占比（Delta / Volume %）

Delta% = Delta / 总成交量 x 100%。这个比值消除了成交量大小的干扰，让你判断"方向性的纯度"。Delta% > 30% 说明方向性极强，一边倒；Delta% 在 10%-30% 属于中等方向性；Delta% < 10% 说明多空势均力敌，成交量大但没方向，通常出现在震荡区间或转折点。GC 5m 级别上，Delta% 突然从 <10% 跳升到 >25%，通常意味着突破即将发生。

### 1.4 MaxDelta / MinDelta

MaxDelta 是这根 K 线形成过程中，Delta 达到的最大正值；MinDelta 是最大负值。它们反映了 bar 内盘中最强一波的方向和力度。如果收盘 Delta 接近零但 MaxDelta 很大，说明多头曾经猛攻但被完全吸收——这是空头力量强大的信号。反之亦然。在 ATAS 中可以将 MaxDelta/MinDelta 添加为 K 线下方指标列，辅助判断 bar 内的"战斗过程"。

### 1.5 Cumulative Delta Divergence（累积 Delta 背离）

Cumulative Delta（CD）是 Delta 的逐根累加，形成一条连续曲线。当价格创新高但 CD 没有同步创新高，形成**顶背离**（Bearish CD Divergence），说明虽然价格在涨，但主动买方的力度在衰减，上涨靠惯性而非新资金推动。反之，价格创新低但 CD 没有新低 = **底背离**（Bullish CD Divergence），空方力竭。CD 背离是 Order Flow 最强的反转预警之一，但需要在关键价位（支撑/阻力/VP POC）出现才有效，孤立的背离意义不大。

---

## 二、Footprint / Cluster 分析

### 2.1 Bid x Ask 矩阵读法

Footprint（也叫 Cluster Chart）将每根 K 线拆解为每个价位的成交细节。ATAS 的 Footprint 显示为左右两列：左列是 Bid 成交量（卖方吃买方挂单 = 主动卖），右列是 Ask 成交量（买方吃卖方挂单 = 主动买）。阅读时从上往下扫，关注两侧数字悬殊的价位——那里是多空交锋最激烈的地方。

### 2.2 Imbalance（不平衡）

当某一个价位的 Bid:Ask 比例超过 3:1（或 300%），标记为**卖方不平衡**（Sell Imbalance），说明该价位主动卖远大于主动买，空方在此价位占绝对优势。反之 Ask:Bid > 3:1 为**买方不平衡**（Buy Imbalance）。ATAS 默认用颜色高亮标记（通常蓝色/红色），在 Cluster Settings 中可调整 Imbalance 阈值。单个 Imbalance 价位只是信号，需要结合位置和其他确认。

### 2.3 Stacked Imbalance（连续不平衡）

当连续 3 个或以上价位出现同方向的 Imbalance，形成 **Stacked Imbalance**，这是最强的方向性信号之一。Stacked Buy Imbalance 意味着买方在连续多个价位都压倒性胜出，通常出现在机构扫货或止损瀑布中。看到 Stacked Imbalance 时：如果它朝你的持仓方向 = 加仓/持有信号；如果它朝你的反方向 = 立刻评估是否止损。Stacked Imbalance 形成的价位区域日后通常作为支撑/阻力。

### 2.4 Unfinished Business（未完成业务）

某个价位只有一侧有成交（只有 Bid 没有 Ask，或反之），称为 Unfinished Business 或 Unfinished Auction。这说明价格在此价位快速穿过，没有完成双向拍卖。市场有很强的倾向会回到这些价位"完成"交易。在 ATAS 中这些价位通常用特殊标记显示，可以将其作为短期的价格磁吸目标。

### 2.5 实战：ATAS Footprint 快速找入场确认

操作流程：(1) PA/SMC 给出方向和入场区域；(2) 等价格触及该区域时切换到 Footprint 视图；(3) 扫描当前和前一根 bar 的 Imbalance 分布——如果在你想做多的区域看到 Stacked Buy Imbalance 或 Unfinished Business 在下方，就是强确认；(4) 同时检查 Delta 是否配合（做多时 Delta 转正或底背离）；(5) 确认后入场，SL 放在 Stacked Imbalance 区域的外侧。

---

## 三、DOM / Level 2 分析

### 3.1 Bid Liquidity vs Ask Liquidity 比值

DOM（Depth of Market）显示当前市场两侧的挂单深度。Bid 侧总挂单量 vs Ask 侧总挂单量的比值反映了当前市场的**意愿倾向**（注意是意愿不是事实，因为挂单可以撤）。GC 上如果 Bid:Ask 比 > 1.5:1，说明买方挂单厚度明显大于卖方，价格下方有较强支撑意愿。但要警惕——DOM 是可以被操纵的，大单可以随时撤单（Spoofing），所以 DOM 只作为辅助参考，不能作为唯一入场依据。

### 3.2 被动大单 / 冰山单（Iceberg Order）识别

冰山单是机构拆分的大单，每次只显示一小部分。识别方法：在 DOM 上某个价位持续显示小量挂单（比如 5 手），但成交后立刻又出现同样的 5 手，反复多次——说明这个价位有人在用算法持续挂单。在 ATAS 的 Smart DOM 或 Footprint 中，如果某价位成交量远大于曾经显示的挂单量，就是冰山单的证据。冰山单所在价位通常是强支撑/阻力。

### 3.3 大单吃穿（Aggressive Sweep）

当一侧出现大量主动成交，将另一侧的挂单逐级吃穿，称为 Aggressive Sweep。比如某一瞬间 Ask 侧从 2950.0 到 2953.0 连续 4 个价位的挂单都被买方吃光。这是最强的方向确认信号——说明有大资金不在乎成本地扫货。在 ATAS 的时间与成交量面板中可以看到成交速度的突然加速。Sweep 完成后通常还会继续该方向移动，因为止损连锁反应会跟上。

### 3.4 Pull / Stack 行为

**Pull**（撤单）：原来 Bid 侧某价位挂着大单（比如 50 手），突然消失。如果发生在支撑位 = 买方撤退，支撑不可靠，价格可能下破。**Stack**（堆单）：某价位突然出现大量新挂单。如果是在当前价格前方的 Ask 侧 = 阻力增强。注意区分真实的 Pull/Stack 和 Spoofing——如果大单反复出现又消失，大概率是诱骗行为。

### 3.5 实战：ATAS DOM 面板怎么看

打开 ATAS 的 Smart DOM（快捷键可自定义）。左侧 Bid 列、右侧 Ask 列、中间价格梯。关注三件事：(1) 两侧挂单总量比值，写在面板顶部；(2) 当前价附近 2-3 个 tick 范围内有没有异常大单（比正常挂单量大 3 倍以上）；(3) 实时成交列（最左/最右列），观察是 Bid 侧还是 Ask 侧在持续被吃。DOM 数据变化极快，不要试图记住每个数字，只抓大单和异常。

---

## 四、Aggr Trades（主动成交）

### 4.1 Aggr Buys vs Aggr Sells 量对比

Aggr Trades 面板实时显示每一笔主动成交的方向和大小。核心看法：在一段时间窗口内（比如最近 30 秒），Aggr Buys 的总量和笔数是否明显大于 Aggr Sells。如果买方主动成交量是卖方的 2 倍以上且持续，方向大概率向上。这比 Delta 更实时——Delta 是 bar 结束时的总和，Aggr Trades 是逐笔的。

### 4.2 大单追踪（Large Trade Tracking）

在 ATAS 中可以设置大单阈值（GC 上建议 10-20 手以上标记为大单）。当大单连续出现在同一方向时，说明机构在行动。特别关注：(1) 在支撑位出现连续大单主动买 = 机构接货；(2) 在阻力位出现连续大单主动卖 = 机构出货；(3) 在无明显支撑/阻力的位置突然出现大单 = 可能是新信息驱动的方向性交易。

### 4.3 吃单速度 / 吸收率（Absorption Rate）

吸收率描述的是：一方持续主动成交，但价格不动或反向移动。比如大量 Aggr Sells 出现但价格不跌甚至微涨——说明买方的被动挂单在完全"吸收"卖方的攻击。这是非常强的反转信号，通常发生在关键支撑/阻力位。在 ATAS 中通过同时观察 Aggr Trades 面板（看到大量卖单）和 K 线（价格不跌）来识别吸收。

### 4.4 实战：ATAS Smart Tape 的关键列

ATAS 的 Smart Tape（成交明细）有几个关键列：(1) **Time**——精确到毫秒的成交时间；(2) **Price**——成交价位；(3) **Volume**——成交手数；(4) **Side**——Buy（主动买，绿色）或 Sell（主动卖，红色）；(5) **Cumulative**——累积值。实战中把 Smart Tape 调到只显示大单（过滤掉 1-2 手的噪音），然后重点看大单的方向和频率。如果 30 秒内连续 3 笔以上大单买入，配合价格在支撑位，做多信心极大。

---

## 五、Heatmap（热力图 / 大单挂单可视化）

### 5.1 颜色含义

Heatmap（ATAS 中叫 Heatmap 或 Depth of Market Map）以颜色深浅显示各价位的挂单密度。黄色/橙色区域 = 大量限价单堆积（高流动性区域）。颜色越亮越深，挂单量越大。Heatmap 的核心价值是让你**一眼看到**大资金在哪里布防。

### 5.2 大单墙的含义

当某个价位出现明亮的 Heatmap 条带，形成所谓"大单墙"（Order Wall），它通常意味着：(1) 在 Bid 侧 = 有人在此价位布下大量买入限价单，形成**支撑墙**；(2) 在 Ask 侧 = 有人在此价位布下大量卖出限价单，形成**阻力墙**。大单墙不保证价格一定被挡住，但它提供了一个概率偏向——价格到达此位置时会遇到阻力。

### 5.3 大单墙被吃 vs 大单墙撤单

**被吃穿**（Absorbed/Swept）：价格到达大单墙，大量主动成交发生，墙逐渐被消耗直到消失，价格穿越。这是极强的方向信号——说明有更大的资金愿意付出巨大成本穿越这道防线。穿越后通常加速。**撤单**（Pulled/Cancelled）：价格还没到达，大单墙就消失了。这通常是 Spoofing（欺骗挂单）——制造假的支撑/阻力来诱骗散户。关键区分方法：看大单墙是在价格到达前消失（撤单 = 假墙）还是在大量成交后消失（被吃 = 真墙）。

### 5.4 实战示例

假设 GC 在 2950 附近，Heatmap 显示 2948 有明亮的 Bid 侧大单墙。价格 5 次下探 2948 都没破——每次到达时都有大量成交但价格被弹回。这说明 2948 有强力被动买方在接货，是真实支撑。做多策略：第 3-5 次测试不破时入场做多，SL 放在 2947 以下（墙外），TP 看上方阻力。如果第 6 次测试时墙突然在价格到达前消失（撤单），立刻取消做多计划。

---

## 六、Volume Profile 与 Order Flow 配合

### 6.1 POC 处的 Delta 方向

POC（Point of Control）是成交量最密集的价位。当价格在 POC 附近交易时，观察该区域的 Delta 方向：如果 POC 处 Delta 持续为正，说明主力在此价位以**主动买为主**，主力偏多；如果 Delta 持续为负，主力偏空。这个信息帮你在 POC 这个"多空战场"上判断谁更可能赢。

### 6.2 VAH/VAL 处的 DOM 行为

VAH（Value Area High）和 VAL（Value Area Low）是 Value Area 的上下边界，价格在这里通常面临方向选择。在 VAH 处看 DOM：如果 Ask 侧出现大量挂单（阻力墙） = 价格大概率被拒回 VA 内；如果 Ask 侧挂单稀薄且有 Aggressive Sweep = 大概率突破。在 VAL 处看 DOM：如果 Bid 侧有冰山单持续吸收 = 支撑有效；如果 Bid 侧大单被快速吃穿 = 下破。

### 6.3 HVN 与 LVN 的 Order Flow 特征

**HVN（High Volume Node）**：高成交量价位，价格在此区域通常运动缓慢，双向成交密集，Delta 数值大但方向可能不明确。在 HVN 区域交易像在泥潭中行走——不适合做突破，适合做回归。**LVN（Low Volume Node）**：低成交量价位，价格在此快速穿越。当价格接近 LVN 时，观察 Aggr Trades 的速度——如果加速且单方向 = 继续穿越；如果减速 = 可能在 LVN 另一侧的 HVN 停住。

---

## 七、Order Flow 入场模型（实战 Checklist）

### 入场五步确认

```
步骤 1 ─ 确定方向
   └─ PA（Price Action）/ SMC（Smart Money Concepts）给出方向偏见
   └─ 例：看到 BOS（Break of Structure）向上 + 回踩到 OB（Order Block）

步骤 2 ─ 等价格到达关键区域
   └─ OB / FVG / VP 的 POC / 前期 support-resistance / Heatmap 大单墙
   └─ 不追价，让价格来找你

步骤 3 ─ Footprint 确认（至少满足一个）
   □ 出现 Stacked Imbalance 朝你的方向
   □ Delta 背离（价格继续跌但 Delta 转正 / 价格继续涨但 Delta 转负）
   □ DOM 大单墙在你的方向且没被吃穿
   □ Unfinished Business 在 TP 方向（价格有磁吸目标）

步骤 4 ─ Aggr Trades 确认
   □ 主动买/卖单放量朝你的方向
   □ 出现大单（GC 上 10+ 手）连续同方向成交
   □ 吸收现象：对手方大量攻击但价格不动

步骤 5 ─ 执行
   └─ 入场：满足步骤 3 中至少 1 项 + 步骤 4 中至少 1 项
   └─ SL：放在 Stacked Imbalance 区域外 / 大单墙外 / OB 外
   └─ TP：对侧 LVN / 对侧大单墙 / 下一个 HVN 边缘
```

### 快速判断矩阵

| 你想做 | 需要看到 | 危险信号（不做） |
|-------|---------|--------------|
| 做多 | 支撑位 Stacked Buy Imbalance + Aggr Buy 放量 + Bid 侧有冰山单 | 支撑位大单墙撤单 + Delta 持续负 + Aggr Sell 加速 |
| 做空 | 阻力位 Stacked Sell Imbalance + Aggr Sell 放量 + Ask 侧有冰山单 | 阻力位大单墙被吃穿 + Delta 持续正 + Aggr Buy 加速 |
| 突破做多 | Ask 侧大单墙被 Aggressive Sweep + Stacked Buy Imbalance + LVN 在上方 | 假突破：穿越后 Delta 迅速转负 + Aggr Buy 枯竭 |
| 突破做空 | Bid 侧大单墙被 Aggressive Sweep + Stacked Sell Imbalance + LVN 在下方 | 假突破：穿越后 Delta 迅速转正 + Aggr Sell 枯竭 |

---

## 附录：ATAS 关键设置备忘

| 工具 | ATAS 面板 | 关键设置 |
|-----|----------|---------|
| Delta | Chart 下方指标 | 添加 Delta 指标，显示 MaxDelta/MinDelta |
| Cumulative Delta | 独立子图 | 添加 Cumulative Delta，与价格对比看背离 |
| Footprint | Chart 类型切换 | Cluster Chart → Bid x Ask 模式，Imbalance 阈值设 300% |
| DOM | Smart DOM 面板 | 显示 Bid/Ask 总量比，标记大单（>10手） |
| Aggr Trades | Smart Tape 面板 | 过滤小单（<3手），按方向着色 |
| Heatmap | Chart 叠加层 | Depth of Market Map，调整颜色灵敏度 |
| Volume Profile | Chart 叠加层 | 显示 POC/VAH/VAL，标记 HVN/LVN |

---

> **记住**：Order Flow 是确认工具，不是方向工具。先用 PA/SMC 定方向，再用 Order Flow 找精确入场点和评估信号质量。没有 Order Flow 确认的 PA 信号可以做（B 级），有 Order Flow 确认的是 A+ 级别。
