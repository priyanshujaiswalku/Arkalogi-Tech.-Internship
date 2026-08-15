"""
Task 02: Trade PnL & Drawdown Analysis (JSON / Excel)
Arkalogi Internship - Priyanshu Kumar

Objective:
- Load trade executions from JSON/Excel.
- Calculate PnL for each trade based on BUY (Long) vs SELL (Short) sides.
- Calculate Cumulative PnL, Peak Equity, and Drawdown.
- Compute performance metrics:
    * Total & Average PnL
    * Top 5 Most Profitable Trades
    * Maximum Drawdown (Max DD in INR and %)
    * Win Rate (%) & Profit Factor
- Export summary metrics to result.csv, top_5_profits.csv, and task_02_with_pnl.xlsx.
"""

import os
import sys
import json
import pandas as pd
import numpy as np

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def seconds_to_time_str(val) -> str:
    """Convert time in seconds (e.g. 34800) or strings to HH:MM:SS."""
    if pd.isna(val):
        return ""
    if isinstance(val, (int, float)):
        val = int(val)
        hours = val // 3600
        minutes = (val % 3600) // 60
        seconds = val % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return str(val)


def load_trade_data(json_path: str = None, excel_path: str = None) -> pd.DataFrame:
    """
    Load trade data from JSON or Excel format into a Pandas DataFrame.
    """
    if json_path and os.path.exists(json_path):
        print(f"[*] Loading trade records from JSON: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        if isinstance(raw_data, dict) and 'trades' in raw_data:
            df = pd.DataFrame(raw_data['trades'])
        elif isinstance(raw_data, list):
            df = pd.DataFrame(raw_data)
        else:
            df = pd.DataFrame([raw_data])
    elif excel_path and os.path.exists(excel_path):
        print(f"[*] Loading trade records from Excel: {excel_path}")
        df = pd.read_excel(excel_path)
    else:
        raise FileNotFoundError("Neither JSON nor Excel data file was found.")

    print(f"[+] Loaded {len(df):,} trades.")
    return df


def calculate_trade_pnl(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate PnL for each trade according to execution side:
    - Long (BUY): (Exit Price - Entry Price) * Qty
    - Short (SELL): (Entry Price - Exit Price) * Qty
    """
    df = df.copy()
    df['side'] = df['side'].astype(str).str.upper()

    df['pnl'] = df.apply(
        lambda row: (row['exit_price'] - row['entry_price']) * row['qty']
        if row['side'] == 'BUY'
        else (row['entry_price'] - row['exit_price']) * row['qty'],
        axis=1
    ).round(2)

    return df


def calculate_drawdown_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort trades chronologically and calculate cumulative PnL, peak equity, and drawdown.
    """
    df = df.copy()

    # Parse entry date cleanly
    if df['entry_date'].dtype == object:
        df['parsed_date'] = pd.to_datetime(df['entry_date'].astype(str), errors='coerce')
    else:
        df['parsed_date'] = pd.to_datetime(df['entry_date'].astype(str), format='%y%m%d', errors='coerce')

    # Convert numeric time to formatted string if needed
    if 'entry_time_formatted' not in df.columns:
        df['entry_time_formatted'] = df['entry_time'].apply(seconds_to_time_str)

    if 'exit_time_formatted' not in df.columns:
        df['exit_time_formatted'] = df['exit_time'].apply(seconds_to_time_str)

    # Sort chronologically
    df = df.sort_values(by=['parsed_date', 'entry_time']).reset_index(drop=True)

    # Cumulative PnL
    df['cumulative_pnl'] = df['pnl'].cumsum().round(2)

    # Peak equity (cummax)
    df['cum_max'] = df['cumulative_pnl'].cummax().round(2)

    # Drawdown = cumulative_pnl - cum_max
    df['drawdown'] = (df['cumulative_pnl'] - df['cum_max']).round(2)

    # Drawdown percentage
    df['drawdown_pct'] = np.where(
        df['cum_max'] > 0,
        ((df['drawdown'] / df['cum_max']) * 100).round(2),
        0.0
    )

    return df


def generate_performance_report(df: pd.DataFrame, output_dir: str):
    """
    Generate comprehensive analytics and export CSV / Excel reports.
    """
    os.makedirs(output_dir, exist_ok=True)

    total_trades = len(df)
    winning_trades = df[df['pnl'] > 0]
    losing_trades = df[df['pnl'] < 0]
    breakeven_trades = df[df['pnl'] == 0]

    total_pnl = df['pnl'].sum()
    avg_pnl = df['pnl'].mean()
    win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0

    gross_profit = winning_trades['pnl'].sum()
    gross_loss = abs(losing_trades['pnl'].sum())
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else float('inf')

    max_drawdown = df['drawdown'].min()
    max_drawdown_pct = df['drawdown_pct'].min()

    # Top 5 Profitable Trades
    top_5_trades = df.nlargest(5, 'pnl')[['symbol', 'side', 'entry_date', 'entry_time_formatted', 'entry_price', 'exit_price', 'qty', 'pnl']]
    top_5_path = os.path.join(output_dir, 'top_5_profits.csv')
    top_5_trades.to_csv(top_5_path, index=False)

    # Summary Metrics DataFrame
    summary_metrics = {
        'Metric': [
            'Total Trades',
            'Winning Trades',
            'Losing Trades',
            'Breakeven Trades',
            'Win Rate (%)',
            'Total Net PnL (INR)',
            'Average PnL per Trade (INR)',
            'Gross Profit (INR)',
            'Gross Loss (INR)',
            'Profit Factor',
            'Max Drawdown (INR)',
            'Max Drawdown (%)'
        ],
        'Value': [
            total_trades,
            len(winning_trades),
            len(losing_trades),
            len(breakeven_trades),
            round(win_rate, 2),
            round(total_pnl, 2),
            round(avg_pnl, 2),
            round(gross_profit, 2),
            round(gross_loss, 2),
            round(profit_factor, 2) if profit_factor != float('inf') else 'N/A',
            round(max_drawdown, 2),
            round(max_drawdown_pct, 2)
        ]
    }
    summary_df = pd.DataFrame(summary_metrics)
    summary_path = os.path.join(output_dir, 'result.csv')
    summary_df.to_csv(summary_path, index=False)

    # Export full dataset with PnL & Drawdown to Excel
    excel_path = os.path.join(output_dir, 'task_02_with_pnl.xlsx')
    export_df = df.drop(columns=['parsed_date'], errors='ignore')
    export_df.to_excel(excel_path, index=False)

    # Print Summary Table
    print("\n" + "=" * 65)
    print(" 📈 TRADE PERFORMANCE & DRAWDOWN SUMMARY METRICS")
    print("=" * 65)
    for _, row in summary_df.iterrows():
        print(f"  {row['Metric']:<30} : {row['Value']}")
    print("=" * 65)

    print(f"\n[✓] Top 5 Profitable Trades saved to: {top_5_path}")
    print(f"[✓] Summary metrics saved to: {summary_path}")
    print(f"[✓] Complete trade audit saved to: {excel_path}")


def main():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    json_path = os.path.join(data_dir, 'task_02.json')
    excel_path = os.path.join(data_dir, 'task_02.xlsx')

    print("=" * 65)
    print(" TASK 02: TRADE PnL & DRAWDOWN ANALYSIS")
    print("=" * 65)

    df = load_trade_data(json_path=json_path, excel_path=excel_path)
    df_pnl = calculate_trade_pnl(df)
    df_analyzed = calculate_drawdown_metrics(df_pnl)
    generate_performance_report(df_analyzed, data_dir)

    print("\n[✓] Task 02 completed successfully!")


if __name__ == '__main__':
    main()
