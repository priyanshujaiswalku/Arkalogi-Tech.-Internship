"""
Task 05: Market Insight (SMA Based Calculation Engine)
Arkalogi Internship - Priyanshu Kumar

Core calculations for SMA market insights.
"""

import os
import sys
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

# Default watchlist stocks
DEFAULT_STOCKS = [
    'SBIN.NS', 'TATAMOTORS.NS', 'RELIANCE.NS', 'INFY.NS', 'HDFCBANK.NS',
    'ITC.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'LT.NS', 'TCS.NS'
]


def calculate_sma(df: pd.DataFrame, sma_length: int = 14) -> pd.Series:
    """Calculate Simple Moving Average on Close prices."""
    close_series = pd.to_numeric(df['Close'], errors='coerce')
    return close_series.rolling(window=sma_length).mean()


def get_stock_data(symbol: str, data_dir: str = None, days: int = 45) -> pd.DataFrame:
    """
    Load stock OHLC data. Tries local cache first, then falls back to yfinance.
    """
    clean_sym = symbol if symbol.endswith('.NS') else f"{symbol}.NS"
    clean_name = clean_sym.replace('.NS', '')

    # Check local CSV cache
    if data_dir and os.path.exists(data_dir):
        possible_paths = [
            os.path.join(data_dir, f"{clean_sym}.csv"),
            os.path.join(data_dir, f"{clean_name}.csv"),
            os.path.join(data_dir, f"{clean_sym}")
        ]
        for p in possible_paths:
            if os.path.exists(p):
                df = pd.read_csv(p)
                if 'Close' in df.columns and len(df) > 0:
                    return df

    # Fallback to yfinance if not cached
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=days)
        df = yf.download(clean_sym, start=start_date, end=end_date, interval='1d', progress=False)
        if not df.empty:
            # Flatten multi-index columns if yfinance returns them
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
    except Exception as e:
        print(f"[!] Error fetching {clean_sym} via yfinance: {e}")

    return pd.DataFrame()


def compute_market_insight(sma_length: int = 14, data_dir: str = None, stocks: List[str] = None) -> Dict[str, Any]:
    """
    Classify stocks into above_sma and below_sma based on latest close vs calculated SMA.
    """
    stocks_to_check = stocks or DEFAULT_STOCKS
    above_sma = []
    below_sma = []
    details = []

    for stock in stocks_to_check:
        df = get_stock_data(stock, data_dir=data_dir)
        stock_name = stock.replace('.NS', '')

        if df.empty or len(df) < sma_length:
            continue

        sma_series = calculate_sma(df, sma_length)
        latest_close = float(pd.to_numeric(df['Close'], errors='coerce').dropna().iloc[-1])
        latest_sma = float(sma_series.dropna().iloc[-1]) if not sma_series.dropna().empty else None

        if latest_sma is None or np.isnan(latest_sma):
            continue

        diff_pct = ((latest_close - latest_sma) / latest_sma) * 100

        item = {
            'symbol': stock_name,
            'close': round(latest_close, 2),
            'sma': round(latest_sma, 2),
            'sma_length': sma_length,
            'diff_pct': round(diff_pct, 2),
            'status': 'ABOVE' if latest_close >= latest_sma else 'BELOW'
        }
        details.append(item)

        if latest_close >= latest_sma:
            above_sma.append(stock_name)
        else:
            below_sma.append(stock_name)

    return {
        'sma_length': sma_length,
        'above_sma': above_sma,
        'below_sma': below_sma,
        'details': details
    }
