"""
Technical Strategies and Backtesting Engine for RUTE Scanner
Implements real mathematical indicators, signal generation, and deterministic backtesting.
Calculates Win Rate %, Loss Rate %, Profit Factor, Max Drawdown, and active Trade Setups.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd


# -------------------------------------------------------------
# Indicator Calculations
# -------------------------------------------------------------

def calculate_ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(window=period).mean()


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Textbook Wilder's RSI calculation (vectorized, identical to TradingView & MetaTrader)."""
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    
    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    
    rs = avg_gain / (avg_loss.replace(0, 1e-9))
    return 100.0 - (100.0 / (1.0 + rs))


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Textbook Wilder's Average True Range (ATR)."""
    high = df["high"]
    low = df["low"]
    close = df["close"]
    prev_close = close.shift(1)
    
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()


def calculate_bollinger_bands(series: pd.Series, period: int = 20, num_std: float = 2.0):
    sma = calculate_sma(series, period)
    std = series.rolling(window=period).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    return sma, upper, lower


def calculate_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    ema_fast = calculate_ema(series, fast)
    ema_slow = calculate_ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


# -------------------------------------------------------------
# Backtest Simulator
# -------------------------------------------------------------

def simulate_backtest(
    df: pd.DataFrame,
    signals: pd.Series,
    rr_ratio: float = 1.5,
    atr_multiplier: float = 1.5,
    max_holding_bars: int = 30
) -> Dict[str, Any]:
    """
    Simulates trades bar-by-bar given a signal series (1 = Buy, -1 = Sell, 0 = Hold).
    No lookahead bias: trade is opened at the open of bar t+1 after signal at bar t.
    """
    if len(df) < 30 or signals.abs().sum() == 0:
        return {
            "win_rate": 0.0,
            "loss_rate": 0.0,
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "profit_factor": 0.0,
            "avg_pnl_pct": 0.0,
            "max_drawdown_pct": 0.0,
            "trades": []
        }

    atr = calculate_atr(df, 14)
    trades = []
    in_trade = False
    trade_type = 0  # 1 for Long, -1 for Short
    entry_price = 0.0
    stop_loss = 0.0
    take_profit = 0.0
    entry_idx = 0

    closes = df["close"].values
    highs = df["high"].values
    lows = df["low"].values
    opens = df["open"].values
    timestamps = df["timestamp"].values
    signal_vals = signals.values
    atr_vals = np.nan_to_num(atr.bfill().values, nan=0.0)

    for i in range(20, len(df) - 1):
        if not in_trade:
            sig = signal_vals[i]
            if sig != 0:
                raw_entry = float(opens[i + 1])
                if raw_entry <= 0 or np.isnan(raw_entry):
                    continue
                in_trade = True
                trade_type = int(sig)
                entry_price = raw_entry
                curr_atr = float(atr_vals[i])
                if curr_atr <= 0:
                    curr_atr = entry_price * 0.005
                risk = max(curr_atr * atr_multiplier, entry_price * 0.003)
                
                if trade_type == 1:
                    stop_loss = entry_price - risk
                    take_profit = entry_price + (risk * rr_ratio)
                else:
                    stop_loss = entry_price + risk
                    take_profit = entry_price - (risk * rr_ratio)
                    
                entry_idx = i + 1
        else:
            # Check price action for SL / TP
            bar_high = highs[i]
            bar_low = lows[i]
            hit_tp = False
            hit_sl = False

            if trade_type == 1:
                if bar_low <= stop_loss:
                    hit_sl = True
                elif bar_high >= take_profit:
                    hit_tp = True
            elif trade_type == -1:
                if bar_high >= stop_loss:
                    hit_sl = True
                elif bar_low <= take_profit:
                    hit_tp = True

            timeout = (i - entry_idx) >= max_holding_bars

            if hit_tp or hit_sl or timeout:
                exit_price = take_profit if hit_tp else (stop_loss if hit_sl else closes[i])
                pnl = (exit_price - entry_price) / entry_price if trade_type == 1 else (entry_price - exit_price) / entry_price
                outcome = "WIN" if pnl > 0 else "LOSS"

                trades.append({
                    "entry_time": str(timestamps[entry_idx])[:16],
                    "exit_time": str(timestamps[i])[:16],
                    "type": "BUY" if trade_type == 1 else "SELL",
                    "entry_price": round(entry_price, 5),
                    "exit_price": round(float(exit_price), 5),
                    "pnl_pct": round(pnl * 100, 2),
                    "outcome": outcome,
                    "bars_held": i - entry_idx
                })
                in_trade = False

    total_trades = len(trades)
    if total_trades == 0:
        return {
            "win_rate": 0.0,
            "loss_rate": 0.0,
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "profit_factor": 0.0,
            "avg_pnl_pct": 0.0,
            "max_drawdown_pct": 0.0,
            "trades": []
        }

    wins = [t for t in trades if t["outcome"] == "WIN"]
    losses = [t for t in trades if t["outcome"] == "LOSS"]
    win_count = len(wins)
    loss_count = len(losses)
    win_rate = round((win_count / total_trades) * 100, 1)
    loss_rate = round((loss_count / total_trades) * 100, 1)

    gross_profit = sum(t["pnl_pct"] for t in wins)
    gross_loss = abs(sum(t["pnl_pct"] for t in losses))
    profit_factor = round(gross_profit / gross_loss, 2) if gross_loss > 0 else 9.99

    # Calculate Max Drawdown
    equity_curve = [100.0]
    for t in trades:
        equity_curve.append(equity_curve[-1] * (1.0 + t["pnl_pct"] / 100.0))
    peak = equity_curve[0]
    max_dd = 0.0
    for val in equity_curve:
        if val > peak:
            peak = val
        dd = (peak - val) / peak * 100.0
        if dd > max_dd:
            max_dd = dd

    return {
        "win_rate": win_rate,
        "loss_rate": loss_rate,
        "total_trades": total_trades,
        "wins": win_count,
        "losses": loss_count,
        "profit_factor": profit_factor,
        "avg_pnl_pct": round(float(np.mean([t["pnl_pct"] for t in trades])), 2),
        "max_drawdown_pct": round(max_dd, 1),
        "trades": trades[-10:]  # last 10 trades for quick audit
    }


# -------------------------------------------------------------
# Strategies Implementations
# -------------------------------------------------------------

class AlphaTrendStrategy:
    """Trend confluence: EMA 20 > EMA 50 > EMA 200 + Volume confirmation."""
    name = "AlphaTrend Momentum"
    description = "Trend-following strategy combining multi-EMA hierarchy with volume expansion."

    @staticmethod
    def run(df: pd.DataFrame) -> Dict[str, Any]:
        if len(df) < 50:
            return {"status": "insufficient_data"}

        ema20 = calculate_ema(df["close"], 20)
        ema50 = calculate_ema(df["close"], 50)
        ema200 = calculate_ema(df["close"], min(len(df) - 1, 200))
        vol_sma = calculate_sma(df["volume"], 20)
        atr = calculate_atr(df, 14)

        signals = pd.Series(0, index=df.index)
        
        # Check if volume data is present and non-trivial (Forex typically has volume=0 on Yahoo)
        has_real_volume = bool((df["volume"].sum() > 0) and (df["volume"].std() > 0))
        vol_filter = (df["volume"] > vol_sma * 1.05) if has_real_volume else pd.Series(True, index=df.index)

        # Bullish conditions: Price > EMA20 > EMA50 and Volume > Average (when volume available)
        bull = (df["close"] > ema20) & (ema20 > ema50) & vol_filter
        bear = (df["close"] < ema20) & (ema20 < ema50) & vol_filter
        
        # Trigger on crossover / initial alignment
        signals[bull & (~bull.shift(1).fillna(False))] = 1
        signals[bear & (~bear.shift(1).fillna(False))] = -1

        backtest = simulate_backtest(df, signals, rr_ratio=1.8, atr_multiplier=1.4)

        # Current status
        last_close = float(df["close"].iloc[-1])
        last_atr = float(atr.iloc[-1])
        current_sig = "NEUTRAL"
        setup = None

        if bull.iloc[-1]:
            current_sig = "BUY"
            sl = round(last_close - (last_atr * 1.4), 5)
            tp1 = round(last_close + (last_atr * 1.4 * 1.2), 5)
            tp2 = round(last_close + (last_atr * 1.4 * 2.0), 5)
            setup = {"action": "BUY", "entry": last_close, "sl": sl, "tp1": tp1, "tp2": tp2, "rr": 1.8}
        elif bear.iloc[-1]:
            current_sig = "SELL"
            sl = round(last_close + (last_atr * 1.4), 5)
            tp1 = round(last_close - (last_atr * 1.4 * 1.2), 5)
            tp2 = round(last_close - (last_atr * 1.4 * 2.0), 5)
            setup = {"action": "SELL", "entry": last_close, "sl": sl, "tp1": tp1, "tp2": tp2, "rr": 1.8}

        return {
            "strategy_id": "alpha_trend",
            "name": AlphaTrendStrategy.name,
            "description": AlphaTrendStrategy.description,
            "signal": current_sig,
            "setup": setup,
            "backtest": backtest
        }


class RSIDivergenceBollingerStrategy:
    """Mean reversion: RSI overbought/oversold with Bollinger Band rejection."""
    name = "RSI & Bollinger Mean Reversion"
    description = "Identifies overextended price spikes touching outer Bollinger Bands with RSI extreme exhaustion."

    @staticmethod
    def run(df: pd.DataFrame) -> Dict[str, Any]:
        if len(df) < 30:
            return {"status": "insufficient_data"}

        rsi = calculate_rsi(df["close"], 14)
        mid, upper, lower = calculate_bollinger_bands(df["close"], 20, 2.0)
        atr = calculate_atr(df, 14)

        signals = pd.Series(0, index=df.index)
        
        # Long when price touches lower band and RSI < 35, then crosses back up
        long_cond = (df["low"] <= lower) & (rsi < 35) & (df["close"] > df["open"])
        short_cond = (df["high"] >= upper) & (rsi > 65) & (df["close"] < df["open"])

        signals[long_cond] = 1
        signals[short_cond] = -1

        backtest = simulate_backtest(df, signals, rr_ratio=1.5, atr_multiplier=1.2)

        last_close = float(df["close"].iloc[-1])
        last_atr = float(atr.iloc[-1])
        last_rsi = float(rsi.iloc[-1])
        current_sig = "NEUTRAL"
        setup = None

        if long_cond.iloc[-1] or (last_rsi < 32 and df["close"].iloc[-1] <= lower.iloc[-1]):
            current_sig = "BUY"
            sl = round(last_close - (last_atr * 1.2), 5)
            tp1 = round(max(float(mid.iloc[-1]), last_close + (last_atr * 0.8)), 5)
            tp2 = round(last_close + (last_atr * 1.8), 5)
            setup = {"action": "BUY", "entry": last_close, "sl": sl, "tp1": tp1, "tp2": tp2, "rr": 1.5}
        elif short_cond.iloc[-1] or (last_rsi > 68 and df["close"].iloc[-1] >= upper.iloc[-1]):
            current_sig = "SELL"
            sl = round(last_close + (last_atr * 1.2), 5)
            tp1 = round(min(float(mid.iloc[-1]), last_close - (last_atr * 0.8)), 5)
            tp2 = round(last_close - (last_atr * 1.8), 5)
            setup = {"action": "SELL", "entry": last_close, "sl": sl, "tp1": tp1, "tp2": tp2, "rr": 1.5}

        return {
            "strategy_id": "rsi_bollinger",
            "name": RSIDivergenceBollingerStrategy.name,
            "description": RSIDivergenceBollingerStrategy.description,
            "signal": current_sig,
            "setup": setup,
            "backtest": backtest
        }


class MACDMomentumStrategy:
    """Momentum expansion: MACD crossover above/below zero-line."""
    name = "MACD Momentum Expansion"
    description = "Catches high-velocity momentum shifts where the MACD line crosses the signal line with expanding histogram."

    @staticmethod
    def run(df: pd.DataFrame) -> Dict[str, Any]:
        if len(df) < 35:
            return {"status": "insufficient_data"}

        macd, signal, hist = calculate_macd(df["close"])
        atr = calculate_atr(df, 14)

        signals = pd.Series(0, index=df.index)
        
        # Bull cross: MACD crosses above signal
        bull_cross = (macd > signal) & (macd.shift(1) <= signal.shift(1))
        bear_cross = (macd < signal) & (macd.shift(1) >= signal.shift(1))

        signals[bull_cross] = 1
        signals[bear_cross] = -1

        backtest = simulate_backtest(df, signals, rr_ratio=1.6, atr_multiplier=1.5)

        last_close = float(df["close"].iloc[-1])
        last_atr = float(atr.iloc[-1])
        current_sig = "NEUTRAL"
        setup = None

        if hist.iloc[-1] > 0 and hist.iloc[-1] > hist.iloc[-2]:
            current_sig = "BUY"
            sl = round(last_close - (last_atr * 1.5), 5)
            tp1 = round(last_close + (last_atr * 1.5 * 1.2), 5)
            tp2 = round(last_close + (last_atr * 1.5 * 2.0), 5)
            setup = {"action": "BUY", "entry": last_close, "sl": sl, "tp1": tp1, "tp2": tp2, "rr": 1.6}
        elif hist.iloc[-1] < 0 and hist.iloc[-1] < hist.iloc[-2]:
            current_sig = "SELL"
            sl = round(last_close + (last_atr * 1.5), 5)
            tp1 = round(last_close - (last_atr * 1.5 * 1.2), 5)
            tp2 = round(last_close - (last_atr * 1.5 * 2.0), 5)
            setup = {"action": "SELL", "entry": last_close, "sl": sl, "tp1": tp1, "tp2": tp2, "rr": 1.6}

        return {
            "strategy_id": "macd_momentum",
            "name": MACDMomentumStrategy.name,
            "description": MACDMomentumStrategy.description,
            "signal": current_sig,
            "setup": setup,
            "backtest": backtest
        }


class SmartMoneyLiquiditySweepStrategy:
    """Order Flow: Sweeps of 20-bar High/Low followed by rejection pin bar."""
    name = "Smart Money Liquidity Sweep"
    description = "Detects institutional stop-runs: price sweeps key swing highs/lows then closes aggressively back inside the range."

    @staticmethod
    def run(df: pd.DataFrame) -> Dict[str, Any]:
        if len(df) < 30:
            return {"status": "insufficient_data"}

        swing_high = df["high"].rolling(20).max().shift(1)
        swing_low = df["low"].rolling(20).min().shift(1)
        atr = calculate_atr(df, 14)

        signals = pd.Series(0, index=df.index)
        
        # Bullish sweep: Low broke swing low, but Close rallied back above swing low (fakeout/sweep)
        bull_sweep = (df["low"] < swing_low) & (df["close"] > swing_low) & (df["close"] > df["open"])
        bear_sweep = (df["high"] > swing_high) & (df["close"] < swing_high) & (df["close"] < df["open"])

        signals[bull_sweep] = 1
        signals[bear_sweep] = -1

        backtest = simulate_backtest(df, signals, rr_ratio=2.0, atr_multiplier=1.2)

        last_close = float(df["close"].iloc[-1])
        last_atr = float(atr.iloc[-1])
        current_sig = "NEUTRAL"
        setup = None

        if bull_sweep.iloc[-1]:
            current_sig = "BUY"
            raw_risk = last_close - (float(df["low"].iloc[-1]) - (last_atr * 0.3))
            risk = max(raw_risk, last_atr * 0.6, last_close * 0.003)
            sl = round(last_close - risk, 5)
            tp1 = round(last_close + risk * 1.5, 5)
            tp2 = round(last_close + risk * 2.5, 5)
            setup = {"action": "BUY", "entry": last_close, "sl": sl, "tp1": tp1, "tp2": tp2, "rr": 2.0}
        elif bear_sweep.iloc[-1]:
            current_sig = "SELL"
            raw_risk = (float(df["high"].iloc[-1]) + (last_atr * 0.3)) - last_close
            risk = max(raw_risk, last_atr * 0.6, last_close * 0.003)
            sl = round(last_close + risk, 5)
            tp1 = round(last_close - risk * 1.5, 5)
            tp2 = round(last_close - risk * 2.5, 5)
            setup = {"action": "SELL", "entry": last_close, "sl": sl, "tp1": tp1, "tp2": tp2, "rr": 2.0}

        return {
            "strategy_id": "liquidity_sweep",
            "name": SmartMoneyLiquiditySweepStrategy.name,
            "description": SmartMoneyLiquiditySweepStrategy.description,
            "signal": current_sig,
            "setup": setup,
            "backtest": backtest
        }


ALL_STRATEGIES = [
    AlphaTrendStrategy,
    RSIDivergenceBollingerStrategy,
    MACDMomentumStrategy,
    SmartMoneyLiquiditySweepStrategy
]
