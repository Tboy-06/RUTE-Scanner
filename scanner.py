"""
Opportunity Scanner & Trade Ranking Engine for RUTE
Scans markets across Forex, Crypto, Commodities, and Stocks.
Ranks trade setups by Win Rate %, Confluence Score, and Risk/Reward.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading
import logging
from typing import Dict, Any, List
from market_data import WATCHLIST, get_market_candles, get_current_price
from market_catalog import CORE_PRIORITY_SYMBOLS
from strategies import ALL_STRATEGIES
from mtf_engine import get_mtf_matrix
from trade_journal import TradeJournal

logger = logging.getLogger("scanner")

# Global cached scan results and thread lock
_SCAN_LOCK = threading.Lock()
_LATEST_SCAN: Dict[str, Any] = {
    "timestamp": 0,
    "top_setups": [],
    "market_summary": {},
    "all_results": []
}


def scan_asset(symbol: str, asset_info: Dict[str, Any], interval: str = "1h", include_candles: bool = True) -> Dict[str, Any]:
    """Runs all strategies on a single asset and calculates confluence & win/loss statistics."""
    df = get_market_candles(symbol, interval=interval, period="1mo")
    if len(df) < 30:
        return {
            "symbol": symbol,
            "name": asset_info.get("name", symbol),
            "type": asset_info.get("type", "unknown"),
            "status": "insufficient_data",
            "current_price": float(df["close"].iloc[-1]) if len(df) > 0 else 0.0,
            "change_pct": 0.0,
            "confluence": "NEUTRAL",
            "confluence_score": 0,
            "buy_votes": 0,
            "sell_votes": 0,
            "avg_win_rate": 0.0,
            "best_setup": None,
            "strategies": [],
            "candles": [],
            "mtf": None
        }

    last_price = float(df["close"].iloc[-1])
    prev_price = float(df["close"].iloc[-2])
    change_pct = round(((last_price - prev_price) / prev_price) * 100, 2)

    strategy_results = []
    buy_votes = 0
    sell_votes = 0
    total_strategies = 0
    win_rates = []

    for Strat in ALL_STRATEGIES:
        res = Strat.run(df)
        if "backtest" in res:
            strategy_results.append(res)
            sig = res.get("signal", "NEUTRAL")
            wr = res["backtest"].get("win_rate", 0.0)
            
            if sig == "BUY":
                buy_votes += 1
                win_rates.append(wr)
            elif sig == "SELL":
                sell_votes += 1
                win_rates.append(wr)
            total_strategies += 1

    # Confluence calculation
    confluence = "NEUTRAL"
    consensus_score = 0
    best_setup = None
    best_wr = 0.0

    if buy_votes > sell_votes and buy_votes >= 1:
        confluence = "BUY"
        consensus_score = int((buy_votes / total_strategies) * 100)
    elif sell_votes > buy_votes and sell_votes >= 1:
        confluence = "SELL"
        consensus_score = int((sell_votes / total_strategies) * 100)

    # Find the single best setup among active strategies
    for res in strategy_results:
        setup = res.get("setup")
        wr = res["backtest"].get("win_rate", 0.0)
        if setup and setup.get("action") == confluence:
            if wr > best_wr:
                best_wr = wr
                best_setup = {
                    **setup,
                    "strategy_name": res["name"],
                    "strategy_id": res["strategy_id"],
                    "win_rate": wr,
                    "loss_rate": res["backtest"].get("loss_rate", 0.0),
                    "profit_factor": res["backtest"].get("profit_factor", 0.0),
                    "total_trades": res["backtest"].get("total_trades", 0),
                    "max_drawdown_pct": res["backtest"].get("max_drawdown_pct", 0.0)
                }

    avg_win_rate = round(float(sum(win_rates) / len(win_rates)), 1) if win_rates else 0.0

    # Include recent 50 bars for live interactive chart rendering (bklit / NEXUS style)
    recent_candles = []
    if include_candles and len(df) > 0:
        for _, row in df.tail(50).iterrows():
            recent_candles.append({
                "time": str(row["timestamp"])[:16],
                "open": round(float(row["open"]), 5),
                "high": round(float(row["high"]), 5),
                "low": round(float(row["low"]), 5),
                "close": round(float(row["close"]), 5)
            })

    # Include MTF matrix when detail is requested
    mtf_data = None
    if include_candles:
        try:
            mtf_data = get_mtf_matrix(symbol)
        except Exception as e:
            logger.warning(f"MTF calculation fallback for {symbol}: {e}")
            mtf_data = None

    return {
        "symbol": symbol,
        "name": asset_info["name"],
        "type": asset_info["type"],
        "current_price": last_price,
        "change_pct": change_pct,
        "confluence": confluence,
        "confluence_score": consensus_score,
        "buy_votes": buy_votes,
        "sell_votes": sell_votes,
        "avg_win_rate": avg_win_rate,
        "best_setup": best_setup,
        "strategies": strategy_results,
        "candles": recent_candles,
        "mtf": mtf_data
    }


def run_full_scan(interval: str = "1h") -> Dict[str, Any]:
    """
    Tiered Market Scanner:
    1. Scans core priority assets immediately (35 assets across all markets) for sub-second UI response.
    2. Progressively scans the full 260+ catalog (Top 100 Stocks, Top 100 Crypto, Top 60+ Forex/Commodities)
       in a background thread pool, populating results smoothly without rate limiting.
    """
    global _LATEST_SCAN
    start_time = time.time()
    all_results = []
    top_setups = []

    # Flatten asset list
    all_assets = [asset for assets in WATCHLIST.values() for asset in assets]
    core_assets = [a for a in all_assets if a["symbol"] in CORE_PRIORITY_SYMBOLS]
    extended_assets = [a for a in all_assets if a["symbol"] not in CORE_PRIORITY_SYMBOLS]

    def _worker(asset):
        try:
            return scan_asset(asset["symbol"], asset, interval=interval, include_candles=False)
        except Exception as e:
            logger.error(f"Error scanning {asset.get('symbol')}: {e}")
            return None

    def _process_result(res):
        if res and res.get("status") != "insufficient_data":
            all_results.append(res)
            if res.get("best_setup") and res["confluence"] in ["BUY", "SELL"]:
                setup = res["best_setup"]
                score = round((setup["win_rate"] * 0.5) + (res["confluence_score"] * 0.3) + (setup.get("rr", 1.5) * 10), 1)
                top_setups.append({
                    "symbol": res["symbol"],
                    "name": res["name"],
                    "type": res["type"],
                    "price": res["current_price"],
                    "action": res["confluence"],
                    "entry": setup["entry"],
                    "sl": setup["sl"],
                    "tp1": setup["tp1"],
                    "tp2": setup["tp2"],
                    "rr": setup.get("rr", 1.5),
                    "strategy": setup["strategy_name"],
                    "win_rate": setup["win_rate"],
                    "loss_rate": setup["loss_rate"],
                    "profit_factor": setup["profit_factor"],
                    "total_trades": setup["total_trades"],
                    "max_drawdown_pct": setup["max_drawdown_pct"],
                    "confluence_score": res["confluence_score"],
                    "opportunity_score": score
                })

    # 1. Immediate scan of Core Priority Markets
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(_worker, asset) for asset in core_assets]
        for f in as_completed(futures):
            _process_result(f.result())

    top_setups.sort(key=lambda x: x["opportunity_score"], reverse=True)

    for s in top_setups[:5]:
        try:
            s["mtf"] = get_mtf_matrix(s["symbol"])
        except Exception:
            s["mtf"] = None

    try:
        price_map = {r["symbol"]: r["current_price"] for r in all_results if "symbol" in r and "current_price" in r}
        TradeJournal.update_prices(price_map)
        for s in top_setups:
            if s.get("opportunity_score", 0) >= 50:
                TradeJournal.log_setup(s)
    except Exception as e:
        logger.error(f"Error updating trade journal: {e}")

    with _SCAN_LOCK:
        _LATEST_SCAN = {
            "timestamp": int(time.time()),
            "scan_duration_sec": round(time.time() - start_time, 2),
            "total_assets_scanned": len(all_results),
            "total_catalog_size": len(all_assets),
            "top_setups_count": len(top_setups),
            "top_setups": list(top_setups),
            "all_results": list(all_results)
        }

    # 2. Asynchronous background scan of remaining extended markets (Top 100 Stocks, Top 100 Crypto, etc.)
    def _bg_extended_worker():
        chunk_size = 15
        for i in range(0, len(extended_assets), chunk_size):
            chunk = extended_assets[i:i + chunk_size]
            with ThreadPoolExecutor(max_workers=8) as ex:
                futs = [ex.submit(_worker, a) for a in chunk]
                for f in as_completed(futs):
                    _process_result(f.result())
            
            top_setups.sort(key=lambda x: x["opportunity_score"], reverse=True)
            # Ensure top 5 always have MTF attached
            for s in top_setups[:5]:
                if "mtf" not in s or s["mtf"] is None:
                    try:
                        s["mtf"] = get_mtf_matrix(s["symbol"])
                    except Exception:
                        s["mtf"] = None

            with _SCAN_LOCK:
                _LATEST_SCAN["total_assets_scanned"] = len(all_results)
                _LATEST_SCAN["top_setups_count"] = len(top_setups)
                _LATEST_SCAN["top_setups"] = list(top_setups)
                _LATEST_SCAN["all_results"] = list(all_results)
            time.sleep(0.15)  # Politeness delay to prevent rate limits

        # Log any newly surfaced high-probability extended setups to journal
        try:
            for s in top_setups[:10]:
                if s.get("opportunity_score", 0) >= 50:
                    TradeJournal.log_setup(s)
        except Exception:
            pass

    threading.Thread(target=_bg_extended_worker, daemon=True).start()

    with _SCAN_LOCK:
        return dict(_LATEST_SCAN)


_IS_SCANNING = False

def get_latest_scan() -> Dict[str, Any]:
    """
    Ultra-fast non-blocking scan provider.
    Returns existing cached scan immediately (< 5ms).
    If cache is older than 60s, updates in a background thread without blocking the user.
    """
    global _LATEST_SCAN, _IS_SCANNING
    now = time.time()
    with _SCAN_LOCK:
        has_data = bool(_LATEST_SCAN.get("all_results"))
        is_stale = (now - _LATEST_SCAN.get("timestamp", 0)) > 60

    if has_data:
        if is_stale and not _IS_SCANNING:
            _IS_SCANNING = True
            def _bg_scan():
                global _IS_SCANNING
                try:
                    run_full_scan()
                finally:
                    _IS_SCANNING = False
            threading.Thread(target=_bg_scan, daemon=True).start()
        with _SCAN_LOCK:
            return dict(_LATEST_SCAN)

    return run_full_scan()
