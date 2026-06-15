from http.server import BaseHTTPRequestHandler, HTTPServer
try:
    from http.server import ThreadingHTTPServer
except ImportError:
    from socketserver import ThreadingMixIn
    class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
        daemon_threads = True
import json
import re
import os
import tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta
# 注：原使用 zoneinfo.ZoneInfo("Asia/Shanghai")，但 Windows uv python 缺 tzdata 包会抛 ZoneInfoNotFoundError
# 改用固定偏移 +08:00，效果等价（中国不实行夏令时）
BJT = timezone(timedelta(hours=8))
from urllib.parse import urlparse


# 加载配置
CONFIG_PATH = Path(__file__).parent / "config.json"
def load_config():
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "output_dir": "G:\\PriceAction\\交易日志",
        "webhook_data_dir": "webhook-data",
        "log_prefix": "trade-log",
        "webhook_secret": "",
        "host": "127.0.0.1",
        "port": 8787
    }

CONFIG = load_config()
OUTPUT_DIR = Path(CONFIG["output_dir"])
HOST = CONFIG.get("host", "127.0.0.1")
PORT = CONFIG.get("port", 8787)
WEBHOOK_SECRET = CONFIG.get("webhook_secret", "")

# 本地缓存目录（接收器内部使用）
DATA_DIR = Path(CONFIG.get("webhook_data_dir", "webhook-data"))
LATEST_PATH = DATA_DIR / "latest-bars.json"

# 统一输出目录（所有 agent 读取）
BARS_DIR = OUTPUT_DIR / "bars"
HISTORY_PATH = BARS_DIR / f"bars-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
RECENT_BARS_PATH = BARS_DIR / "recent-20-bars.json"
DECISION_PACK_PATH = OUTPUT_DIR / "latest-decision-pack.json"
CODEX_BRIEF_PATH = OUTPUT_DIR / "latest-codex-brief.md"
SESSION_CONTEXT_PATH = OUTPUT_DIR / "session-context.json"
SESSION_STATE_PATH = OUTPUT_DIR / "session-state.json"
NOTIFICATION_PATH = OUTPUT_DIR / "new-bar-notification.txt"


DEFAULT_SESSION_CONTEXT = {
    "instrument": "GC futures scalp",
    "primary_timeframe": "5m",
    "mode": "manual_execution_only",
    "methodology": "price_action",
    "methodology_note": "当前使用 Al Brooks Price Action 方法论，后续可扩展 SMC 等其他方法",
    "accounts": [
        {
            "name": "TakeProfitTrader / TPT",
            "stage": "PRO",
            "bias": "protect account, build buffer first",
            "default_size": "0-1 GC contract",
            "risk_note": "Intraday trailing drawdown is the main danger; do not use TPT PRO for catch-up trades.",
        },
        {
            "name": "Alpha Futures",
            "stage": "Qualified/Pro target",
            "bias": "protect account and work toward payout days/profit pool",
            "default_size": "1 GC contract",
            "risk_note": "Qualified stage should focus on $200+ winning days and controlled drawdown.",
        },
    ],
    "execution_rules": [
        "User executes all orders manually; never auto-order.",
        "Default recommendation is no trade unless edge is clear.",
        "GC default size is 1 contract; 2 contracts only for A+ clean trend structure after user confirmation.",
        "During an active discussion, do not add noisy automation commentary unless a new 5m bar changes the plan.",
        "Every trade suggestion must include do/wait, direction, entry/trigger, invalidation/stop, TP, and size.",
    ],
    "output_must_include": [
        "建议点位（入场/触发）",
        "止盈（TP）",
        "止损（失效点）",
        "手数",
        "原因（一句话）",
    ],
}


def atomic_write_json(path, data):
    """原子性写入 JSON 文件"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
        dir=path.parent,
        suffix=".tmp"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        temp_path = f.name
    os.replace(temp_path, path)


def atomic_write_text(path, text):
    """原子性写入文本文件"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
        dir=path.parent,
        suffix=".tmp"
    ) as f:
        f.write(text)
        temp_path = f.name
    os.replace(temp_path, path)


def load_session_state():
    """加载会话状态（开始/停止控制）"""
    if not SESSION_STATE_PATH.exists():
        default_state = {
            "active": False,
            "started_at": None,
            "stopped_at": None,
        }
        atomic_write_json(SESSION_STATE_PATH, default_state)
        return default_state
    try:
        return json.loads(SESSION_STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"active": False, "started_at": None, "stopped_at": None}


def set_session_state(active):
    """设置会话状态"""
    state = load_session_state()
    state["active"] = active
    if active:
        state["started_at"] = datetime.now(timezone.utc).isoformat()
        state["stopped_at"] = None
    else:
        state["stopped_at"] = datetime.now(timezone.utc).isoformat()
    atomic_write_json(SESSION_STATE_PATH, state)
    return state


def load_session_context():
    if not SESSION_CONTEXT_PATH.exists():
        atomic_write_json(SESSION_CONTEXT_PATH, DEFAULT_SESSION_CONTEXT)
        return DEFAULT_SESSION_CONTEXT
    try:
        return json.loads(SESSION_CONTEXT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_SESSION_CONTEXT


def parse_tradingview_fallback(raw):
    payload = {"raw": raw}
    string_fields = ["symbol", "exchange", "timeframe", "note"]
    number_fields = [
        "time",
        "time_close",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "ema20",
        "bar_index",
    ]

    for field in string_fields:
        match = re.search(rf'"{field}"\s*:\s*"([^"]*)"', raw)
        if match:
            payload[field] = match.group(1)

    for field in number_fields:
        match = re.search(rf'"{field}"\s*:\s*(-?\d+(?:\.\d+)?)', raw)
        if match:
            value = match.group(1)
            payload[field] = float(value) if "." in value else int(value)

    payload["parse_warning"] = "fallback_parser_used"
    return payload


def normalize_payload(payload):
    if isinstance(payload, dict) and set(payload.keys()) == {"raw"}:
        return parse_tradingview_fallback(payload["raw"])
    return payload


def bar_identity(payload):
    for key in ("time_close", "bar_index", "received_at"):
        value = payload.get(key)
        if value is not None:
            return str(value)
    return ""


def timestamp_to_bj(value):
    """转换时间戳为北京时间"""
    if value is None:
        return ""
    if isinstance(value, str) and not value.isdigit():
        return value
    try:
        timestamp = float(value)
        if timestamp > 10_000_000_000:
            timestamp = timestamp / 1000
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc).astimezone(BJT)
        return dt.strftime("%H:%M")
    except (TypeError, ValueError, OSError):
        return str(value)


def format_bar_time(payload):
    start = timestamp_to_bj(payload.get("time"))
    end = timestamp_to_bj(payload.get("time_close"))
    if start and end:
        return f"{start}-{end} 北京时间"
    return start or end or ""


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_today_history_path():
    """获取当天的 bars 历史文件路径"""
    return BARS_DIR / f"bars-{datetime.now(BJT).strftime('%Y-%m-%d')}.jsonl"


def read_recent_bars(limit=20):
    """从环形缓冲读取最近 N 根 K 线"""
    if RECENT_BARS_PATH.exists():
        try:
            bars_data = json.loads(RECENT_BARS_PATH.read_text(encoding="utf-8"))
            if isinstance(bars_data, list):
                return bars_data[-limit:]
        except json.JSONDecodeError:
            pass
    history_path = get_today_history_path()
    if not history_path.exists():
        return []
    lines = history_path.read_text(encoding="utf-8").splitlines()[-limit:]
    bars = []
    for line in lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = normalize_payload(record.get("payload", {}))
        if isinstance(payload, dict):
            payload["received_at"] = record.get("received_at")
            bars.append(payload)
    return bars


def update_recent_bars_cache(new_bar, limit=20):
    """更新环形缓冲"""
    bars = read_recent_bars(limit)
    if not bars or bar_identity(bars[-1]) != bar_identity(new_bar):
        bars.append(new_bar)
    bars = bars[-limit:]
    atomic_write_json(RECENT_BARS_PATH, bars)


def analyze_bars(bars):
    if not bars:
        return {
            "bias": "unknown",
            "environment": "no bar history",
            "pa_read": "等待更多 5m K 线。",
            "suggestion_seed": "不做/等",
        }

    latest = bars[-1]
    closes = [safe_float(bar.get("close")) for bar in bars]
    closes = [value for value in closes if value is not None]
    highs = [safe_float(bar.get("high")) for bar in bars]
    highs = [value for value in highs if value is not None]
    lows = [safe_float(bar.get("low")) for bar in bars]
    lows = [value for value in lows if value is not None]

    close = safe_float(latest.get("close"))
    open_ = safe_float(latest.get("open"))
    high = safe_float(latest.get("high"))
    low = safe_float(latest.get("low"))
    ema20 = safe_float(latest.get("ema20"))

    body = abs(close - open_) if close is not None and open_ is not None else None
    bar_range = high - low if high is not None and low is not None else None
    body_pct = body / bar_range if body is not None and bar_range and bar_range > 0 else None
    ema_distance = close - ema20 if close is not None and ema20 is not None else None

    recent_close_delta = closes[-1] - closes[-6] if len(closes) >= 6 else 0
    lower_highs = len(highs) >= 4 and highs[-1] <= highs[-2] <= highs[-3]
    lower_lows = len(lows) >= 4 and lows[-1] <= lows[-2] <= lows[-3]
    higher_highs = len(highs) >= 4 and highs[-1] >= highs[-2] >= highs[-3]
    higher_lows = len(lows) >= 4 and lows[-1] >= lows[-2] >= lows[-3]

    if ema_distance is not None and close is not None and recent_close_delta < 0 and close < ema20:
        bias = "short"
        environment = "5m bearish / below EMA20"
    elif ema_distance is not None and close is not None and recent_close_delta > 0 and close > ema20:
        bias = "long"
        environment = "5m bullish / above EMA20"
    else:
        bias = "neutral"
        environment = "mixed or transition"

    if lower_highs and lower_lows:
        environment += " / lower highs and lower lows"
    if higher_highs and higher_lows:
        environment += " / higher highs and higher lows"

    direction_word = "阳线" if close is not None and open_ is not None and close > open_ else "阴线"
    strength = "趋势棒" if body_pct is not None and body_pct >= 0.65 else "小实体/震荡棒"
    ema_text = ""
    if ema_distance is not None:
        ema_text = f"，收盘距 EMA20 {ema_distance:+.1f} 点"
    pa_read = f"{direction_word}{strength}{ema_text}；环境：{environment}。"

    if bias == "short":
        suggestion_seed = "优先等反抽失败空；低位急跌后不追空。"
    elif bias == "long":
        suggestion_seed = "优先等回调守住 EMA/前低后多；高位急拉后不追多。"
    else:
        suggestion_seed = "不做/等，先等区间边缘或二次信号。"

    return {
        "bias": bias,
        "environment": environment,
        "bar_body_points": body,
        "bar_range_points": bar_range,
        "body_pct": body_pct,
        "ema_distance_points": ema_distance,
        "pa_read": pa_read,
        "suggestion_seed": suggestion_seed,
    }


def build_decision_pack(record):
    """构建决策包，只在 active=true 时生成 brief"""
    payload = normalize_payload(record.get("payload", {}))
    payload["received_at"] = record.get("received_at")

    update_recent_bars_cache(payload, limit=20)
    bars = read_recent_bars(limit=20)

    analysis = analyze_bars(bars[-20:])
    context = load_session_context()
    state = load_session_state()

    latest_bar = {
        "identity": bar_identity(payload),
        "received_at": record.get("received_at"),
        "symbol": payload.get("symbol"),
        "exchange": payload.get("exchange"),
        "timeframe": payload.get("timeframe"),
        "bar_time_bj": format_bar_time(payload),
        "time": payload.get("time"),
        "time_close": payload.get("time_close"),
        "open": payload.get("open"),
        "high": payload.get("high"),
        "low": payload.get("low"),
        "close": payload.get("close"),
        "volume": payload.get("volume"),
        "ema20": payload.get("ema20"),
        "bar_index": payload.get("bar_index"),
    }

    pack = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "latest_bar": latest_bar,
        "analysis_seed": analysis,
        "session_context": context,
        "session_active": state.get("active", False),
        "codex_response_contract": {
            "language": "Chinese",
            "max_analysis_time_seconds": 30,
            "style": "concise, execution-first",
            "must_include": [
                "做/不做/等",
                "direction",
                "entry_or_trigger",
                "stop_or_invalidation",
                "tp",
                "size",
                "one_line_reason",
            ],
        },
    }
    atomic_write_json(DECISION_PACK_PATH, pack)

    if state.get("active", False):
        atomic_write_text(CODEX_BRIEF_PATH, render_codex_brief(pack))
        notify_new_bar(pack)


def notify_new_bar(pack):
    bar = pack["latest_bar"]
    seed = pack["analysis_seed"]
    line = (
        f"GC 5m 新K {bar.get('bar_time_bj')} "
        f"C {bar.get('close')} / H {bar.get('high')} / L {bar.get('low')} | "
        f"{seed.get('suggestion_seed')}"
    )
    atomic_write_text(NOTIFICATION_PATH, line + "\n")


def render_codex_brief(pack):
    bar = pack["latest_bar"]
    seed = pack["analysis_seed"]
    context = pack["session_context"]
    accounts = "\n".join(
        f"- {account['name']}: {account['stage']}；{account['bias']}；默认 {account['default_size']}"
        for account in context.get("accounts", [])
    )
    rules = "\n".join(f"- {rule}" for rule in context.get("execution_rules", []))
    return f"""# Codex Webhook 快速决策包

## 最新 5m K
- 时间：{bar.get("bar_time_bj")}
- 标的：{bar.get("exchange")}:{bar.get("symbol")} {bar.get("timeframe")}
- OHLCV：O {bar.get("open")} / H {bar.get("high")} / L {bar.get("low")} / C {bar.get("close")} / V {bar.get("volume")}
- EMA20：{bar.get("ema20")}
- bar_index：{bar.get("bar_index")}

## 本地预分析
- Bias：{seed.get("bias")}
- 环境：{seed.get("environment")}
- PA：{seed.get("pa_read")}
- 初始建议方向：{seed.get("suggestion_seed")}

## 账户上下文
{accounts}

## 输出规则
{rules}

## 你要输出
用中文，30 秒内给执行优先建议：
`做/不做/等` + 方向 + 入场/触发 + 止损/失效 + TP + 仓位 + 一句话理由。
"""


class TradingViewWebhookHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path.rstrip("/")
        if path == "/health":
            state = load_session_state()
            self._send_json(200, {
                "ok": True,
                "service": "tradingview-webhook",
                "active": state.get("active", False),
            })
            return
        if path == "/latest":
            if not LATEST_PATH.exists():
                self._send_json(404, {"ok": False, "error": "no bars received yet"})
                return
            self._send_json(200, json.loads(LATEST_PATH.read_text(encoding="utf-8")))
            return
        if path == "/bars":
            if not RECENT_BARS_PATH.exists():
                self._send_json(404, {"ok": False, "error": "no bars yet"})
                return
            self._send_json(200, json.loads(RECENT_BARS_PATH.read_text(encoding="utf-8")))
            return
        if path == "/latest-brief":
            if not CODEX_BRIEF_PATH.exists():
                self._send_json(404, {"ok": False, "error": "no brief generated yet"})
                return
            brief = CODEX_BRIEF_PATH.read_text(encoding="utf-8")
            body = brief.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/markdown; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/decision-pack":
            if not DECISION_PACK_PATH.exists():
                self._send_json(404, {"ok": False, "error": "no decision pack yet"})
                return
            self._send_json(200, json.loads(DECISION_PACK_PATH.read_text(encoding="utf-8")))
            return
        if path == "/status":
            state = load_session_state()
            self._send_json(200, {"ok": True, **state})
            return
        self._send_json(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        request_path = urlparse(self.path).path.rstrip("/")

        if request_path == "/start":
            state = set_session_state(True)
            self._send_json(200, {"ok": True, "message": "session started", **state})
            return
        if request_path == "/stop":
            state = set_session_state(False)
            self._send_json(200, {"ok": True, "message": "session stopped", **state})
            return

        if request_path not in ("", "/webhook", "/tv"):
            self._send_json(404, {"ok": False, "error": "not found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = parse_tradingview_fallback(raw)

        if WEBHOOK_SECRET and payload.get("secret") != WEBHOOK_SECRET:
            self._send_json(403, {"ok": False, "error": "invalid secret"})
            return

        record = {
            "received_at": datetime.now(timezone.utc).isoformat(),
            "source": "tradingview",
            "payload": payload,
        }

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        atomic_write_json(LATEST_PATH, record)
        history_path = get_today_history_path()
        history_path.parent.mkdir(parents=True, exist_ok=True)
        with history_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        build_decision_pack(record)

        self._send_json(200, {"ok": True, "saved": str(LATEST_PATH)})

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BARS_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((HOST, PORT), TradingViewWebhookHandler)
    print(f"TradingView webhook receiver listening on http://{HOST}:{PORT}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("POST /, /webhook, /tv (data); /start, /stop (control)")
    print("GET /latest, /latest-brief, /decision-pack, /bars, /status, /health")
    server.serve_forever()
