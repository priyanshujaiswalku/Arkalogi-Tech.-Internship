"""
Task 09: API Validation & Security Schemas (Pydantic v2 Compatible)
Arkalogi Internship - Priyanshu Kumar

Defines robust BaseModel request and response schemas for all financial APIs.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, List, Optional
from datetime import datetime
import re

VALID_TIMEFRAMES = {'1m', '3m', '5m', '15m', '30m', '1h', '1d'}


class MarketInsightRequest(BaseModel):
    """Schema for Market Insight SMA parameters."""
    sma_length: int = Field(default=14, ge=2, le=200, description="SMA window length between 2 and 200")
    symbols: Optional[List[str]] = Field(default=None, description="Optional custom list of stock tickers")


class EntryExitSimulationRequest(BaseModel):
    """Schema for Entry/Exit Trade Simulator API."""
    symbol: str = Field(..., min_length=1, max_length=20, description="Equity symbol (e.g., SBIN, RELIANCE)")
    entry_date: str = Field(..., description="Trade entry date (YYYY-MM-DD)")
    exit_date: str = Field(..., description="Trade exit date (YYYY-MM-DD)")
    entry_time: str = Field(..., description="Candle entry time (HH:MM)")
    exit_time: str = Field(..., description="Candle exit time (HH:MM)")
    position_type: Literal['long', 'short'] = Field(..., description="Position direction: 'long' or 'short'")
    time_frame: str = Field(default='1m', description="Candle timeframe resolution (e.g., 1m, 5m, 1h)")

    @field_validator('entry_date', 'exit_date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be formatted as YYYY-MM-DD')
        return v

    @field_validator('entry_time', 'exit_time')
    @classmethod
    def validate_time(cls, v: str) -> str:
        if not re.match(r'^(?:[01]\d|2[0-3]):[0-5]\d$', v):
            raise ValueError('Time must be formatted as 24-hour HH:MM (e.g., 09:15, 15:30)')
        return v

    @field_validator('time_frame')
    @classmethod
    def validate_time_frame(cls, v: str) -> str:
        v_clean = v.lower().strip()
        if v_clean not in VALID_TIMEFRAMES:
            raise ValueError(f"Invalid timeframe '{v}'. Allowed: {', '.join(sorted(VALID_TIMEFRAMES))}")
        return v_clean

    @field_validator('symbol')
    @classmethod
    def clean_symbol(cls, v: str) -> str:
        return v.strip().upper()


class MLPredictRequest(BaseModel):
    """Schema for ML Trade Return Prediction."""
    entry_support_distance_pct: float = Field(..., ge=0.0, le=100.0, description="Distance to support level in %")
    entry_resistance_distance_pct: float = Field(..., ge=0.0, le=100.0, description="Distance to resistance level in %")
    entry_time: str = Field(..., description="Entry time (HH:MM)")

    @field_validator('entry_time')
    @classmethod
    def validate_time(cls, v: str) -> str:
        if not re.match(r'^(?:[01]\d|2[0-3]):[0-5]\d$', v):
            raise ValueError('Time must be formatted as 24-hour HH:MM')
        return v


class TradeSimulationResult(BaseModel):
    """Response schema for a single simulated trade execution."""
    date: str
    symbol: str
    position_type: str
    entry_time: str
    exit_time: str
    entry_price: float
    exit_price: float
    pnl: float
    return_pct: float
