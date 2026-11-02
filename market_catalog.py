"""
Comprehensive Market Catalog for RUTE Scanner
Includes Top 100 Stocks & Indices, Top 100 Cryptocurrencies, and Top 60+ Forex & Commodities.
All symbols map directly to real live market feeds (Yahoo Finance v8 / Binance REST).
"""

from typing import Dict, Any, List

# -------------------------------------------------------------
# 1. TOP 100 GLOBAL STOCKS & ETFS (Mega & Large Cap Leaders)
# -------------------------------------------------------------
TOP_STOCKS_100: List[Dict[str, Any]] = [
    # Top Tech Giants & Magnificent 7
    {"symbol": "AAPL", "name": "Apple Inc.", "type": "stock", "sector": "Technology"},
    {"symbol": "MSFT", "name": "Microsoft Corp.", "type": "stock", "sector": "Technology"},
    {"symbol": "NVDA", "name": "NVIDIA Corp.", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "AMZN", "name": "Amazon.com Inc.", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "GOOGL", "name": "Alphabet Inc. (Class A)", "type": "stock", "sector": "Communication Services"},
    {"symbol": "META", "name": "Meta Platforms Inc.", "type": "stock", "sector": "Communication Services"},
    {"symbol": "TSLA", "name": "Tesla Inc.", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "AVGO", "name": "Broadcom Inc.", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "AMD", "name": "Advanced Micro Devices", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "QCOM", "name": "Qualcomm Inc.", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "INTC", "name": "Intel Corp.", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "MU", "name": "Micron Technology", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "AMAT", "name": "Applied Materials", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "TXN", "name": "Texas Instruments", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "LRCX", "name": "Lam Research", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "ADI", "name": "Analog Devices", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "ASML", "name": "ASML Holding", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "TSM", "name": "Taiwan Semiconductor", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "ARM", "name": "Arm Holdings", "type": "stock", "sector": "Semiconductors"},
    {"symbol": "PLTR", "name": "Palantir Technologies", "type": "stock", "sector": "Software"},
    {"symbol": "CRM", "name": "Salesforce Inc.", "type": "stock", "sector": "Software"},
    {"symbol": "ORCL", "name": "Oracle Corp.", "type": "stock", "sector": "Software"},
    {"symbol": "ADBE", "name": "Adobe Inc.", "type": "stock", "sector": "Software"},
    {"symbol": "NOW", "name": "ServiceNow Inc.", "type": "stock", "sector": "Software"},
    {"symbol": "INTU", "name": "Intuit Inc.", "type": "stock", "sector": "Software"},
    {"symbol": "IBM", "name": "IBM Corp.", "type": "stock", "sector": "Software"},
    {"symbol": "PANW", "name": "Palo Alto Networks", "type": "stock", "sector": "Cybersecurity"},
    {"symbol": "CRWD", "name": "CrowdStrike Holdings", "type": "stock", "sector": "Cybersecurity"},
    {"symbol": "NET", "name": "Cloudflare Inc.", "type": "stock", "sector": "Cloud"},
    {"symbol": "SNOW", "name": "Snowflake Inc.", "type": "stock", "sector": "Cloud"},
    {"symbol": "UBER", "name": "Uber Technologies", "type": "stock", "sector": "Technology"},
    {"symbol": "ABNB", "name": "Airbnb Inc.", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "NFLX", "name": "Netflix Inc.", "type": "stock", "sector": "Media"},
    {"symbol": "DIS", "name": "Walt Disney Co.", "type": "stock", "sector": "Media"},
    {"symbol": "SPOT", "name": "Spotify Technology", "type": "stock", "sector": "Media"},

    # Top Financial Leaders
    {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "type": "stock", "sector": "Financials"},
    {"symbol": "BAC", "name": "Bank of America", "type": "stock", "sector": "Financials"},
    {"symbol": "WFC", "name": "Wells Fargo & Co.", "type": "stock", "sector": "Financials"},
    {"symbol": "C", "name": "Citigroup Inc.", "type": "stock", "sector": "Financials"},
    {"symbol": "GS", "name": "Goldman Sachs Group", "type": "stock", "sector": "Financials"},
    {"symbol": "MS", "name": "Morgan Stanley", "type": "stock", "sector": "Financials"},
    {"symbol": "V", "name": "Visa Inc.", "type": "stock", "sector": "Financials"},
    {"symbol": "MA", "name": "Mastercard Inc.", "type": "stock", "sector": "Financials"},
    {"symbol": "AXP", "name": "American Express", "type": "stock", "sector": "Financials"},
    {"symbol": "BLK", "name": "BlackRock Inc.", "type": "stock", "sector": "Financials"},
    {"symbol": "SCHW", "name": "Charles Schwab Corp.", "type": "stock", "sector": "Financials"},
    {"symbol": "COIN", "name": "Coinbase Global", "type": "stock", "sector": "Financials"},

    # Top Healthcare & Biotech
    {"symbol": "LLY", "name": "Eli Lilly and Co.", "type": "stock", "sector": "Healthcare"},
    {"symbol": "UNH", "name": "UnitedHealth Group", "type": "stock", "sector": "Healthcare"},
    {"symbol": "JNJ", "name": "Johnson & Johnson", "type": "stock", "sector": "Healthcare"},
    {"symbol": "ABBV", "name": "AbbVie Inc.", "type": "stock", "sector": "Healthcare"},
    {"symbol": "MRK", "name": "Merck & Co.", "type": "stock", "sector": "Healthcare"},
    {"symbol": "PFE", "name": "Pfizer Inc.", "type": "stock", "sector": "Healthcare"},
    {"symbol": "TMO", "name": "Thermo Fisher Scientific", "type": "stock", "sector": "Healthcare"},
    {"symbol": "ABT", "name": "Abbott Laboratories", "type": "stock", "sector": "Healthcare"},
    {"symbol": "DHR", "name": "Danaher Corp.", "type": "stock", "sector": "Healthcare"},
    {"symbol": "BMY", "name": "Bristol-Myers Squibb", "type": "stock", "sector": "Healthcare"},
    {"symbol": "AMGN", "name": "Amgen Inc.", "type": "stock", "sector": "Healthcare"},
    {"symbol": "GILD", "name": "Gilead Sciences", "type": "stock", "sector": "Healthcare"},
    {"symbol": "ISRG", "name": "Intuitive Surgical", "type": "stock", "sector": "Healthcare"},
    {"symbol": "VRTX", "name": "Vertex Pharmaceuticals", "type": "stock", "sector": "Healthcare"},
    {"symbol": "REGN", "name": "Regeneron Pharma", "type": "stock", "sector": "Healthcare"},

    # Consumer & Retail Leaders
    {"symbol": "WMT", "name": "Walmart Inc.", "type": "stock", "sector": "Consumer Staples"},
    {"symbol": "COST", "name": "Costco Wholesale", "type": "stock", "sector": "Consumer Staples"},
    {"symbol": "PG", "name": "Procter & Gamble", "type": "stock", "sector": "Consumer Staples"},
    {"symbol": "KO", "name": "Coca-Cola Co.", "type": "stock", "sector": "Consumer Staples"},
    {"symbol": "PEP", "name": "PepsiCo Inc.", "type": "stock", "sector": "Consumer Staples"},
    {"symbol": "MCD", "name": "McDonald's Corp.", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "SBUX", "name": "Starbucks Corp.", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "NKE", "name": "Nike Inc.", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "HD", "name": "Home Depot", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "LOW", "name": "Lowe's Companies", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "TGT", "name": "Target Corp.", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "TJX", "name": "TJX Companies", "type": "stock", "sector": "Consumer Discretionary"},
    {"symbol": "PM", "name": "Philip Morris International", "type": "stock", "sector": "Consumer Staples"},
    {"symbol": "MO", "name": "Altria Group", "type": "stock", "sector": "Consumer Staples"},

    # Industrial, Aerospace & Energy
    {"symbol": "XOM", "name": "Exxon Mobil Corp.", "type": "stock", "sector": "Energy"},
    {"symbol": "CVX", "name": "Chevron Corp.", "type": "stock", "sector": "Energy"},
    {"symbol": "COP", "name": "ConocoPhillips", "type": "stock", "sector": "Energy"},
    {"symbol": "SLB", "name": "Schlumberger Ltd.", "type": "stock", "sector": "Energy"},
    {"symbol": "EOG", "name": "EOG Resources", "type": "stock", "sector": "Energy"},
    {"symbol": "CAT", "name": "Caterpillar Inc.", "type": "stock", "sector": "Industrials"},
    {"symbol": "DE", "name": "Deere & Co.", "type": "stock", "sector": "Industrials"},
    {"symbol": "GE", "name": "General Electric", "type": "stock", "sector": "Industrials"},
    {"symbol": "BA", "name": "Boeing Co.", "type": "stock", "sector": "Aerospace"},
    {"symbol": "LMT", "name": "Lockheed Martin", "type": "stock", "sector": "Aerospace"},
    {"symbol": "RTX", "name": "RTX Corporation", "type": "stock", "sector": "Aerospace"},
    {"symbol": "UNP", "name": "Union Pacific Corp.", "type": "stock", "sector": "Transportation"},
    {"symbol": "HON", "name": "Honeywell International", "type": "stock", "sector": "Industrials"},
    {"symbol": "UPS", "name": "United Parcel Service", "type": "stock", "sector": "Transportation"},
    {"symbol": "FDX", "name": "FedEx Corp.", "type": "stock", "sector": "Transportation"},
    {"symbol": "NEE", "name": "NextEra Energy", "type": "stock", "sector": "Utilities"},
    {"symbol": "SO", "name": "Southern Company", "type": "stock", "sector": "Utilities"},
    {"symbol": "DUK", "name": "Duke Energy", "type": "stock", "sector": "Utilities"},

    # Top Market Index ETFs
    {"symbol": "SPY", "name": "SPDR S&P 500 ETF", "type": "index", "sector": "Index ETF"},
    {"symbol": "QQQ", "name": "Invesco QQQ (Nasdaq 100)", "type": "index", "sector": "Index ETF"},
    {"symbol": "DIA", "name": "SPDR Dow Jones Industrial", "type": "index", "sector": "Index ETF"},
    {"symbol": "IWM", "name": "iShares Russell 2000 ETF", "type": "index", "sector": "Index ETF"},
    {"symbol": "SMH", "name": "VanEck Semiconductor ETF", "type": "index", "sector": "Sector ETF"},
    {"symbol": "XLF", "name": "Financial Select Sector SPDR", "type": "index", "sector": "Sector ETF"},
    {"symbol": "XLE", "name": "Energy Select Sector SPDR", "type": "index", "sector": "Sector ETF"},
    {"symbol": "XLK", "name": "Technology Select Sector SPDR", "type": "index", "sector": "Sector ETF"},
]

# -------------------------------------------------------------
# 2. TOP 100 CRYPTOCURRENCIES (By Market Cap & Liquidity)
# -------------------------------------------------------------
TOP_CRYPTO_100: List[Dict[str, Any]] = [
    # Top 10 Bluechip Layer 1s & Majors
    {"symbol": "BTC-USD", "name": "Bitcoin", "type": "crypto", "binance": "BTCUSDT"},
    {"symbol": "ETH-USD", "name": "Ethereum", "type": "crypto", "binance": "ETHUSDT"},
    {"symbol": "SOL-USD", "name": "Solana", "type": "crypto", "binance": "SOLUSDT"},
    {"symbol": "BNB-USD", "name": "Binance Coin", "type": "crypto", "binance": "BNBUSDT"},
    {"symbol": "XRP-USD", "name": "XRP (Ripple)", "type": "crypto", "binance": "XRPUSDT"},
    {"symbol": "DOGE-USD", "name": "Dogecoin", "type": "crypto", "binance": "DOGEUSDT"},
    {"symbol": "ADA-USD", "name": "Cardano", "type": "crypto", "binance": "ADAUSDT"},
    {"symbol": "AVAX-USD", "name": "Avalanche", "type": "crypto", "binance": "AVAXUSDT"},
    {"symbol": "SUI20947-USD", "name": "Sui Network", "type": "crypto", "binance": "SUIUSDT"},
    {"symbol": "LINK-USD", "name": "Chainlink", "type": "crypto", "binance": "LINKUSDT"},

    # High-Velocity Layer 1s, 2s & Protocols
    {"symbol": "NEAR-USD", "name": "NEAR Protocol", "type": "crypto", "binance": "NEARUSDT"},
    {"symbol": "DOT-USD", "name": "Polkadot", "type": "crypto", "binance": "DOTUSDT"},
    {"symbol": "LTC-USD", "name": "Litecoin", "type": "crypto", "binance": "LTCUSDT"},
    {"symbol": "BCH-USD", "name": "Bitcoin Cash", "type": "crypto", "binance": "BCHUSDT"},
    {"symbol": "SHIB-USD", "name": "Shiba Inu", "type": "crypto", "binance": "SHIBUSDT"},
    {"symbol": "PEPE24478-USD", "name": "Pepe", "type": "crypto", "binance": "PEPEUSDT"},
    {"symbol": "UNI7083-USD", "name": "Uniswap", "type": "crypto", "binance": "UNIUSDT"},
    {"symbol": "APT21794-USD", "name": "Aptos", "type": "crypto", "binance": "APTUSDT"},
    {"symbol": "FET-USD", "name": "Artificial Superintelligence", "type": "crypto", "binance": "FETUSDT"},
    {"symbol": "ICP-USD", "name": "Internet Computer", "type": "crypto", "binance": "ICPUSDT"},
    {"symbol": "TAO22974-USD", "name": "Bittensor", "type": "crypto", "binance": "TAOUSDT"},
    {"symbol": "KAS-USD", "name": "Kaspa", "type": "crypto", "binance": "KASUSDT"},
    {"symbol": "RENDER-USD", "name": "Render Token", "type": "crypto", "binance": "RENDERUSDT"},
    {"symbol": "POL-USD", "name": "Polygon (POL)", "type": "crypto", "binance": "POLUSDT"},
    {"symbol": "STX4847-USD", "name": "Stacks", "type": "crypto", "binance": "STXUSDT"},
    {"symbol": "TIA-USD", "name": "Celestia", "type": "crypto", "binance": "TIAUSDT"},
    {"symbol": "ONDO-USD", "name": "Ondo Finance", "type": "crypto", "binance": "ONDOUSDT"},
    {"symbol": "ARB11841-USD", "name": "Arbitrum", "type": "crypto", "binance": "ARBUSDT"},
    {"symbol": "OP-USD", "name": "Optimism", "type": "crypto", "binance": "OPUSDT"},
    {"symbol": "FIL-USD", "name": "Filecoin", "type": "crypto", "binance": "FILUSDT"},
    {"symbol": "HBAR-USD", "name": "Hedera", "type": "crypto", "binance": "HBARUSDT"},
    {"symbol": "INJ-USD", "name": "Injective", "type": "crypto", "binance": "INJUSDT"},
    {"symbol": "XLM-USD", "name": "Stellar", "type": "crypto", "binance": "XLMUSDT"},
    {"symbol": "ATOM-USD", "name": "Cosmos", "type": "crypto", "binance": "ATOMUSDT"},
    {"symbol": "VET-USD", "name": "VeChain", "type": "crypto", "binance": "VETUSDT"},
    {"symbol": "RUNE-USD", "name": "THORChain", "type": "crypto", "binance": "RUNEUSDT"},
    {"symbol": "AAVE-USD", "name": "Aave", "type": "crypto", "binance": "AAVEUSDT"},
    {"symbol": "GRT6733-USD", "name": "The Graph", "type": "crypto", "binance": "GRTUSDT"},
    {"symbol": "ALGO-USD", "name": "Algorand", "type": "crypto", "binance": "ALGOUSDT"},
    {"symbol": "FTM-USD", "name": "Fantom (Sonic)", "type": "crypto", "binance": "FTMUSDT"},
    {"symbol": "SEI-USD", "name": "Sei", "type": "crypto", "binance": "SEIUSDT"},
    {"symbol": "JUP-USD", "name": "Jupiter", "type": "crypto", "binance": "JUPUSDT"},
    {"symbol": "FLOKI-USD", "name": "Floki", "type": "crypto", "binance": "FLOKIUSDT"},
    {"symbol": "BONK-USD", "name": "Bonk", "type": "crypto", "binance": "BONKUSDT"},
    {"symbol": "WIF-USD", "name": "Dogwifhat", "type": "crypto", "binance": "WIFUSDT"},
    {"symbol": "PYTH-USD", "name": "Pyth Network", "type": "crypto", "binance": "PYTHUSDT"},
    {"symbol": "SAND-USD", "name": "The Sandbox", "type": "crypto", "binance": "SANDUSDT"},
    {"symbol": "MANA-USD", "name": "Decentraland", "type": "crypto", "binance": "MANAUSDT"},
    {"symbol": "AXS-USD", "name": "Axie Infinity", "type": "crypto", "binance": "AXSUSDT"},
    {"symbol": "CRV-USD", "name": "Curve DAO", "type": "crypto", "binance": "CRVUSDT"},
    {"symbol": "MKR-USD", "name": "Maker", "type": "crypto", "binance": "MKRUSDT"},
    {"symbol": "SNX-USD", "name": "Synthetix", "type": "crypto", "binance": "SNXUSDT"},
    {"symbol": "DYDX-USD", "name": "dYdX", "type": "crypto", "binance": "DYDXUSDT"},
    {"symbol": "IMX10603-USD", "name": "Immutable", "type": "crypto", "binance": "IMXUSDT"},
    {"symbol": "LDO-USD", "name": "Lido DAO", "type": "crypto", "binance": "LDOUSDT"},
    {"symbol": "FLOW-USD", "name": "Flow", "type": "crypto", "binance": "FLOWUSDT"},
    {"symbol": "EGLD-USD", "name": "MultiversX", "type": "crypto", "binance": "EGLDUSDT"},
    {"symbol": "GALA-USD", "name": "GALA", "type": "crypto", "binance": "GALAUSDT"},
    {"symbol": "CHZ-USD", "name": "Chiliz", "type": "crypto", "binance": "CHZUSDT"},
    {"symbol": "BEAM-USD", "name": "Beam", "type": "crypto", "binance": "BEAMUSDT"},
    {"symbol": "STRK-USD", "name": "Starknet", "type": "crypto", "binance": "STRKUSDT"},
    {"symbol": "WLD-USD", "name": "Worldcoin", "type": "crypto", "binance": "WLDUSDT"},
    {"symbol": "BLUR-USD", "name": "Blur", "type": "crypto", "binance": "BLURUSDT"},
    {"symbol": "PENDLE-USD", "name": "Pendle", "type": "crypto", "binance": "PENDLEUSDT"},
    {"symbol": "MINA-USD", "name": "Mina Protocol", "type": "crypto", "binance": "MINAUSDT"},
    {"symbol": "QNT-USD", "name": "Quant", "type": "crypto", "binance": "QNTUSDT"},
    {"symbol": "EOS-USD", "name": "EOS", "type": "crypto", "binance": "EOSUSDT"},
    {"symbol": "KSM-USD", "name": "Kusama", "type": "crypto", "binance": "KSMUSDT"},
    {"symbol": "KLAY-USD", "name": "Klaytn (Kaia)", "type": "crypto", "binance": "KLAYUSDT"},
    {"symbol": "GNO-USD", "name": "Gnosis", "type": "crypto", "binance": "GNOUSDT"},
    {"symbol": "COMP5692-USD", "name": "Compound", "type": "crypto", "binance": "COMPUSDT"},
    {"symbol": "FXS-USD", "name": "Frax Share", "type": "crypto", "binance": "FXSUSDT"},
    {"symbol": "1INCH-USD", "name": "1inch Network", "type": "crypto", "binance": "1INCHUSDT"},
    {"symbol": "ENS-USD", "name": "Ethereum Name Service", "type": "crypto", "binance": "ENSUSDT"},
    {"symbol": "ROSE-USD", "name": "Oasis Network", "type": "crypto", "binance": "ROSEUSDT"},
    {"symbol": "ZIL-USD", "name": "Zilliqa", "type": "crypto", "binance": "ZILUSDT"},
    {"symbol": "ENJ-USD", "name": "Enjin Coin", "type": "crypto", "binance": "ENJUSDT"},
    {"symbol": "BAT-USD", "name": "Basic Attention Token", "type": "crypto", "binance": "BATUSDT"},
    {"symbol": "RVN-USD", "name": "Ravencoin", "type": "crypto", "binance": "RVNUSDT"},
    {"symbol": "ZEC-USD", "name": "Zcash", "type": "crypto", "binance": "ZECUSDT"},
    {"symbol": "DASH-USD", "name": "Dash", "type": "crypto", "binance": "DASHUSDT"},
    {"symbol": "XTZ-USD", "name": "Tezos", "type": "crypto", "binance": "XTZUSDT"},
    {"symbol": "IOTA-USD", "name": "IOTA", "type": "crypto", "binance": "IOTAUSDT"},
    {"symbol": "KAVA-USD", "name": "Kava", "type": "crypto", "binance": "KAVAUSDT"},
    {"symbol": "OSMO-USD", "name": "Osmosis", "type": "crypto", "binance": "OSMOUSDT"},
    {"symbol": "LRC-USD", "name": "Loopring", "type": "crypto", "binance": "LRCUSDT"},
    {"symbol": "HOT-USD", "name": "Holo", "type": "crypto", "binance": "HOTUSDT"},
    {"symbol": "ANKR-USD", "name": "Ankr", "type": "crypto", "binance": "ANKRUSDT"},
    {"symbol": "AUDIO-USD", "name": "Audius", "type": "crypto", "binance": "AUDIOUSDT"},
    {"symbol": "JASMY-USD", "name": "JasmyCoin", "type": "crypto", "binance": "JASMYUSDT"},
    {"symbol": "ILV-USD", "name": "Illuvium", "type": "crypto", "binance": "ILVUSDT"},
    {"symbol": "SKL-USD", "name": "SKALE", "type": "crypto", "binance": "SKLUSDT"},
    {"symbol": "CKB-USD", "name": "Nervos Network", "type": "crypto", "binance": "CKBUSDT"},
    {"symbol": "WOO-USD", "name": "WOO Network", "type": "crypto", "binance": "WOOUSDT"},
    {"symbol": "BICO-USD", "name": "Biconomy", "type": "crypto", "binance": "BICOUSDT"},
    {"symbol": "ACH-USD", "name": "Alchemy Pay", "type": "crypto", "binance": "ACHUSDT"},
    {"symbol": "SUPER-USD", "name": "SuperVerse", "type": "crypto", "binance": "SUPERUSDT"},
    {"symbol": "API3-USD", "name": "API3", "type": "crypto", "binance": "API3USDT"},
    {"symbol": "TRB-USD", "name": "Tellor", "type": "crypto", "binance": "TRBUSDT"},
    {"symbol": "BNT-USD", "name": "Bancor", "type": "crypto", "binance": "BNTUSDT"},
    {"symbol": "GMT-USD", "name": "STEPN", "type": "crypto", "binance": "GMTUSDT"},
    {"symbol": "CELO-USD", "name": "Celo", "type": "crypto", "binance": "CELOUSDT"},
    {"symbol": "GLMR-USD", "name": "Moonbeam", "type": "crypto", "binance": "GLMRUSDT"},
    {"symbol": "TWT-USD", "name": "Trust Wallet Token", "type": "crypto", "binance": "TWTUSDT"},
    {"symbol": "MASK-USD", "name": "Mask Network", "type": "crypto", "binance": "MASKUSDT"},
    {"symbol": "ID-USD", "name": "SPACE ID", "type": "crypto", "binance": "IDUSDT"},
    {"symbol": "ARKM-USD", "name": "Arkham", "type": "crypto", "binance": "ARKMUSDT"},
    {"symbol": "MAV-USD", "name": "Maverick Protocol", "type": "crypto", "binance": "MAVUSDT"},
    {"symbol": "ACE-USD", "name": "Fusionist", "type": "crypto", "binance": "ACEUSDT"},
    {"symbol": "AI-USD", "name": "Sleepless AI", "type": "crypto", "binance": "AIUSDT"},
]

# -------------------------------------------------------------
# 3. TOP 60+ FOREX & COMMODITIES (All Majors, Crosses & Metals)
# -------------------------------------------------------------
TOP_FOREX_60: List[Dict[str, Any]] = [
    # Forex Majors
    {"symbol": "EURUSD=X", "name": "EUR/USD", "type": "forex", "pip": 0.0001},
    {"symbol": "GBPUSD=X", "name": "GBP/USD", "type": "forex", "pip": 0.0001},
    {"symbol": "USDJPY=X", "name": "USD/JPY", "type": "forex", "pip": 0.01},
    {"symbol": "AUDUSD=X", "name": "AUD/USD", "type": "forex", "pip": 0.0001},
    {"symbol": "USDCAD=X", "name": "USD/CAD", "type": "forex", "pip": 0.0001},
    {"symbol": "USDCHF=X", "name": "USD/CHF", "type": "forex", "pip": 0.0001},
    {"symbol": "NZDUSD=X", "name": "NZD/USD", "type": "forex", "pip": 0.0001},

    # Euro Crosses
    {"symbol": "EURGBP=X", "name": "EUR/GBP", "type": "forex", "pip": 0.0001},
    {"symbol": "EURJPY=X", "name": "EUR/JPY", "type": "forex", "pip": 0.01},
    {"symbol": "EURAUD=X", "name": "EUR/AUD", "type": "forex", "pip": 0.0001},
    {"symbol": "EURCAD=X", "name": "EUR/CAD", "type": "forex", "pip": 0.0001},
    {"symbol": "EURCHF=X", "name": "EUR/CHF", "type": "forex", "pip": 0.0001},
    {"symbol": "EURNZD=X", "name": "EUR/NZD", "type": "forex", "pip": 0.0001},

    # British Pound Crosses
    {"symbol": "GBPJPY=X", "name": "GBP/JPY", "type": "forex", "pip": 0.01},
    {"symbol": "GBPAUD=X", "name": "GBP/AUD", "type": "forex", "pip": 0.0001},
    {"symbol": "GBPCAD=X", "name": "GBP/CAD", "type": "forex", "pip": 0.0001},
    {"symbol": "GBPCHF=X", "name": "GBP/CHF", "type": "forex", "pip": 0.0001},
    {"symbol": "GBPNZD=X", "name": "GBP/NZD", "type": "forex", "pip": 0.0001},

    # Yen Crosses & Asian Pairs
    {"symbol": "AUDJPY=X", "name": "AUD/JPY", "type": "forex", "pip": 0.01},
    {"symbol": "CADJPY=X", "name": "CAD/JPY", "type": "forex", "pip": 0.01},
    {"symbol": "CHFJPY=X", "name": "CHF/JPY", "type": "forex", "pip": 0.01},
    {"symbol": "NZDJPY=X", "name": "NZD/JPY", "type": "forex", "pip": 0.01},

    # Other Commodity Pairs & Crosses
    {"symbol": "AUDCAD=X", "name": "AUD/CAD", "type": "forex", "pip": 0.0001},
    {"symbol": "AUDCHF=X", "name": "AUD/CHF", "type": "forex", "pip": 0.0001},
    {"symbol": "AUDNZD=X", "name": "AUD/NZD", "type": "forex", "pip": 0.0001},
    {"symbol": "CADCHF=X", "name": "CAD/CHF", "type": "forex", "pip": 0.0001},
    {"symbol": "NZDCAD=X", "name": "NZD/CAD", "type": "forex", "pip": 0.0001},
    {"symbol": "NZDCHF=X", "name": "NZD/CHF", "type": "forex", "pip": 0.0001},

    # High-Yield Liquid Exotics
    {"symbol": "USDMXN=X", "name": "USD/MXN (Mexican Peso)", "type": "forex", "pip": 0.001},
    {"symbol": "USDZAR=X", "name": "USD/ZAR (South African Rand)", "type": "forex", "pip": 0.001},
    {"symbol": "USDTRY=X", "name": "USD/TRY (Turkish Lira)", "type": "forex", "pip": 0.001},
    {"symbol": "USDSEK=X", "name": "USD/SEK (Swedish Krona)", "type": "forex", "pip": 0.001},
    {"symbol": "USDNOK=X", "name": "USD/NOK (Norwegian Krone)", "type": "forex", "pip": 0.001},
    {"symbol": "USDSGD=X", "name": "USD/SGD (Singapore Dollar)", "type": "forex", "pip": 0.0001},
    {"symbol": "USDHKD=X", "name": "USD/HKD (Hong Kong Dollar)", "type": "forex", "pip": 0.0001},
    {"symbol": "USDCNH=X", "name": "USD/CNH (Offshore Yuan)", "type": "forex", "pip": 0.0001},
    {"symbol": "USDINR=X", "name": "USD/INR (Indian Rupee)", "type": "forex", "pip": 0.01},
    {"symbol": "EURTRY=X", "name": "EUR/TRY", "type": "forex", "pip": 0.001},
    {"symbol": "EURSEK=X", "name": "EUR/SEK", "type": "forex", "pip": 0.001},
    {"symbol": "EURNOK=X", "name": "EUR/NOK", "type": "forex", "pip": 0.001},
    {"symbol": "EURPLN=X", "name": "EUR/PLN", "type": "forex", "pip": 0.0001},
    {"symbol": "GBPZAR=X", "name": "GBP/ZAR", "type": "forex", "pip": 0.001},

    # Precious & Industrial Metals
    {"symbol": "GC=F", "name": "Gold Futures (XAU/USD)", "type": "commodity", "pip": 0.1},
    {"symbol": "SI=F", "name": "Silver Futures (XAG/USD)", "type": "commodity", "pip": 0.01},
    {"symbol": "PL=F", "name": "Platinum Futures", "type": "commodity", "pip": 0.1},
    {"symbol": "PA=F", "name": "Palladium Futures", "type": "commodity", "pip": 0.5},
    {"symbol": "HG=F", "name": "Copper Futures", "type": "commodity", "pip": 0.0005},

    # Energy Commodities
    {"symbol": "CL=F", "name": "Crude Oil WTI", "type": "commodity", "pip": 0.01},
    {"symbol": "BZ=F", "name": "Brent Crude Oil", "type": "commodity", "pip": 0.01},
    {"symbol": "NG=F", "name": "Natural Gas", "type": "commodity", "pip": 0.001},
    {"symbol": "RB=F", "name": "RBOB Gasoline", "type": "commodity", "pip": 0.0001},
    {"symbol": "HO=F", "name": "Heating Oil", "type": "commodity", "pip": 0.0001},

    # Agricultural Commodities
    {"symbol": "ZC=F", "name": "Corn Futures", "type": "commodity", "pip": 0.25},
    {"symbol": "ZW=F", "name": "Wheat Futures", "type": "commodity", "pip": 0.25},
    {"symbol": "ZS=F", "name": "Soybeans Futures", "type": "commodity", "pip": 0.25},
    {"symbol": "KC=F", "name": "Coffee Futures", "type": "commodity", "pip": 0.05},
    {"symbol": "SB=F", "name": "Sugar Futures", "type": "commodity", "pip": 0.01},
    {"symbol": "CC=F", "name": "Cocoa Futures", "type": "commodity", "pip": 1.0},
]

# Combined Master Catalog
MASTER_WATCHLIST: Dict[str, List[Dict[str, Any]]] = {
    "Stocks": TOP_STOCKS_100,
    "Crypto": TOP_CRYPTO_100,
    "Forex & Commodities": TOP_FOREX_60,
}

# Core priority watchlist (first to load for immediate setups)
CORE_PRIORITY_SYMBOLS = [
    # Top Forex
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "USDCHF=X", "GBPJPY=X", "EURJPY=X",
    # Top Commodities
    "GC=F", "SI=F", "CL=F", "NG=F",
    # Top Crypto
    "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "DOGE-USD", "ADA-USD", "AVAX-USD", "SUI20947-USD", "LINK-USD",
    # Top Stocks
    "SPY", "QQQ", "NVDA", "AAPL", "MSFT", "AMZN", "META", "TSLA", "AMD", "PLTR", "JPM", "LLY"
]
