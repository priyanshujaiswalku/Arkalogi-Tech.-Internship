"""
Task 07: Entry/Exit Trade Simulation Engine
Arkalogi Internship - Priyanshu Kumar

Core logic for backtesting intraday trade entries and exits across 1-minute candle datasets.
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List


def simulate_trade_range(
    symbol: str,
    entry_date: str,
    exit_date: str,
    entry_time: str,
    exit_time: str,
    position_type: str,
    time_frame: str = '1m',
    data_dir: str = None
) -> Dict[str, Any]:
    """
    Simulates trades across a date range using 1-minute historical data files.
    """
    symbol_clean = symbol.lower().strip()
    position_type_clean = position_type.lower().strip()
    log_messages = []
    results = []

    current_date = pd.to_datetime(entry_date)
    final_date = pd.to_datetime(exit_date)

    while current_date <= final_date:
        date_str = current_date.strftime("%Y-%m-%d")

        try:
            # Look for matching CSV
            file_name = f"{symbol_clean}_{date_str}.csv"
            file_path = os.path.join(data_dir, file_name) if data_dir else file_name

            if not os.path.exists(file_path):
                # Try uppercase as well
                alt_name = f"{symbol_clean.upper()}_{date_str}.csv"
                alt_path = os.path.join(data_dir, alt_name) if data_dir else alt_name
                if os.path.exists(alt_path):
                    file_path = alt_path
                else:
                    log_messages.append(f"No candle data found for {symbol.upper()} on {date_str}")
                    current_date += timedelta(days=1)
                    continue

            df = pd.read_csv(file_path)
            log_messages.append(f"Loaded {len(df)} candles for {symbol.upper()} on {date_str}")

            if 'Time' not in df.columns or 'Close' not in df.columns:
                log_messages.append(f"Malformed columns in {file_name}")
                current_date += timedelta(days=1)
                continue

            # Standardize time format to HH:MM
            try:
                df['Time_HHMM'] = pd.to_datetime(df['Time'].astype(str), format='%H:%M:%S', errors='coerce').dt.strftime('%H:%M')
            except Exception:
                df['Time_HHMM'] = df['Time'].astype(str).str[:5]

            entry_row = df[df['Time_HHMM'] == entry_time]
            exit_row = df[df['Time_HHMM'] == exit_time]

            if entry_row.empty or exit_row.empty:
                log_messages.append(f"Entry ({entry_time}) or Exit ({exit_time}) timestamp missing on {date_str}")
                current_date += timedelta(days=1)
                continue

            entry_price = float(entry_row.iloc[0]['Close'])
            exit_price = float(exit_row.iloc[0]['Close'])

            if position_type_clean == 'short':
                pnl = entry_price - exit_price
                return_pct = ((entry_price - exit_price) / entry_price) * 100
            else:
                pnl = exit_price - entry_price
                return_pct = ((exit_price - entry_price) / entry_price) * 100

            results.append({
                'entry_date': date_str,
                'exit_date': date_str,
                'entry_time': entry_time,
                'exit_time': exit_time,
                'Time Frame': time_frame,
                'Symbol': symbol.upper(),
                'Position Type': position_type.capitalize(),
                'Date': date_str,
                'Entry_Price': round(entry_price, 2),
                'Exit_Price': round(exit_price, 2),
                'PnL': round(float(pnl), 2),
                'Return_Pct': round(float(return_pct), 2)
            })
            log_messages.append(f"Trade Executed on {date_str} | Entry: ₹{entry_price:.2f} | Exit: ₹{exit_price:.2f} | PnL: ₹{pnl:+.2f}")

        except Exception as e:
            log_messages.append(f"Error processing {date_str}: {str(e)}")

        current_date += timedelta(days=1)

    # Chart payload
    pnl_chart = {
        "labels": [r['Date'] for r in results],
        "pnl": [r['PnL'] for r in results],
        "cumulative_pnl": list(pd.Series([r['PnL'] for r in results]).cumsum().round(2)) if results else []
    }

    return {
        'results': results,
        'log_messages': log_messages,
        'pnl_chart': pnl_chart,
        'total_pnl': round(sum(r['PnL'] for r in results), 2) if results else 0.0,
        'total_trades': len(results)
    }
