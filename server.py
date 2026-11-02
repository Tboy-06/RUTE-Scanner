"""
RUTE Scanner & Strategy Testing Server
FastAPI Web Server binding to 0.0.0.0:8080.
Provides REST APIs for mobile and desktop web browsers with zero desktop MT5 popups.
"""

import os
import socket
import logging
from typing import Optional
from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from scanner import run_full_scan, get_latest_scan, scan_asset
from market_data import WATCHLIST, get_current_price
from rute_pulse import RutePulse
from rute_news_lens import RuteNewsLens
from rute_connect import RuteConnect
from rute_visuals import RuteVisuals
import tunnel_manager
from mtf_engine import get_mtf_matrix
from trade_journal import TradeJournal

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("server")

app = FastAPI(title="RUTE Trade Scanner & Strategy Tester", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


def get_local_ip() -> str:
    """Finds the primary local LAN IP address of this machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


@app.get("/api/network-info")
def network_info():
    """Returns local network details so user knows exact URL for phone access."""
    ip = get_local_ip()
    port = 8080
    return {
        "status": "online",
        "local_ip": ip,
        "port": port,
        "desktop_url": f"http://localhost:{port}",
        "mobile_url": f"http://{ip}:{port}",
        "instructions": "Ensure your phone is connected to the same Wi-Fi network, then open mobile_url in Safari or Chrome."
    }


@app.get("/api/watchlist")
def get_watchlist():
    return WATCHLIST


@app.get("/api/pulse")
def get_system_pulse():
    """RutePulse: Real-time background process lineage and RAM/CPU watchdog."""
    return RutePulse.get_system_pulse()


@app.get("/api/macro-news")
def get_macro_news():
    """RuteNewsLens: Live financial RSS headlines and real-time CBOE VIX volatility regime."""
    return {
        "headlines": RuteNewsLens.get_live_headlines(),
        "regime": RuteNewsLens.evaluate_market_regime()
    }


@app.get("/api/connect")
def get_connect_manifest():
    """RuteConnect: Pairing codes and cellular remote tunnel instructions."""
    return RuteConnect.get_connection_manifest(port=8080)


@app.get("/api/scan")
def get_scan(interval: str = Query("1h", description="Candle interval (15m, 1h, 4h, 1d)")):
    """Returns the ranked trade opportunities and strategy performance across all markets."""
    if interval == "1h":
        return get_latest_scan()
    return run_full_scan(interval=interval)


@app.get("/api/scan/force")
def force_scan(interval: str = Query("1h")):
    """Forces an instant fresh market rescan."""
    return run_full_scan(interval=interval)


@app.get("/api/asset/{symbol}")
def get_asset_detail(symbol: str, interval: str = Query("1h")):
    """Deep-dive backtest and strategy breakdown for a single symbol."""
    clean_sym = symbol.strip()
    found_info = None
    for category, assets in WATCHLIST.items():
        for item in assets:
            if item["symbol"].upper() == clean_sym.upper():
                found_info = item
                break
        if found_info:
            break
            
    if not found_info:
        found_info = {"symbol": clean_sym.upper(), "name": clean_sym.upper(), "type": "custom"}
        
    return scan_asset(clean_sym, found_info, interval=interval, include_candles=True)


# -------------------------------------------------------------
# Cloudflare Mobile Tunnel Endpoints
# -------------------------------------------------------------
@app.post("/api/tunnel/start")
def api_start_tunnel():
    """Starts Cloudflare Tunnel for mobile access on 4G/5G cellular."""
    return tunnel_manager.start_tunnel(port=8080)


@app.post("/api/tunnel/stop")
def api_stop_tunnel():
    """Stops active Cloudflare Tunnel."""
    return tunnel_manager.stop_tunnel()


@app.get("/api/tunnel/status")
def api_tunnel_status():
    """Returns current Cloudflare Tunnel state and public URL."""
    return tunnel_manager.get_tunnel_status()


# -------------------------------------------------------------
# Forward-Testing Trade Journal Endpoints
# -------------------------------------------------------------
@app.get("/api/journal")
def api_get_journal(limit: int = 50):
    """Returns forward-tested logged trade history and real-world win/loss stats."""
    return TradeJournal.get_journal(limit=limit)


@app.post("/api/journal/log")
def api_log_trade(setup: dict):
    """Manually or programmatically logs a trade setup to forward-test."""
    trade_id = TradeJournal.log_setup(setup)
    return {"status": "logged", "id": trade_id}


# -------------------------------------------------------------
# Multi-Timeframe Confluence Matrix Endpoint
# -------------------------------------------------------------
@app.get("/api/mtf/{symbol}")
def api_get_mtf(symbol: str):
    """Returns 15m, 1h, and 4h trend alignment for an asset."""
    return get_mtf_matrix(symbol)


# -------------------------------------------------------------
# Dynamic Arbitrary Market Scanner (User can scan ANY global symbol)
# -------------------------------------------------------------
@app.get("/api/scan/custom")
def api_scan_custom(symbol: str = Query(..., description="Any global ticker, e.g. META, NFLX, GBPJPY=X"), interval: str = Query("1h")):
    """Scans and backtests any arbitrary market ticker on-the-fly without hardcoding."""
    clean_sym = symbol.strip().upper()
    info = {"symbol": clean_sym, "name": clean_sym, "type": "custom"}
    return scan_asset(clean_sym, info, interval=interval, include_candles=True)


@app.on_event("startup")
def startup_event():
    """Pre-warms the market scan in background so initial page load takes < 10ms."""
    import threading
    threading.Thread(target=run_full_scan, daemon=True).start()


# Mount static directory for frontend
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    local_ip = get_local_ip()
    port = 8080
    print("\n" + "=" * 65)
    print("  [+] RUTE HIGH-PROBABILITY TRADE SCANNER IS RUNNING!")
    print(f"  [PC] Laptop / Desktop: http://localhost:{port}")
    print(f"  [PHONE] Phone (Same Wi-Fi): http://{local_ip}:{port}")
    print("=" * 65 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
