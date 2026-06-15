# Legacy / 归档版本

这里存放**旧版 Skill**，已不是默认使用的版本，仅作参考与回退保留。

| 文件 | 是什么 | 与当前版的区别 |
|------|--------|----------------|
| `SKILL.md` | `price-action-assistant` 旧版 | **纯 Al Brooks 价格行为**，不含 SMC / Order Flow / Volume Profile |
| `SKILL-LITE.md` | 上面那版的轻量版 | 纯 MCP 模式，不依赖本地 webhook 接收器 |

> 当前默认版是仓库根目录的 [`skill/SKILL.md`](../../skill/SKILL.md)（`交易助手 v3.1.0`，四套体系完整版）。

## 想改用旧版怎么办？

旧版只是一个 `SKILL.md`，安装/切换就是「**把哪一份 SKILL.md 放进 skill 目录**」的区别。

**方案一：临时试用（不动仓库）**

直接把旧版拷进你的 Agent skills 目录，覆盖默认安装：

```bash
# 纯 PA 完整版
cp docs/legacy/SKILL.md ~/.claude/skills/trading-assistant/SKILL.md

# 或纯 PA 轻量版（无需本地服务器）
cp docs/legacy/SKILL-LITE.md ~/.claude/skills/trading-assistant/SKILL.md
```

> 注意目标文件名要统一成 `SKILL.md`，Agent 只认这个名字。

**方案二：作为本仓库的默认版（替换 skill/）**

如果你想让本仓库默认就用旧版：

```bash
# 备份当前四体系版
cp skill/SKILL.md skill/SKILL.full.md.bak

# 用旧版覆盖
cp docs/legacy/SKILL.md skill/SKILL.md
```

之后照 README 的「安装 Skill」步骤把 `skill/` 拷到 Agent 目录即可。想换回来就用备份覆盖，或 `git checkout skill/SKILL.md` 还原。

**轻量版 vs 完整版怎么选？**

- **完整版**（`SKILL.md`）：配合本地 `webhook_receiver.py` / ATAS 自动取数，每根新 K 自动分析。
- **轻量版**（`SKILL-LITE.md`）：纯 MCP 拉取，不跑本地服务器，适合只想随手问盘、贴截图分析的场景。
