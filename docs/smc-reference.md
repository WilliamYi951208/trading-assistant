# SMC 参考（用户体系版）

> 基于 **Trading Hub 3.0**（Mr. Khan, 2023），用户实际使用的 SMC 框架
> 整理时间：2026-05-20
> 用途：明天起看盘时给用户做信息佐证用，**不审用户判断，只做客观对照**

---

## 0. 用户实际使用的 SMC 子集（最重要）

**用户不用全套 TH 3.0 流程**，只用以下 4 个核心概念：

| 概念 | 用途 | 优先级 |
|------|------|--------|
| **S&D（Supply & Demand）** | 找入场区域 | ★★★★★ |
| **PD（Premium / Discount）** | 判断当前价格在 swing range 的位置 | ★★★★ |
| **BOS（Break of Structure）** | 确认趋势延续 | ★★★★★ |
| **Liquidity（流动性扫单）** | 判断扫完后是反转还是延续 | ★★★★★ |

**用户的核心交易逻辑**：
```
价格到达流动性区域 → 扫过止损 → 判断反转 or 延续
  反转 → 在 S&D zone 入场做反方向
  延续 → BOS 确认后跟随
```

**助手佐证重点**：
- 流动性在哪（前高/前低/EQH/EQL/趋势线 — 用 5m 数据标注）
- 扫完后 5m 收盘是否确认方向（收盘回区间内 = 反转 / 站稳 = BOS）
- S&D zone 对应的 VP 位置（HVN/POC/VAH/VAL）
- Premium/Discount 计算（swing range 的 50% 分界线）

---

## 1. 核心理念

SMC 的核心：**Identify Liquidity or Become Liquidity**（识别流动性，或成为流动性）

机构（OTF）和散户的对立游戏：
- 散户在 **明显的支撑阻力/趋势线/前高前低** 设止损 → 这些区域积累了流动性
- 机构会先制造"假动作"扫止损 → 收集流动性 → 再向真实方向运行
- SMC 交易者的工作：站在机构一边，**等流动性被扫后再入场**

---

## 2. 关键词缩写表（按 TH 3.0 完整列出）

| 缩写 | 全称 | 中文 |
|------|------|------|
| **SMC** | Smart Money Concept | 聪明钱概念 |
| **SMT** | Smart Money Trap | 聪明钱陷阱 |
| **BOS** | Break Of Structure | 结构突破（顺势确认） |
| **CHoCH** | Change of Character | 性格转变（趋势反转确认） |
| **IDM** | Inducement | 诱导（小流动性，机构入场前的扫单） |
| **OB** | Order Block | 订单块 |
| **OF** | Order Flow | 订单流（注意：用户体系里不看 footprint/delta，只看 candle 级别的 OF） |
| **POI** | Point Of Interest | 关注点（OB / Imbalance 等） |
| **FVG** | Fair Value Gap | 公允价值缺口（= Imbalance） |
| **IPA** | Inefficient Price Action | 低效价格行为 |
| **IFC** | Institutional Funding Candle | 机构资金 K 线 |
| **AOI** | Area Of Interest | 关注区域 |
| **HTF** | Higher Time Frame | 大时间框架 |
| **LTF** | Lower Time Frame | 小时间框架 |
| **EQH** | Equal High | 等高 |
| **EQL** | Equal Low | 等低 |
| **S&D** | Supply & Demand | 供需 |
| **DOS** | Demand To Supply | 需求转供给 |
| **SOD** | Supply To Demand | 供给转需求 |
| **ERL** | Engineering Liquidity | 工程化流动性 |
| **BSL** | Buy Side Liquidity | 买方流动性（前高上方/EQH 上方）|
| **SSL** | Sell Side Liquidity | 卖方流动性（前低下方/EQL 下方）|
| **TL** | Trendline | 趋势线 |
| **PDH/PDL** | Previous Day High/Low | 前日高/低 |
| **PWH/PWL** | Previous Week High/Low | 前周高/低 |
| **HOD/LOD** | High/Low Of Day | 日内高/低 |
| **SOS/SOW** | Sign Of Strength/Weakness | 强势/弱势信号 |
| **LQD** | Liquidity | 流动性 |

---

## 3. Impulse & Correction（推动 vs 修正）

**核心区别**：

| 维度 | Impulse Move（推动腿） | Corrective Move（修正腿） |
|------|----------------------|------------------------|
| 速度 | 快 | 慢 |
| 走势 | 直接、单向 | 重叠、犹豫 |
| K 线 | 大实体、少影线 | 小实体、多影线、内包多 |
| 视觉 | 一条清晰的腿 | 锯齿状 / 横盘 |

**SMC 交易者只在 Corrective Move 里找入场**，因为：
- Impulse 是机构已经动手了，追进去风险大
- Correction 是机构暂停、给散户挂止损的时间
- 等 Correction 结束、新的 Impulse 开始 → 跟上

**Valid Pullback Identification**：
- 必须看到 **Sweep**（扫过前一个高/低点）
- 或 **Engulfing**（吞没前一根反向 K）
- 没有 sweep / engulfing 的回撤 = **invalid**，不入场

---

## 4. 结构（Structure Mapping）

**Bullish Structure**（上升结构）：
- HH（Higher High，更高的高点）
- HL（Higher Low，更高的低点）
- 持续 HH-HL 序列 = 多头趋势

**Bearish Structure**（下降结构）：
- LH（Lower High）
- LL（Lower Low）
- 持续 LH-LL 序列 = 空头趋势

### BOS（Break of Structure）

**多头 BOS**：价格创新高，**收盘高于前一个 HH** → 趋势延续
**空头 BOS**：价格创新低，**收盘低于前一个 LL** → 趋势延续

**关键**：必须用 **收盘价**确认，不是影线。

### CHoCH（Change of Character）

**多头转空头**：在上升结构中，**收盘跌破最近一个 HL** → 趋势可能反转
**空头转多头**：在下降结构中，**收盘突破最近一个 LH** → 趋势可能反转

**CHoCH 是反转信号的第一步，但不是入场信号**。需要等：
1. CHoCH 形成
2. 新方向的第一次 BOS 确认
3. 找到对应的 OB / Imbalance 做回撤入场

### Valid / Invalid BOS 和 CHoCH

✅ **Valid**：完整 K 线收盘穿越关键位
❌ **Invalid**：只有影线扫过，收盘没站稳 = **Sweep / Liquidity Grab**

---

## 5. Order Block（OB）

**定义**：导致价格反转或突破的最后一根**反向 K 线**。

**Bearish OB**（看跌 OB）：
- 在上涨的最高点之前，**最后一根阳线**
- 价格回测这根阳线 → 大概率反转向下

**Bullish OB**（看涨 OB）：
- 在下跌的最低点之前，**最后一根阴线**
- 价格回测这根阴线 → 大概率反转向上

**OB 识别要点**：
1. OB 必须出现在 **Sweep / Liquidity Grab** 之后
2. OB 形成后**必须有 BOS / CHoCH 确认**
3. OB 没被 mitigate 之前都有效（**Fresh OB**）
4. OB 已被回测过 = **Mitigated OB**（强度降低）

**入场逻辑**：
- 价格回到 OB 区域
- 在 OB 的 50% 或 OB 高/低点入场
- SL 放在 OB 之外（结构性止损）

---

## 6. Imbalance / FVG（公允价值缺口）

**定义**：3 根连续 K 线中，第 1 根的影线和第 3 根的影线**不重叠**形成的空白区域。

```
[K1]  影线高点
                 ← 空白区域 = Imbalance / FVG
[K3]  影线低点
```

**类型**：
- **Bullish Imbalance**：上涨方向留下的空白，**支撑作用**
- **Bearish Imbalance**：下跌方向留下的空白，**阻力作用**

**关键认知**：
- 价格倾向于**回头填补**这些 imbalance
- 但**不一定每次都填满** —— 主要看在哪种结构里
- 填补 imbalance 后，**如果有 OB 在附近，OB 的强度增加**

**用法**：
- 用 imbalance 找 POI 入场点
- 用 imbalance 作为 TP（价格回到 imbalance 边缘部分平仓）

---

## 7. Order Flow（K 线级别）

**注意**：用户体系里这个 OF 不是 footprint/delta 的 OF，而是 **K 线层面观察资金流向**。

**Order Flow 解读**：
- 观察每一根 K 的实体大小、收盘位置、相对前一根的关系
- **Bullish OF**：连续阳线 + 实体扩大 + 高点抬高
- **Bearish OF**：连续阴线 + 实体扩大 + 低点降低
- **OF 反转信号**：突然出现反向大实体 K + 吞没前一根 + 量能放大

---

## 8. IFC（Institutional Funding Candle，机构资金 K 线）

**定义**：导致主要 BOS / CHoCH 的**那根触发 K 线**。

**特征**：
- 实体大、几乎无影线
- 一次性穿透关键位
- 量能显著（在 VP 上对应 LVN / imbalance）
- 这根 K **必然是机构的入场点**

**用法**：
- IFC 之后的回撤是高概率入场
- IFC 本身就是一个 POI

---

## 9. Liquidity（流动性）

### 9.1 Retail Liquidity（散户流动性）

散户常见挂止损的位置：
- **Support / Resistance** 上下
- **Trendline 突破点**
- **Pattern**（头肩、双顶双底等）的颈线
- **EQH / EQL**（等高/等低）—— 这是 SMC 最重要的流动性类型
- **Round Number**（整数关口）

**EQH / EQL 的重要性**：
- 价格在某个高点附近形成两个或多个**几乎相等的高点** → EQH
- 散户认为这是阻力会做空、设止损在 EQH 上方
- 机构会扫过 EQH 收割止损，再向真实方向运行
- **EQH 上方 = BSL（买方流动性，等待被扫）**
- **EQL 下方 = SSL（卖方流动性，等待被扫）**

### 9.2 Trendline & Breakout Liquidity

- 趋势线突破时，跟单的散户会在突破点上方挂买单/下方挂卖单
- 机构会反向把这个突破做成 **Fake Breakout**
- 跟随趋势线突破的散户被止损 → 机构反向获利

### 9.3 Session Liquidity（节段流动性）

**核心**：每个交易时段有其自己的高低点，作为流动性目标。

主要节段（亚盘 / 伦敦 / 纽约）：
- **Asia Session High / Low**
- **London Session High / Low**
- **NY Session High / Low**

**典型套路**：
- 亚盘形成 Range（高低点）
- 伦敦开盘后扫亚盘高/低（**Sweep**）
- 扫完后 CHoCH → 反向运行

### 9.4 Daily Candle Liquidity

每根日线的高点/低点是**第二天**的流动性目标：
- **PDH（前日高）** → 第二天会被测试，扫过后可能反转
- **PDL（前日低）** → 同上

**重要**：日线级别的 sweep 比小级别 sweep 信号更强。

---

## 10. Smart Money Trap（聪明钱陷阱）

**定义**：基于明显结构和 OB 做单的散户被反向收割。

**典型场景**：
- 散户看到 OB 形成 + BOS 确认 → 在 OB 回测时入场
- 但**机构故意制造 Inducement（IDM）** → 价格突破 OB 后假反转
- 散户止损被扫 → 机构真正方向才开始

**避免方法**：
- **等 Inducement Confirmation** 出现后再入场
- **等 Sweep + Order Block Confirmation** 双重信号
- 不在第一次 OB 回测就重仓

---

## 11. POI（Point of Interest，关注点）识别

**高概率 POI 的特征**：

1. **位于 Liquidity Sweep 之后**（机构已经"加油"）
2. **配合 Imbalance**（FVG 在附近）
3. **HTF 和 LTF 对齐**（不同级别都指向同一区域）
4. **Fresh / 未被 mitigate**
5. **靠近关键水平位**（PDH/PDL/Round Number/VPOC）

**POI 类型优先级（用户体系）**：
- ★★★★★ Sweep + S&D zone + 处于 Discount/Premium 区
- ★★★★ Sweep + BOS 确认 + S&D zone
- ★★★ 单独 S&D zone（未被回测过）
- ★★ 单独 Liquidity 区域（无 zone 配合）
- ★ 普通 S&R 水平位

---

## 11.5 Premium / Discount（PD 概念）⭐

**核心**：把一个 swing range（从一个 swing low 到 swing high）分成两半。

```
                    Swing High
  ┌──────────────────┐  ← 高点
  │   Premium Zone   │  ← 上半部分（50%-100%）
  │   （只做空）      │
  ├──────────────────┤  ← 50% Equilibrium（均衡线）
  │   Discount Zone  │  ← 下半部分（0%-50%）
  │   （只做多）      │
  └──────────────────┘  ← 低点
                    Swing Low
```

**规则**：
- **多头趋势中**：只在 **Discount zone**（下半部分）做多。在 Premium 区做多 = 高位追多 = 坏交易
- **空头趋势中**：只在 **Premium zone**（上半部分）做空。在 Discount 区做空 = 低位追空 = 坏交易
- **50% 均衡线**：是两个区域的分界，也叫 EQ（Equilibrium）

**实战要点**：
- swing range 必须是**当前结构下的有效 swing**
- 不是随便挑两个点，要是 BOS 确认后的最后一个完整 leg
- 当 swing range 改变（新的 BOS 形成新高/新低），PD 重新计算

**示例**：
```
GC 今日 swing low 4467（夜盘底）→ swing high 4510.4（今晨高）
swing range = 43.4 点
50% 均衡线 = 4488.7
  - 4488.7 以上 = Premium → 只考虑做空
  - 4488.7 以下 = Discount → 只考虑做多
```

**助手能做的佐证**：
- 实时算出当前 swing range 和 50% 均衡线
- 提示用户"现价在 Premium / Discount / 均衡线附近"
- 当 swing 改变时提示用户"PD 需要重新计算"

---

## 12. Multiple Time Frame（多时间框架）分析

**用户体系的 MTF 组合**：

| 市场 | HTF | LTF |
|------|-----|-----|
| **Forex** | M15 | M1 |
| **Crypto** | M15 | M1 |
| **Stock / Indices** | M15 + PDH/PDL | M5 |

**操作流程**：
1. **HTF 找方向**：看 M15 的结构是 Bullish 还是 Bearish
2. **HTF 找 POI**：在 M15 上标出 OB / Imbalance / Liquidity
3. **价格进入 POI**：切到 LTF（M1 或 M5）
4. **LTF 找确认**：等 CHoCH 或 BOS 出现
5. **LTF 入场**：在 LTF 的 OB / Imbalance 内入场

**风险控制**：
- HTF 决定方向 → 错了 SL 也只在 HTF 结构外
- LTF 决定时机 → SL 紧、风险小

---

## 13. Entry Types（入场类型）

### 13.1 CHoCH with IDM Entry Module

**完整流程**：
1. HTF 上看到趋势反转的初步信号（CHoCH 形成）
2. LTF 上 CHoCH 出现 + **IDM（小诱导）**
3. **等 IDM 被扫后**才入场
4. 入场点：IDM 扫单后的 OB / Imbalance 内
5. SL：IDM 高/低点之外

### 13.2 CHoCH without IDM Entry Module

**适用场景**：没有明显 IDM 的情况

1. HTF CHoCH 形成
2. LTF 直接在 CHoCH 后的 OB 回测时入场
3. SL：CHoCH 触发点之外
4. **信心等级低于 13.1**

### 13.3 FLIP with IDM Entry Module

**FLIP**：Supply 翻转成 Demand（或反之）

1. 原本的供给区被突破并转为需求区
2. 价格回测这个**已 flipped** 的区域
3. 等 IDM 扫单 + 入场

### 13.4 FLIP without IDM Entry Module

类似 13.2 + 13.3 的结合，没有 IDM 直接入场。

### 13.5 Single Candle Mitigation Entry

**最高级也最难的入场**：

- 只有**一根 K 线**触及 OB 就立即反转
- 不给二次回测机会
- 适合**强趋势行情**
- 必须有 HTF 的强烈方向支持
- SL 放在那根 K 线之外

### 13.6 Ping Pong Entries

**适用场景**：HTF 范围内的来回波动

- 在 Range 上沿（Supply）做空，下沿（Demand）做多
- 来回打几次，直到 Range 突破
- 每次入场都要看 LTF 确认

### 13.7 Multiple Scale Entries

**多周期叠加入场**：

- 在 H1 / M15 / M5 都有 POI 对齐时分批入场
- 第一笔轻仓试探
- 后续按结构确认加仓
- **注意**：用户在 PRO 阶段**禁止加仓**，这条只作概念了解

---

## 14. Risk Management（TH 3.0 章节摘录）

**用户体系**：

| 项 | TH 3.0 建议 | 用户当前规则（更严） |
|----|------------|---------------------|
| 单笔风险 | 1-2% | TPT 3 点 ≈ $300（约 0.3%） |
| 盈亏比 | 1:3 起步 | 1:3 以上优先 |
| 每日交易数 | 1-3 笔 | TPT 每天 ≤ 2 笔 |
| 连亏后行动 | 暂停 | 当日 -$500 浮亏停手 |

---

## 15. 实战 Checklist（用户每笔交易可参考）

入场前自检：

- [ ] HTF 结构是什么？BOS 还是 CHoCH？
- [ ] 我入场的 POI 是什么？（OB / Imbalance / S&D）
- [ ] POI 是 Fresh 还是 Mitigated？
- [ ] POI 之前有没有 Sweep？（扫过哪个 Liquidity）
- [ ] LTF 上有 CHoCH / BOS 确认吗？
- [ ] IDM 有没有出现？（如果有，已经被扫了吗？）
- [ ] SL 放在哪个结构外？（必须结构性止损）
- [ ] TP1 在哪个 Liquidity / Imbalance？
- [ ] 盈亏比是否 ≥ 1:2？

---

## 16. 与 PA / VP 的对照关系（给助手用）

| SMC 概念 | PA（Brooks）对应 | VP 对应 |
|---------|-----------------|---------|
| **BOS** | 突破棒 / Higher High 形成 | 突破 VAH/VAL |
| **CHoCH** | 趋势反转信号（首个反向 swing） | POC 转移 |
| **Order Block** | 反转棒（Reversal Bar） | HVN（高成交量节点） |
| **Imbalance / FVG** | 趋势棒留下的 Gap | LVN（低成交量节点） |
| **EQH / EQL** | 双顶 / 双底 | VAH / VAL 上下 |
| **Liquidity Sweep** | 假突破 / Stop Hunt | POC 扫单 |
| **IDM** | 小尾巴扫止损 | 单根 LVN 穿透 |
| **POI** | 关键位 + 信号棒位置 | HVN 边缘 |
| **Mitigation** | 二次入场 | POC 回测 |

**用助手时**：
- 用户说"M15 出 CHoCH" → 我可以补"5m 上对应的是趋势棒+反转吞没"
- 用户说"等 OB 回测" → 我补"该 OB 位置在 VP 上是 HVN，强度可信"
- 用户说"扫了 EQH" → 我补"PA 上是 ii 突破假阳线" 或 "VP 上是 LVN 快穿"

---

## 17. 我（助手）的边界

- ✅ 给用户 SMC 概念**对应位置**的描述（用 5m PA 视角和 VP 视角佐证）
- ✅ 当用户说出明确 SMC 术语时**确认理解**（"你说的是 OB 还是 OF？"）
- ✅ 提示 SMC 与 PA/VP 的**冲突点**（"SMC 说 sweep 完应反转，但 PA 上量能不支撑"）
- ❌ **不评判**用户的 SMC 判断对错（我只看 5m，不是 LTF 实时）
- ❌ **不主动**给 SMC 入场建议（用户体系比我深）
- ❌ **不要求**用户解释每个 SMC 信号（影响 scalp 速度）
