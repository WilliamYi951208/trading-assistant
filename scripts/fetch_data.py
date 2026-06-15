#!/usr/bin/env python3
"""
Price Action 数据获取脚本 - 支持 tradingview-mcp
用于从 tradingview-mcp 获取 GC 5m 数据并转换为标准格式

Usage:
    python fetch_data.py GC1! COMEX 5m
"""
import sys
import json
from datetime import datetime, timezone

try:
    from tradingview_ta import TA_Handler, Interval
except ImportError:
    print(json.dumps({"error": "tradingview-ta not installed", "fix": "pip install tradingview-ta"}))
    sys.exit(1)


def get_interval(timeframe: str):
    """转换时间周期字符串为 Interval 枚举"""
    mapping = {
        "1m": Interval.INTERVAL_1_MINUTE,
        "5m": Interval.INTERVAL_5_MINUTES,
        "15m": Interval.INTERVAL_15_MINUTES,
        "1h": Interval.INTERVAL_1_HOUR,
        "4h": Interval.INTERVAL_4_HOURS,
        "1d": Interval.INTERVAL_1_DAY,
    }
    return mapping.get(timeframe.lower(), Interval.INTERVAL_5_MINUTES)


def fetch_gc_data(symbol: str = "GOLD", exchange: str = "TVC", timeframe: str = "5m"):
    """获取黄金数据并转换为 webhook 兼容格式

    黄金期货可用格式：
    - GOLD @ TVC (推荐)
    - XAUUSD @ OANDA
    - XAUUSD @ FX_IDC
    - XAUUSD @ FOREXCOM
    """
    # 自动映射常见黄金标的
    symbol_map = {
        "GC1!": ("GOLD", "TVC", "cfd"),
        "GC": ("GOLD", "TVC", "cfd"),
        "GOLD": ("GOLD", "TVC", "cfd"),
        "XAUUSD": ("XAUUSD", "OANDA", "cfd"),
    }

    if symbol in symbol_map:
        symbol, exchange, screener = symbol_map[symbol]
    else:
        screener = "cfd" if exchange in ["TVC", "OANDA", "FX_IDC", "FOREXCOM"] else "america"

    try:
        handler = TA_Handler(
            symbol=symbol,
            exchange=exchange,
            screener=screener,
            interval=get_interval(timeframe),
            timeout=10
        )

        analysis = handler.get_analysis()
        indicators = analysis.indicators

        # 转换为 webhook 兼容格式
        now = datetime.now(timezone.utc)
        payload = {
            "symbol": symbol,
            "exchange": exchange,
            "timeframe": timeframe,
            "time": int(now.timestamp() * 1000),
            "time_close": int(now.timestamp() * 1000),
            "open": indicators.get("open"),
            "high": indicators.get("high"),
            "low": indicators.get("low"),
            "close": indicators.get("close"),
            "volume": indicators.get("volume"),
            "ema20": indicators.get("EMA20"),
            "bar_index": None,
            "note": "mcp_fetch",
            "source": "tradingview-mcp",
            "recommendation": analysis.summary.get("RECOMMENDATION"),
            "buy_signals": analysis.summary.get("BUY"),
            "sell_signals": analysis.summary.get("SELL"),
            "neutral_signals": analysis.summary.get("NEUTRAL"),
        }

        return payload

    except Exception as e:
        return {"error": str(e), "symbol": symbol, "exchange": exchange}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        symbol = "GOLD"
        exchange = "TVC"
        timeframe = "5m"
    else:
        symbol = sys.argv[1]
        exchange = sys.argv[2] if len(sys.argv) > 2 else "COMEX"
        timeframe = sys.argv[3] if len(sys.argv) > 3 else "5m"

    result = fetch_gc_data(symbol, exchange, timeframe)
    print(json.dumps(result, indent=2, default=str))
