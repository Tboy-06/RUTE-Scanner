"""
Multi-Timeframe (MTF) Alignment Matrix Engine
Analyzes 15-Minute (Execution), 1-Hour (Swing), and 4-Hour / Daily (Macro)
trends to verify higher-timeframe confluence and eliminate counter-trend traps.
"""

import logging
import threading
from typing import Dict, Any, Optional
import pandas as pd
from market_data import get_market_candles
from strategies import calculate_ema, calculate_rsi

logger = logging.getLogger("mtf_engine")

# In-memory cache for MTF results to avoid excessive API calls (TTL 60s)
_MTF_CACHE: Dict[str, tuple[float, Dict[str, Any]]] = {}
_MTF_LOCK = threading.Lock()
CACHE_TTL = 60.0


def _evaluate_timeframe_trend(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyzes a timeframe candle dataframe for EMA hierarchy and RSI momentum."""
    if len(df) < 25:
        return {"trend": "NEUTRAL", "rsi": 50.0, "color": "slate", "desc": "Insufficient Data"}

    close = df["close"]
    ema20 = calculate_ema(close, 20)
    ema50 = calculate_ema(close, min(len(df) - 1, 50))
    rsi = calculate_rsi(close, 14)

    last_close = float(close.iloc[-1])
    last_ema20 = float(ema20.iloc[-1])
    last_ema50 = float(ema50.iloc[-1])
    last_rsi = round(float(rsi.iloc[-1]), 1)

    if last_close > last_ema20 and last_ema20 >= last_ema50 and last_rsi >= 48:
        return {"trend": "BULLISH", "rsi": last_rsi, "color": "emerald", "desc": "Bullish Trend"}
    elif last_close < last_ema20 and last_ema20 <= last_ema50 and last_rsi <= 52:
        return {"trend": "BEARISH", "rsi": last_rsi, "color": "rose", "desc": "Bearish Trend"}
    elif last_close > last_ema20:
        return {"trend": "BULLISH_BIAS", "rsi": last_rsi, "color": "teal", "desc": "Mild Bullish"}
    elif last_close < last_ema20:
        return {"trend": "BEARISH_BIAS", "rsi": last_rsi, "color": "amber", "desc": "Mild Bearish"}
    else:
        return {"trend": "NEUTRAL", "rsi": last_rsi, "color": "slate", "desc": "Consolidating"}


def get_mtf_matrix(symbol: str) -> Dict[str, Any]:
    """
    Computes 15m, 1h, and 4h/Daily alignment for a given symbol.
    Uses caching to prevent repetitive network requests.
    """
    import time
    now = time.time()
    with _MTF_LOCK:
        if symbol in _MTF_CACHE:
            cached_time, cached_val = _MTF_CACHE[symbol]
            if now - cached_time < CACHE_TTL:
                return cached_val

    # 1. 15-Minute execution
    df_15m = get_market_candles(symbol, interval="15m", period="5d")
    m15 = _evaluate_timeframe_trend(df_15m)

    # 2. 1-Hour swing
    df_1h = get_market_candles(symbol, interval="1h", period="1mo")
    h1 = _evaluate_timeframe_trend(df_1h)

    # 3. Daily / Macro
    df_1d = get_market_candles(symbol, interval="1d", period="3mo")
    macro = _evaluate_timeframe_trend(df_1d)

    # Confluence Score calculation
    bull_count = sum(1 for tf in [m15, h1, macro] if "BULLISH" in tf["trend"])
    bear_count = sum(1 for tf in [m15, h1, macro] if "BEARISH" in tf["trend"])

    if bull_count == 3:
        confluence_grade = "STRONG BULLISH ALIGNMENT"
        confluence_score = 100
        confluence_action = "BUY"
        status_color = "emerald"
    elif bear_count == 3:
        confluence_grade = "STRONG BEARISH ALIGNMENT"
        confluence_score = 100
        confluence_action = "SELL"
        status_color = "rose"
    elif bull_count == 2 and bear_count == 0:
        confluence_grade = "MODERATE BULLISH (2/3)"
        confluence_score = 75
        confluence_action = "BUY"
        status_color = "teal"
    elif bear_count == 2 and bull_count == 0:
        confluence_grade = "MODERATE BEARISH (2/3)"
        confluence_score = 75
        confluence_action = "SELL"
        status_color = "rose"
    else:
        confluence_grade = "TIMEFRAME DIVERGENCE (CHOP)"
        confluence_score = 40
        confluence_action = "NEUTRAL"
        status_color = "slate"

    result = {
        "symbol": symbol,
        "m15": m15,
        "h1": h1,
        "macro": macro,
        "confluence_grade": confluence_grade,
        "confluence_score": confluence_score,
        "confluence_action": confluence_action,
        "status_color": status_color
    }

    with _MTF_LOCK:
        _MTF_CACHE[symbol] = (now, result)
    return result
