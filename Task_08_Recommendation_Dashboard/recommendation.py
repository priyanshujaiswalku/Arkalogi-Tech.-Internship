"""
Task 08: Multi-Indicator Strategy Recommendation Engine
Arkalogi Internship - Priyanshu Kumar

Synthesizes technical signals into a composite trade decision (Buy/Sell/Hold) with confidence scoring.
"""

import pandas as pd
from typing import Dict, List, Any


def generate_recommendation(df: pd.DataFrame, indicators: List[str], period: int = 14) -> Dict[str, Any]:
    """
    Evaluates latest candlestick against selected technical indicators to produce a recommendation.
    """
    if df.empty:
        return {"Signal": "Hold", "Confidence": 50, "Price": 0}

    last = df.iloc[-1]
    close = float(last['Close'])

    signal = "Hold"
    confidence = 50
    rsi = stoch = ema = sma = None

    if 'RSI' in indicators:
        val = last.get(f'RSI_{period}')
        if pd.notna(val):
            rsi = float(val)
            if rsi < 30:
                signal = "Buy"
                confidence += 25
            elif rsi > 70:
                signal = "Sell"
                confidence += 25

    if 'StochRSI' in indicators:
        val = last.get(f'StochRSI_{period}')
        if pd.notna(val):
            stoch = float(val)
            if stoch < 0.2:
                signal = "Buy"
                confidence += 15
            elif stoch > 0.8:
                signal = "Sell"
                confidence += 15

    if 'EMA' in indicators:
        val = last.get(f'EMA_{period}')
        if pd.notna(val):
            ema = float(val)
            if close > ema:
                confidence += 5
            else:
                confidence -= 5

    if 'SMA' in indicators:
        val = last.get(f'SMA_{period}')
        if pd.notna(val):
            sma = float(val)
            if close > sma:
                confidence += 5
            else:
                confidence -= 5

    confidence = max(0, min(confidence, 100))

    symbol_val = last.get('Symbol', 'STOCK')
    date_val = last.get('Date', 'N/A')

    return {
        "Signal": signal,
        "Confidence": int(confidence),
        "RSI": round(rsi, 2) if rsi is not None else "-",
        "StochRSI": round(stoch, 2) if stoch is not None else "-",
        "EMA": round(ema, 2) if ema is not None else "-",
        "SMA": round(sma, 2) if sma is not None else "-",
        "Price": round(close, 2),
        "Symbol": str(symbol_val).upper(),
        "Date": str(date_val)
    }
