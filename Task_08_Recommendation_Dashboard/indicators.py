"""
Task 08: Technical Indicators Module
Arkalogi Internship - Priyanshu Kumar

Computes SMA, EMA, RSI, and Stochastic RSI.
"""

import pandas as pd
import numpy as np


def calculate_sma(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Calculate Simple Moving Average."""
    df[f'SMA_{period}'] = pd.to_numeric(df['Close'], errors='coerce').rolling(window=period).mean()
    return df


def calculate_ema(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Calculate Exponential Moving Average."""
    df[f'EMA_{period}'] = pd.to_numeric(df['Close'], errors='coerce').ewm(span=period, adjust=False).mean()
    return df


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Calculate Relative Strength Index (RSI)."""
    close = pd.to_numeric(df['Close'], errors='coerce')
    delta = close.diff()
    gain = delta.clip(lower=0).rolling(window=period).mean()
    loss = (-delta.clip(upper=0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, np.nan)
    df[f'RSI_{period}'] = 100 - (100 / (1 + rs))
    df[f'RSI_{period}'] = df[f'RSI_{period}'].fillna(50)
    return df


def calculate_stoch_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Calculate Stochastic RSI Oscillator (0 to 1 scale)."""
    df = calculate_rsi(df, period)
    rsi_col = f'RSI_{period}'
    min_rsi = df[rsi_col].rolling(window=period).min()
    max_rsi = df[rsi_col].rolling(window=period).max()
    denom = (max_rsi - min_rsi).replace(0, np.nan)
    df[f'StochRSI_{period}'] = ((df[rsi_col] - min_rsi) / denom).fillna(0.5)
    return df
