"""
Task 08: Benchmark Index Tracker (yfinance / offline cached data)
Arkalogi Internship - Priyanshu Kumar

Tracks key Indian market indices: NIFTY 50, SENSEX, and BSE MidCap.
"""

import os
import yfinance as yf
import pandas as pd
from typing import List, Dict, Any

INDEX_SYMBOLS = {
    'NIFTY 50': '^NSEI',
    'SENSEX': '^BSESN',
    'BSE MidCap': 'BSE-MIDCAP.BO'
}


def get_market_indices(data_dir: str = None) -> List[Dict[str, Any]]:
    """
    Fetch price quotes and intraday performance for major benchmark indices.
    """
    indices_data = []

    for name, symbol in INDEX_SYMBOLS.items():
        price = 0.0
        change_pct = 0.0
        chart_points = []
        time_points = []

        # 1. Try local CSV first
        clean_file_key = name.replace(' ', '_')
        if data_dir and os.path.exists(data_dir):
            matches = [f for f in os.listdir(data_dir) if clean_file_key in f and f.endswith('.csv')]
            if matches:
                df = pd.read_csv(os.path.join(data_dir, matches[0]))
                if 'Close' in df.columns and len(df) > 1:
                    close_vals = pd.to_numeric(df['Close'], errors='coerce').dropna()
                    price = float(close_vals.iloc[-1])
                    prev = float(close_vals.iloc[0])
                    change_pct = ((price - prev) / prev) * 100
                    chart_points = close_vals.tail(30).round(2).tolist()
                    time_points = df['Date'].tail(30).tolist() if 'Date' in df.columns else list(range(len(chart_points)))

        # 2. Fallback to yfinance if not populated
        if price == 0.0:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='5d', interval='15m')
                if not hist.empty and len(hist) > 1:
                    price = float(hist['Close'].iloc[-1])
                    prev_close = float(hist['Close'].iloc[-2])
                    change_pct = ((price - prev_close) / prev_close) * 100
                    chart_points = hist['Close'].tail(25).round(2).tolist()
                    time_points = hist.index.strftime('%H:%M').tail(25).tolist()
            except Exception:
                pass

        if price > 0.0:
            indices_data.append({
                'name': name,
                'symbol': symbol,
                'price': round(price, 2),
                'change_pct': round(change_pct, 2),
                'data': chart_points,
                'time': time_points
            })

    return indices_data
