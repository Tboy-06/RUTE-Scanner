"""
RuteVisuals Engine - Proprietary SVG & Visual Trading Diagram Generator
Inspired by high-end editorial diagram architectures (diagram-design concept),
completely rebuilt and customized specifically for institutional trade visualization.

Generates self-contained, responsive vector graphics:
- RuteRiskLadder: Vertical price ladder showing Entry, Invalidation (SL), and Expansion Targets (TP).
- RuteConfluenceRadar: Multi-strategy consensus polygon matrix.
- RuteEquitySpark: Geometric trade equity progression curve.
"""

from typing import Dict, Any, List


class RuteVisuals:
    """Proprietary SVG rendering engine for RUTE financial dashboards."""

    @staticmethod
    def render_risk_ladder(entry: float, sl: float, tp1: float, tp2: float, action: str) -> str:
        """Generates an editorial SVG price ladder with defined liquidity & target bands."""
        is_buy = action.upper() == "BUY"
        min_p = sl if is_buy else tp2
        max_p = tp2 if is_buy else sl
        p_range = max(max_p - min_p, entry * 0.001)

        def to_y(price: float) -> float:
            return round(90 - ((price - min_p) / p_range * 70), 1)

        y_entry = to_y(entry)
        y_sl = to_y(sl)
        y_tp1 = to_y(tp1)
        y_tp2 = to_y(tp2)

        sl_color = "#ef4444"
        tp_color = "#10b981"
        entry_color = "#06b6d4"

        return f"""
        <svg viewBox="0 0 320 100" class="w-full h-24 my-1 overflow-visible" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="tpGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="{tp_color}" stop-opacity="0.15"/>
              <stop offset="100%" stop-color="{tp_color}" stop-opacity="0.02"/>
            </linearGradient>
            <linearGradient id="slGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="{sl_color}" stop-opacity="0.02"/>
              <stop offset="100%" stop-color="{sl_color}" stop-opacity="0.15"/>
            </linearGradient>
          </defs>

          <!-- Expansion Zone (TP) -->
          <rect x="10" y="{min(y_entry, y_tp2)}" width="300" height="{abs(y_entry - y_tp2)}" fill="url(#tpGrad)" rx="6"/>
          <!-- Risk Zone (SL) -->
          <rect x="10" y="{min(y_entry, y_sl)}" width="300" height="{abs(y_entry - y_sl)}" fill="url(#slGrad)" rx="6"/>

          <!-- TP2 Marker -->
          <line x1="20" y1="{y_tp2}" x2="300" y2="{y_tp2}" stroke="{tp_color}" stroke-width="1.2" stroke-dasharray="2,3"/>
          <text x="25" y="{y_tp2 - 3}" fill="{tp_color}" font-size="9" font-family="JetBrains Mono" font-weight="700">TP2 {tp2:.4f}</text>

          <!-- TP1 Marker -->
          <line x1="20" y1="{y_tp1}" x2="300" y2="{y_tp1}" stroke="{tp_color}" stroke-width="1.5" stroke-dasharray="4,3"/>
          <circle cx="20" cy="{y_tp1}" r="3" fill="{tp_color}"/>
          <text x="30" y="{y_tp1 - 3}" fill="{tp_color}" font-size="9" font-family="JetBrains Mono" font-weight="700">TP1 {tp1:.4f}</text>

          <!-- Entry Node -->
          <line x1="20" y1="{y_entry}" x2="300" y2="{y_entry}" stroke="{entry_color}" stroke-width="2"/>
          <circle cx="20" cy="{y_entry}" r="4.5" fill="{entry_color}"/>
          <text x="32" y="{y_entry - 4}" fill="{entry_color}" font-size="10" font-family="JetBrains Mono" font-weight="800">ENTRY {entry:.4f}</text>

          <!-- Stop Loss Marker -->
          <line x1="20" y1="{y_sl}" x2="300" y2="{y_sl}" stroke="{sl_color}" stroke-width="1.5" stroke-dasharray="4,3"/>
          <circle cx="20" cy="{y_sl}" r="3" fill="{sl_color}"/>
          <text x="30" y="{y_sl + 11}" fill="{sl_color}" font-size="9" font-family="JetBrains Mono" font-weight="700">SL {sl:.4f}</text>
        </svg>
        """.strip()

    @staticmethod
    def render_confluence_radar(strategies: List[Dict[str, Any]]) -> str:
        """Generates a multi-axis strategy confluence SVG polygon."""
        if not strategies:
            return ""

        cx, cy, r = 70, 70, 50
        num_strats = len(strategies)
        points = []

        import math
        for i, strat in enumerate(strategies):
            angle = (2 * math.pi / num_strats) * i - (math.pi / 2)
            wr = strat.get("backtest", {}).get("win_rate", 50.0) / 100.0
            dist = r * (0.3 + (wr * 0.7))
            px = cx + dist * math.cos(angle)
            py = cy + dist * math.sin(angle)
            points.append(f"{px:.1f},{py:.1f}")

        polygon_str = " ".join(points)

        return f"""
        <svg viewBox="0 0 140 140" class="w-28 h-28 mx-auto overflow-visible" xmlns="http://www.w3.org/2000/svg">
          <!-- Background Grid Rings -->
          <circle cx="{cx}" cy="{cy}" r="{r * 0.33:.1f}" fill="none" stroke="#1e293b" stroke-width="1"/>
          <circle cx="{cx}" cy="{cy}" r="{r * 0.66:.1f}" fill="none" stroke="#1e293b" stroke-width="1"/>
          <circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="#334155" stroke-width="1"/>

          <!-- Radar Shape -->
          <polygon points="{polygon_str}" fill="rgba(6, 182, 212, 0.25)" stroke="#06b6d4" stroke-width="1.8"/>
          <circle cx="{cx}" cy="{cy}" r="2" fill="#06b6d4"/>
        </svg>
        """.strip()
