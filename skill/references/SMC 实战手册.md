# SMC 实战手册

> 基于 ICT/Trading Hub 方法论，聚焦 GC（Gold Futures）5 分钟日内 scalp 实战应用。
> 术语格式：中文（English）。所有时间均为北京时间（BJT）。

---

## 一、市场结构（Market Structure）

### BOS（Break of Structure）

价格打破前一个同方向的摆动高/低点，确认当前趋势延续。上升趋势中，新高突破前高 = bullish BOS；下降趋势中，新低跌破前低 = bearish BOS。BOS 是"趋势还在"的信号，不是入场信号本身——你要等它回踩再做。

### CHoCH（Change of Character）

价格首次打破反方向的关键摆动点，暗示趋势可能反转。比如一直在创新高，突然跌破最近一个 higher low，这就是 bearish CHoCH。CHoCH 是"趋势可能变了"的第一个警报，但不等于确认反转——确认需要后续的 BOS。

### BOS vs CHoCH 核心区别

| | BOS | CHoCH |
|---|---|---|
| 含义 | 趋势延续确认 | 趋势反转的第一信号 |
| 发生位置 | 顺着当前趋势方向突破 | 逆着当前趋势方向突破 |
| 实战用法 | 顺势加仓/继续持有 | 警惕反转，准备换方向 |

### 内部结构 vs 外部结构（Internal vs External Structure）

外部结构（External）是你在 15m/1H 上看到的主要摆动高低点，决定大方向 bias。内部结构（Internal）是 5m 上在两个外部摆动点之间形成的小级别高低点，用来精确入场和出场。实战原则：**用外部结构定方向，用内部结构找入场**。当内部结构的 CHoCH 与外部结构方向一致时，就是高概率入场窗口。

### 5m 结构判断方向（实战）

打开 5m 图，从左到右连线标出明显的摆动高点（swing high）和摆动低点（swing low）。如果 HH + HL 持续出现 = 上升结构，做多 bias；如果 LH + LL 持续出现 = 下降结构，做空 bias。**结构不清晰时不做**——等一个清晰的 BOS 或 CHoCH 出来再说。

---

## 二、订单块（Order Block）

### 看涨 OB（Bullish Order Block）

一段下跌行情中最后一根下跌 K 线（或该区间的最后一组下跌 K 线），随后价格被强力推升并打破结构（BOS）。这根 K 线的范围（开盘到最低点）就是看涨 OB 区域。本质：机构在这个价位大量挂多单，价格回来时大概率再次被买起来。

### 看跌 OB（Bearish Order Block）

一段上涨行情中最后一根上涨 K 线，随后价格被强力打压并向下 BOS。这根 K 线的范围（开盘到最高点）就是看跌 OB 区域。价格回踩到这里时，机构的卖单会再次施压。

### 有效 OB 的条件

OB 必须被 **位移（Displacement）** 确认——也就是 OB 之后必须出现一组大实体 K 线（通常 2-3 根）强力脱离，并且造成 BOS。如果 OB 之后价格磨磨蹭蹭、没有明显位移，这个 OB 就是弱的，不值得做。另外，有效 OB 通常伴随一个 FVG（公允价值缺口），两者重叠的区域是入场黄金地带。

### OB 入场方式

1. 标记 OB 区域（那根关键 K 线的开盘价到极值）
2. 等价格回踩到 OB 区域
3. **不盲入**——进入 OB 区域后看反应：出现吞没 K、pin bar、delta 反转（ATAS 可观察）再入场
4. SL 放在 OB 区域外侧（看涨 OB 的 SL 在 OB 最低点下方）

### 突破块（Breaker Block）

原本的 OB 被价格打穿、失效了。失效后这个区域的角色翻转：原来的看涨 OB 变成看跌 Breaker，原来的看跌 OB 变成看涨 Breaker。价格回踩到 Breaker Block 时，它充当新方向的支撑/阻力。实战中 Breaker 往往出现在 CHoCH 之后——结构变了，原来的 OB 也跟着变角色。

### 缓解块（Mitigation Block）

类似 Breaker，但更具体：指的是之前造成过流动性扫除（sweep）的 OB。价格扫掉一侧流动性后强力反转，扫除起点处的 OB 就变成 Mitigation Block。机构在这个位置"缓解"了之前的仓位，价格再回来时阻力/支撑会更强。

### 实战过滤：哪些 OB 值得做

**做的**：
- OB 后有明显位移（大实体 K + FVG）
- OB 处于 Discount 区域（做多）或 Premium 区域（做空）
- OB 与 HTF（15m/1H）方向一致
- OB 内有未填补的 FVG

**不做的**：
- OB 后价格磨蹭、没有位移
- OB 已经被测试过一次（二次测试成功率大幅降低）
- OB 方向与 HTF bias 相反
- OB 在盘整区间中间（没有清晰结构）

---

## 三、公允价值缺口（FVG / Fair Value Gap）

### 定义

三根连续 K 线中，第一根 K 线的影线端与第三根 K 线的影线端之间留下的空白区域——也就是第二根 K 线的实体/影线覆盖范围之外、上下两根 K 线没有重叠的部分。这是价格被"不公平地"快速推过的区域，市场倾向于回来填补。

### 看涨 FVG（Bullish FVG）

出现在快速上涨中：第一根 K 线的最高点 < 第三根 K 线的最低点，两者之间的空间就是 bullish FVG。表明买方力量极强，价格回踩到这个区域时很可能再次被买起。

### 看跌 FVG（Bearish FVG）

出现在快速下跌中：第一根 K 线的最低点 > 第三根 K 线的最高点，两者之间的空间就是 bearish FVG。价格反弹到这个区域时卖压大概率再次出现。

### FVG 入场区域

价格回填 FVG 的 50% 到 100% 之间是理想入场区域。最激进的入场在 FVG 的边缘（刚碰到就进）；最保守的入场等价格完全填补 FVG 后看反应。实战中推荐在 FVG 50% 位附近设限价单，SL 放在 FVG 完全填补之后的位置。

### 相应侵入（Consequent Encroachment / CE）

FVG 的 50% 中线位置。价格触及 CE 位代表 FVG 被"公平"地回填了一半。CE 位本身就是一个精确的入场点——很多时候价格碰到 CE 位就反弹，不会完全填补整个 FVG。在图上标出 CE 位可以显著提高入场精度。

### 反转 FVG（Inversion FVG / IFVG）

FVG 被价格完全穿越后，角色翻转。原来的 bullish FVG 变成阻力（价格从下方回来测试时被压回去），原来的 bearish FVG 变成支撑。IFVG 的逻辑类似 Breaker Block：失效后角色对调。实战中当你看到一个 FVG 被打穿，不要删掉标记——它可能在反方向上继续有效。

### 实战：5m 图快速标记有效 FVG

1. 只标记伴随 BOS 的 FVG（没有造成结构突破的 FVG 大概率会被完全填补、失效）
2. 优先标记与 HTF bias 方向一致的 FVG
3. 如果 FVG 与 OB 重叠，该区域入场概率极高（双重确认）
4. GC 在 5m 上经常产生 FVG——只关注位移明显、实体大的那些；小 FVG 过滤掉

---

## 四、流动性（Liquidity）

### 买方流动性（Buy-side Liquidity / BSL）

堆积在摆动高点上方的止损单和突破买单。当价格扫过前高时，这些订单被触发，为机构提供对手盘（机构在这里卖出）。在图上看：任何明显的高点、尤其是被多次测试但没突破的高点上方，都有 BSL。

### 卖方流动性（Sell-side Liquidity / SSL）

堆积在摆动低点下方的止损单和突破卖单。价格扫过前低时这些单子被触发，机构在这里买入。前低、支撑位下方、equal lows 下方都是 SSL 密集区。

### 等高/等低（Equal Highs / Equal Lows）

两个或多个几乎相同价位的高点/低点。这些位置极其"诱人"——散户会在 EQH 上方挂突破买单、在 EQL 下方挂突破卖单。对机构来说，这就是一个清晰的流动性池，大概率会被扫掉。**看到 equal highs/lows，想的不是"支撑阻力"，而是"流动性目标"**。

### 扫流动性（Liquidity Sweep / Raid）

价格快速刺穿一个流动性池（前高/前低/EQH/EQL），触发堆积的止损单，然后迅速反转。这是 SMC 最核心的入场场景之一：扫完流动性 + 在 OB/FVG 区域出现反转信号 = 高概率交易。

### 与 Al Brooks "假突破"（Failed Breakout）的对应

Al Brooks 的 failed breakout（突破失败后反转）本质上就是 SMC 的 liquidity sweep。区别在于叙事方式不同：
- Al Brooks：价格试图突破但买方/卖方力量不够，突破失败
- SMC/ICT：机构故意推动价格突破来触发散户止损，获取流动性后反转

两者的入场时机、SL 位置、预期走势几乎一致。如果你已经理解 failed breakout，SMC 的 liquidity sweep 就是同一件事换了一个解释框架。

### 止损猎杀（Stop Hunt）识别

典型 stop hunt 特征：
1. 价格在明显的高/低点附近震荡（积累流动性）
2. 突然一根大 K 线刺穿高/低点
3. 刺穿后立刻出现反方向的大实体 K（位移）
4. 在 ATAS 上可以看到：刺穿瞬间 delta 巨变、aggressive 订单涌入反方向

### 实战：ATAS DOM 的流动性应用

在 ATAS 的 DOM（订单簿深度）上，你能直接看到挂单堆积的位置——那就是 SMC 说的 liquidity pool。关注：
- 某个价位突然出现大量 limit order 堆积 = 流动性池
- 价格接近该位置时 aggressive order 是否增加（准备扫）
- 扫完后 delta 是否急剧反转（确认 sweep 完成）

ATAS 提供了 SMC 理论缺少的微观确认——你不只是"猜"流动性在哪里，而是真的看到了。

---

## 五、溢价/折扣区域（Premium / Discount）

### 基本概念

取任意一段完整的摆动（swing high 到 swing low），用 Fibonacci 0.5（50%）一分为二：
- **上半部分 = 溢价区（Premium）**——价格偏贵
- **下半部分 = 折扣区（Discount）**——价格偏便宜

这是 SMC 中最简单但最有效的过滤器之一。

### 做多规则

只在 Discount 区域（50% 以下）寻找做多入场。价格在 Premium 区域给你看涨信号？忽略它——风险回报不划算。等它跌回 Discount 再说。

### 做空规则

只在 Premium 区域（50% 以上）寻找做空入场。价格在 Discount 区域给你看跌信号？不做——让价格涨到 Premium 再空。

### 最优交易入场点（Optimal Trade Entry / OTE）

Fibonacci 0.62 到 0.79 回撤区间。这是机构最常用的入场区域。当 OB 或 FVG 恰好落在 OTE 区间内时，该交易的概率显著提高。

实战操作：
1. 画出最近一段明显的摆动（从 swing high 到 swing low 或反过来）
2. 挂上 Fibonacci 回撤工具
3. 0.62-0.79 区间标出来
4. 看这个区间内是否有 OB 或 FVG——如果有，就是你的狙击区

---

## 六、时间框架与 Kill Zones（ICT 时段，北京时间）

### 亚盘 Kill Zone（Asian Session KZ）

- **时间**：06:00-09:00 BJT（对应纽约 18:00-21:00 前一天）
- **特点**：流动性最低，价格波动小，经常走出窄幅盘整区间
- **SMC 意义**：亚盘的高低点形成流动性池。伦敦/纽约开盘后大概率先扫亚盘的一侧流动性，然后走出真正方向。
- **实战**：不在亚盘做单，但必须标出亚盘高点（Asia High）和亚盘低点（Asia Low）——它们是后续 KZ 的 sweep 目标。

### 伦敦 Kill Zone（London Session KZ）

- **时间**：15:00-18:00 BJT（对应伦敦 08:00-11:00）
- **特点**：流动性剧增，通常确立当天的主要方向
- **SMC 意义**：伦敦开盘经常先扫亚盘一侧的流动性（Asia High 或 Asia Low），然后反转走出日内趋势。这个"扫完反转"就是经典的 London sweep 模型。
- **实战**：15:00-16:00 观察价格是否扫了亚盘高/低点。扫完后出现 CHoCH + OB/FVG = 高概率入场。

### 纽约 Kill Zone（New York Session KZ）

- **时间**：20:30-23:30 BJT（对应纽约 08:30-11:30）
- **特点**：GC 的主战场——黄金在纽约时段波动最大、流动性最充足
- **SMC 意义**：纽约可能延续伦敦的方向，也可能在扫掉伦敦的流动性后反转。重大经济数据（NFP、CPI、FOMC）都在纽约时段发布，会造成巨大的 displacement 和 FVG。
- **实战**：GC 日内 scalp 的最佳窗口。20:30-21:30 是核心交易时段，流动性和波动性最高。

### GC 黄金的最佳 SMC 入场 Kill Zone

**纽约 KZ（20:30-23:30 BJT）是 GC 的绝对主场。** 原因：
1. 黄金以美元计价，美盘经济数据对 GC 影响最直接
2. 此时段 CME（GC 的交易所）流动性最充足
3. 机构活跃度最高，SMC 模型的"机构行为"在此时段最清晰
4. ATAS 上的 DOM 和 delta 数据在此时段最有参考价值

其次是伦敦 KZ（15:00-18:00 BJT），尤其是伦敦扫亚盘流动性后的反转模型。

---

## 七、SMC 入场模型（实战 Checklist）

### 标准入场流程

```
Step 1 ─ HTF Bias（15m / 1H）
│  在 15m 或 1H 图上判断结构方向
│  HH+HL = 看涨 bias → 只找做多机会
│  LH+LL = 看跌 bias → 只找做空机会
│  结构不清 = 不做
│
Step 2 ─ 5m 结构确认
│  等 5m 出现与 HTF bias 一致的 CHoCH 或 BOS
│  CHoCH = 第一个反转信号（激进入场）
│  BOS = 确认信号（稳健入场）
│
Step 3 ─ 标记 POI（Point of Interest）
│  在 BOS/CHoCH 造成的位移脚下标出：
│  ├─ Order Block（最后一根反向 K 线）
│  ├─ FVG（三 K 缺口）
│  └─ 两者重叠区域 = 最高概率 POI
│
Step 4 ─ Premium / Discount 过滤
│  做多：POI 必须在 Discount 区域（< 50% fib）
│  做空：POI 必须在 Premium 区域（> 50% fib）
│  POI 在 OTE（0.62-0.79）= 最佳
│
Step 5 ─ ATAS 微观确认
│  价格到达 POI 后，切到 ATAS 观察：
│  ├─ Delta 反转（由负转正 = 看涨；由正转负 = 看跌）
│  ├─ Aggressive 买/卖单涌入反方向
│  ├─ DOM 上对手方挂单被吃掉
│  └─ 不需要所有信号都出现，2/3 即可
│
Step 6 ─ 入场 + 风控
│  入场：POI 区域 + ATAS 确认后市价入场
│  SL：OB 外侧（看涨 OB 最低点下方 / 看跌 OB 最高点上方）
│  TP：对侧流动性池（做多 TP = 前高/BSL；做空 TP = 前低/SSL）
│  R:R 目标 ≥ 2:1（达不到就不做）
```

### 快速决策矩阵

| 条件 | 满足 | 不满足 |
|---|---|---|
| HTF bias 清晰 | 继续 | 停，不做 |
| 5m CHoCH/BOS 确认 | 继续 | 等，不追 |
| POI 在正确的 Premium/Discount | 继续 | 跳过这个 POI |
| OB + FVG 重叠 | A+ 信号 | 单独 OB 或 FVG 也可 |
| ATAS delta 确认 | 入场 | 再等一会，或缩小仓位 |
| R:R >= 2:1 | 入场 | 不做 |

### 不做的场景

- HTF 结构不清晰（震荡市）
- 即将发布重大经济数据（等数据出来再说）
- 价格在 50% fib 附近（不在 Premium 也不在 Discount = 无优势区）
- Kill Zone 之外（流动性不足，假信号多）
- 连续亏损 2 笔后（执行停手纪律，不是市场问题是状态问题）

---

## 附录：SMC 与 Al Brooks Price Action 术语对照

| SMC / ICT 术语 | Al Brooks 对应概念 | 备注 |
|---|---|---|
| BOS（Break of Structure） | Breakout（突破） | SMC 更强调结构级别 |
| CHoCH（Change of Character） | Major Trend Reversal 初步信号 | CHoCH 类似 first pullback 反转 |
| Order Block | Signal Bar / Entry Bar 区域 | OB 更关注"区域"而非单根 K 线 |
| FVG（Fair Value Gap） | Gap / Measured Move 空间 | FVG 定义更精确 |
| Liquidity Sweep | Failed Breakout | 本质相同，叙事不同 |
| Premium/Discount | "High/Low of range"概念 | SMC 用 Fibonacci 量化 |
| Kill Zone | 交易时段偏好 | ICT 对时间更系统化 |
| Displacement | Strong Breakout / Climax | 大实体连续 K = 位移 |
| Mitigation | 二次测试 / Second Entry | 类似但 SMC 叙事不同 |

---

> **核心原则**：SMC 不是预测工具，是反应框架。等结构出来，等价格回到你的区域，等微观确认，然后执行。不追、不猜、不扛。
