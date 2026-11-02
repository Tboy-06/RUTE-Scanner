# RUTE NEXUS V2 — High-Probability Trade Scanner & Strategy Tester

An institutional, local-first trade scanner, strategy testing engine, and live forward-test journal. Designed to run silently on your machine with zero desktop GUI clutter and instant accessibility across **Desktop**, **Local Wi-Fi Mobile**, and **4G/5G Cellular Networks** via Cloudflare Tunnel.

---

## Key Highlights

- **260+ Real Live Market Catalog:** Covers Top 100 Cryptocurrencies, Top 100 US Equities & Index ETFs, and 60+ Forex currency pairs and commodities (Gold, Silver, WTI Crude, Brent, Natural Gas).
- **Zero MetaTrader 5 Dependencies:** Never launches MT5 desktop popups, never suffers broker login timeouts. Data is sourced through real-time financial feeds (Binance public REST API & Yahoo Finance v8 direct JSON engine).
- **Symmetrical Buy & Sell Strategies:** All strategies generate mathematically rigorous signals and walk-forward backtests symmetrically for both Long and Short market regimes.
- **SQLite Forward-Testing Trade Journal:** Automatically logs high-probability setups and tracks their live performance in real-time until Take-Profit (TP1/TP2) or Stop-Loss (SL) levels trigger.
- **Multi-Timeframe Alignment Matrix (MTF):** Evaluates 15m (Execution), 1h (Swing), and 4h/Daily (Macro) candle hierarchies to eliminate counter-trend traps.
- **Universal Arbitrary Search:** Allows scanning and backtesting any arbitrary ticker globally on-the-fly (e.g. `AAPL`, `SOL-USD`, `GBPJPY=X`, `CL=F`).
- **Cloudflare Mobile Tunnel:** One-click built-in mobile pairing for iPhone and Android over cellular 4G/5G without router port forwarding.
- **Institutional NEXUS V2 UI:** High-contrast terminal aesthetic with live interactive SVG chart, risk-reward price ladder diagrams, and Web Audio API alerts.

---

## Strategy Catalog

1. **AlphaTrend Momentum:** Multi-EMA hierarchy (20 > 50 > 200) with volume confirmation expansion.
2. **RSI & Bollinger Mean Reversion:** Identifies price exhaustion touching outer 2.0-std Bollinger Bands with RSI extreme divergence.
3. **MACD Momentum Expansion:** Velocity crossovers above/below zero-line with accelerating histogram confirmation.
4. **Smart Money Liquidity Sweep:** Detects institutional stop-runs sweeping 20-bar swing highs/lows with aggressive rejection pin bars.

---

## Quick Start

### Prerequisites
- Python 3.10+
- Dependencies: `pip install fastapi uvicorn requests pandas numpy psutil`
- Optional: `winget install Cloudflare.cloudflared` (for cellular remote tunnel)

### Launching the Application
Double-click `start_scanner.bat` or run:

```bash
python server.py
```

### Accessing the Dashboard
- **Laptop / Desktop:** `http://localhost:8080`
- **Phone (Same Wi-Fi):** Displayed on terminal startup and in the in-app Phone QR modal (e.g. `http://<local-ip>:8080`)
- **Remote Cellular (4G/5G):** Click "Phone QR" &rarr; "Launch Cloudflare Global Tunnel" inside the web terminal.

---

## API Endpoints

- `GET /api/scan`: Retrieves ranked market opportunities and consensus scores.
- `GET /api/scan/force`: Forces an immediate synchronous rescan of all markets.
- `GET /api/asset/{symbol}`: Returns deep walk-forward backtest, MTF matrix, and recent candles.
- `GET /api/scan/custom?symbol={ticker}`: Scans any arbitrary global symbol on-the-fly.
- `GET /api/journal`: Returns forward-tested trade records and real-world win/loss statistics.
- `POST /api/journal/log`: Manually or programmatically logs a trade setup.
- `GET /api/mtf/{symbol}`: Returns multi-timeframe trend alignment scores.
- `GET /api/pulse`: System health, RAM usage, CPU %, and thread counts.
- `GET /api/macro-news`: Real-time financial headlines and CBOE VIX volatility regime.
- `POST /api/tunnel/start`: Launches Cloudflare tunnel.
- `POST /api/tunnel/stop`: Terminates active Cloudflare tunnel.
- `GET /api/tunnel/status`: Returns active tunnel state and public URL.
