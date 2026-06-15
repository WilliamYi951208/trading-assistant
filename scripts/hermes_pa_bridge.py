"""
hermes_pa_bridge.py — 独立桥接脚本
监听 latest-decision-pack.json 变化 → POST 给 Hermes gateway → 存分析结果

用法：python hermes_pa_bridge.py
不修改 webhook_receiver.py，不侵入现有流程。
"""

import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# === 配置 ===
DECISION_PACK_PATH = Path(r"G:\PriceAction\交易日志\latest-decision-pack.json")
SYSTEM_PROMPT_PATH = Path(__file__).parent / "hermes-pa-system.md"
OUTPUT_PATH = Path(r"G:\PriceAction\交易日志\latest-hermes-analysis.md")
LOG_PATH = Path(__file__).parent / "hermes-bridge.log"

HERMES_URL = "http://127.0.0.1:8642/v1/chat/completions"
HERMES_MODEL = "deepseek-v4-flash"
TIMEOUT_S = 30
POLL_INTERVAL_S = 2  # 轮询间隔


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def load_system_prompt():
    if SYSTEM_PROMPT_PATH.exists():
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    return "你是 GC 黄金期货 5m PA 分析助手。简洁给出 做/等/不做 建议。"


def build_user_message(pack):
    """把 decision-pack 转成给 Hermes 的 user message。"""
    bar = pack.get("latest_bar", {})
    seed = pack.get("analysis_seed", {})

    return f"""新 5m bar 来了，按 system prompt 给执行建议。

# 最新 K
- 时间: {bar.get('bar_time_bj')}
- 标的: {bar.get('exchange')}:{bar.get('symbol')} {bar.get('timeframe')}m
- OHLCV: O={bar.get('open')} H={bar.get('high')} L={bar.get('low')} C={bar.get('close')} V={bar.get('volume')}
- EMA20: {bar.get('ema20')}
- bar_index: {bar.get('bar_index')}

# 本地预分析（仅供参考，你可不采纳）
- bias: {seed.get('bias')}
- environment: {seed.get('environment')}
- bar_body_pct: {seed.get('body_pct')}
- ema_distance_points: {seed.get('ema_distance_points')}
- pa_read: {seed.get('pa_read')}
- suggestion_seed: {seed.get('suggestion_seed')}

直接按 system prompt 的 7 行格式输出，不要解释方法论。
"""


def call_hermes(system_prompt, user_message):
    """同步调用 Hermes gateway。返回 assistant content 或 None。"""
    body = json.dumps({
        "model": HERMES_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": 400,
        "temperature": 0.3,
    }).encode("utf-8")

    req = urllib.request.Request(
        HERMES_URL,
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            resp = json.loads(r.read().decode("utf-8"))
            return resp["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace")[:300]
        log(f"HTTP {e.code} from Hermes: {body_txt}")
        return None
    except Exception as e:
        log(f"call_hermes failed: {type(e).__name__}: {e}")
        return None


def write_analysis(pack, analysis):
    bar = pack.get("latest_bar", {})
    seed = pack.get("analysis_seed", {})
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = f"""# Hermes PA 分析

> 生成时间：{ts}
> Bar：{bar.get('bar_time_bj')} | C {bar.get('close')} | EMA20 {bar.get('ema20')}
> 本地 seed：{seed.get('suggestion_seed')}

---

{analysis}
"""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(md, encoding="utf-8")
    log(f"wrote {OUTPUT_PATH.name}")


def process_pack(pack):
    """处理一份 decision-pack。"""
    if not pack.get("session_active"):
        log("session_active=false，跳过")
        return

    bar_id = pack.get("latest_bar", {}).get("identity")
    log(f"new bar identity={bar_id}, calling Hermes…")

    sys_prompt = load_system_prompt()
    user_msg = build_user_message(pack)
    t0 = time.time()
    analysis = call_hermes(sys_prompt, user_msg)
    dt = time.time() - t0

    if analysis:
        log(f"Hermes 返回 {len(analysis)} 字符，耗时 {dt:.1f}s")
        write_analysis(pack, analysis)
    else:
        log("Hermes 调用失败，未写文件")


def watch_loop():
    """轮询 decision-pack.json，按 created_at 去重。"""
    log(f"启动桥接，监听 {DECISION_PACK_PATH}")
    log(f"Hermes URL: {HERMES_URL}, model: {HERMES_MODEL}")

    last_seen = None
    while True:
        try:
            if not DECISION_PACK_PATH.exists():
                time.sleep(POLL_INTERVAL_S)
                continue

            pack = json.loads(DECISION_PACK_PATH.read_text(encoding="utf-8"))
            created_at = pack.get("created_at")

            if created_at and created_at != last_seen:
                last_seen = created_at
                process_pack(pack)
        except json.JSONDecodeError:
            # 文件正在被写入（atomic_write 之间），跳过
            pass
        except KeyboardInterrupt:
            log("收到 Ctrl+C，退出")
            return
        except Exception as e:
            log(f"循环异常: {type(e).__name__}: {e}")

        time.sleep(POLL_INTERVAL_S)


def main():
    if "--once" in sys.argv:
        # 单次跑一遍当前 pack
        if not DECISION_PACK_PATH.exists():
            log(f"找不到 {DECISION_PACK_PATH}")
            return 1
        pack = json.loads(DECISION_PACK_PATH.read_text(encoding="utf-8"))
        process_pack(pack)
        return 0
    watch_loop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
