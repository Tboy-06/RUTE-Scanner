"""
RUTE Forward-Test Trade Journal Engine
Stores recommended high-probability setups in local SQLite database.
Continuously forward-tests them against live market prices to track real-world
TP/SL hit rates, forward win rates, and strategy efficacy.
"""

import os
import time
import sqlite3
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger("trade_journal")
DB_PATH = os.path.join(os.path.dirname(__file__), "trade_journal.db")


def init_db():
    """Initializes SQLite database tables."""
    conn = sqlite3.connect(DB_PATH, timeout=15)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal_trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            datetime_str TEXT NOT NULL,
            symbol TEXT NOT NULL,
            name TEXT NOT NULL,
            market_type TEXT NOT NULL,
            action TEXT NOT NULL,
            strategy TEXT NOT NULL,
            entry_price REAL NOT NULL,
            sl REAL NOT NULL,
            tp1 REAL NOT NULL,
            tp2 REAL NOT NULL,
            rr REAL NOT NULL,
            win_rate REAL NOT NULL,
            profit_factor REAL NOT NULL,
            confluence_score INTEGER NOT NULL,
            status TEXT DEFAULT 'ACTIVE',
            current_price REAL,
            current_pnl_pct REAL DEFAULT 0.0,
            exit_price REAL,
            closed_at TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


class TradeJournal:
    @staticmethod
    def log_setup(setup: Dict[str, Any]) -> Optional[int]:
        """
        Logs a trade setup if not already logged recently (within last 3 hours for same symbol+action).
        """
        symbol = setup.get("symbol")
        action = setup.get("action")
        if not symbol or not action:
            return None

        conn = sqlite3.connect(DB_PATH, timeout=15)
        cursor = conn.cursor()
        
        # Check duplicate in last 3 hours
        three_hours_ago = int(time.time()) - (3 * 3600)
        cursor.execute("""
            SELECT id FROM journal_trades 
            WHERE symbol = ? AND action = ? AND timestamp > ? AND status = 'ACTIVE'
        """, (symbol, action, three_hours_ago))
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return existing[0]

        now = int(time.time())
        dt_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        cursor.execute("""
            INSERT INTO journal_trades (
                timestamp, datetime_str, symbol, name, market_type, action,
                strategy, entry_price, sl, tp1, tp2, rr, win_rate,
                profit_factor, confluence_score, status, current_price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'ACTIVE', ?)
        """, (
            now,
            dt_str,
            symbol,
            setup.get("name", symbol),
            setup.get("type", "unknown"),
            action,
            setup.get("strategy", "Unknown Strategy"),
            setup.get("entry", 0.0),
            setup.get("sl", 0.0),
            setup.get("tp1", 0.0),
            setup.get("tp2", 0.0),
            setup.get("rr", 1.5),
            setup.get("win_rate", 0.0),
            setup.get("profit_factor", 1.0),
            setup.get("confluence_score", 0),
            setup.get("entry", 0.0)
        ))
        trade_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return trade_id

    @staticmethod
    def update_prices(price_map: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Evaluates active trades against live market prices to detect TP/SL triggers.
        """
        conn = sqlite3.connect(DB_PATH, timeout=15)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM journal_trades WHERE status = 'ACTIVE'")
        active_trades = cursor.fetchall()
        
        updated_events = []
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        for row in active_trades:
            t_id = row["id"]
            symbol = row["symbol"]
            curr_price = price_map.get(symbol)
            if curr_price is None or curr_price <= 0:
                continue

            action = row["action"]
            entry = row["entry_price"]
            if entry <= 0:
                continue
            sl = row["sl"]
            tp1 = row["tp1"]
            tp2 = row["tp2"]

            # Calculate PnL
            if action == "BUY":
                pnl_pct = ((curr_price - entry) / entry) * 100
                if curr_price >= tp2:
                    new_status = "HIT_TP2"
                    exit_p = tp2
                elif curr_price >= tp1:
                    new_status = "HIT_TP1"
                    exit_p = tp1
                elif curr_price <= sl:
                    new_status = "HIT_SL"
                    exit_p = sl
                else:
                    new_status = "ACTIVE"
                    exit_p = None
            else: # SELL
                pnl_pct = ((entry - curr_price) / entry) * 100
                if curr_price <= tp2:
                    new_status = "HIT_TP2"
                    exit_p = tp2
                elif curr_price <= tp1:
                    new_status = "HIT_TP1"
                    exit_p = tp1
                elif curr_price >= sl:
                    new_status = "HIT_SL"
                    exit_p = sl
                else:
                    new_status = "ACTIVE"
                    exit_p = None

            pnl_pct = round(pnl_pct, 2)
            if new_status != "ACTIVE":
                cursor.execute("""
                    UPDATE journal_trades 
                    SET status = ?, current_price = ?, current_pnl_pct = ?, exit_price = ?, closed_at = ?
                    WHERE id = ?
                """, (new_status, curr_price, pnl_pct, exit_p, now_str, t_id))
                updated_events.append({
                    "id": t_id, "symbol": symbol, "status": new_status, "pnl_pct": pnl_pct
                })
            else:
                cursor.execute("""
                    UPDATE journal_trades 
                    SET current_price = ?, current_pnl_pct = ?
                    WHERE id = ?
                """, (curr_price, pnl_pct, t_id))

        conn.commit()
        conn.close()
        return updated_events

    @staticmethod
    def get_journal(limit: int = 50) -> Dict[str, Any]:
        """Retrieves forward-tested trades and overall win/loss metrics."""
        conn = sqlite3.connect(DB_PATH, timeout=15)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM journal_trades ORDER BY id DESC LIMIT ?", (limit,))
        rows = [dict(r) for r in cursor.fetchall()]
        
        # Calculate stats
        cursor.execute("SELECT COUNT(*) FROM journal_trades")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM journal_trades WHERE status IN ('HIT_TP1', 'HIT_TP2')")
        wins = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM journal_trades WHERE status = 'HIT_SL'")
        losses = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM journal_trades WHERE status = 'ACTIVE'")
        active = cursor.fetchone()[0]

        closed_total = wins + losses
        forward_win_rate = round((wins / closed_total) * 100, 1) if closed_total > 0 else 0.0

        conn.close()
        return {
            "total_logged": total,
            "active_trades": active,
            "forward_wins": wins,
            "forward_losses": losses,
            "forward_win_rate": forward_win_rate,
            "trades": rows
        }
