"""
Task 01: NIFTY50 Option Symbol Filtering (CSV)
Arkalogi Internship - Priyanshu Kumar

Objective:
- Extract and process options and futures contracts from Zerodha/Kite instrument CSV.
- Handcrafted string slicing logic without Regular Expressions (Regex) as per constraints.
- Filter instruments starting with NIFTY50 constituents and ending with 'CE', 'PE', or 'FUT'.
- Extract expiry dates and save filtered dataset to CSV.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

NIFTY_50_SYMBOLS = {
    'ADANIENT', 'ADANIPORTS', 'APOLLOHOSP', 'ASIANPAINT', 'AXISBANK',
    'BAJAJ-AUTO', 'BAJFINANCE', 'BAJAJFINSV', 'BPCL', 'BHARTIARTL',
    'BRITANNIA', 'CIPLA', 'COALINDIA', 'DIVISLAB', 'DRREDDY',
    'EICHERMOT', 'GRASIM', 'HCLTECH', 'HDFCBANK', 'HDFCLIFE',
    'HEROMOTOCO', 'HINDALCO', 'HINDUNILVR', 'ICICIBANK', 'ITC',
    'INDUSINDBK', 'INFY', 'JSWSTEEL', 'KOTAKBANK', 'LT',
    'M&M', 'MARUTI', 'NTPC', 'NESTLEIND', 'ONGC',
    'POWERGRID', 'RELIANCE', 'SBILIFE', 'SBIN', 'SUNPHARMA',
    'TCS', 'TATACONSUM', 'TATAMOTORS', 'TATASTEEL', 'TECHM',
    'TITAN', 'ULTRACEMCO', 'UPL', 'WIPRO'
}

MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
          'jul', 'aug', 'sep', 'oct', 'nov', 'dec']


def extract_date_handcrafted(text: str) -> str:
    """
    Extract expiry date from trading symbol using handcrafted string slicing.
    Constraint: NO REGEX ALLOWED.
    Example: 'NIFTY24JUL24500CE' -> '24JUL'
             'BANKNIFTY30JAN2548000PE' -> '30JAN'
    """
    if not isinstance(text, str):
        return None

    text_lower = text.lower()
    for month in MONTHS:
        idx = text_lower.find(month)
        if idx != -1:
            i = idx - 1
            digits = ''
            while i >= 0 and text_lower[i].isdigit():
                digits = text_lower[i] + digits
                i -= 1
            if digits:
                return f"{digits}{month.upper()}"
    return None


def filter_nfo_contracts(input_csv: str, output_csv: str) -> pd.DataFrame:
    """
    Read instrument CSV, filter NFO segment with CE/PE/FUT suffix,
    extract expiry, and save sorted results.
    """
    print(f"[*] Reading master instrument file: {input_csv}")
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"Input file not found: {input_csv}")

    df = pd.read_csv(input_csv)
    print(f"[+] Total instruments loaded: {len(df):,}")

    # 1. Filter exchange/segment containing NFO
    if 'exchange' in df.columns:
        df_nfo = df[df['exchange'].astype(str).str.contains('NFO', case=False, na=False)].copy()
    else:
        df_nfo = df.copy()

    # 2. Filter suffixes CE, PE, FUT
    valid_suffixes = ('CE', 'PE', 'FUT')
    df_nfo = df_nfo[df_nfo['tradingsymbol'].astype(str).str.endswith(valid_suffixes)].copy()
    print(f"[+] NFO Options & Futures matched: {len(df_nfo):,}")

    # 3. Extract expiry date using handcrafted slicing
    print("[*] Extracting expiry date using handcrafted string slicing (No Regex)...")
    df_nfo['expiry_date_extracted'] = df_nfo['tradingsymbol'].apply(extract_date_handcrafted)

    # 4. Save results
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_nfo.to_csv(output_csv, index=False)
    print(f"[✓] Saved filtered contracts to: {output_csv} ({len(df_nfo):,} records)")

    return df_nfo


def filter_equity_nifty50(input_csv: str, output_csv: str) -> pd.DataFrame:
    """
    Extract NIFTY 50 equity stock instruments from master CSV.
    """
    print(f"\n[*] Filtering NIFTY50 Equity instruments...")
    df = pd.read_csv(input_csv)

    mask = (
        (df['exchange'] == 'NSE') &
        (df['segment'] == 'NSE') &
        (df['instrument_type'] == 'EQ') &
        (df['tradingsymbol'].isin(NIFTY_50_SYMBOLS))
    )
    nifty50_df = df[mask].copy().sort_values('tradingsymbol')

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    nifty50_df.to_csv(output_csv, index=False)
    print(f"[✓] Saved NIFTY50 stocks to: {output_csv} ({len(nifty50_df)} stocks)")

    return nifty50_df


def main():
    base_dir = os.path.dirname(__file__)
    input_file = os.path.join(base_dir, 'data', 'nse_master_raw.csv')
    output_contracts = os.path.join(base_dir, 'data', 'filtered_contracts_with_date.csv')
    output_stocks = os.path.join(base_dir, 'data', 'nifty50_stocks.csv')

    print("=" * 65)
    print(" TASK 01: NIFTY50 OPTION SYMBOL FILTERING (NO REGEX)")
    print("=" * 65)

    if not os.path.exists(input_file):
        print(f"[!] Warning: {input_file} does not exist.")
        return

    filter_nfo_contracts(input_file, output_contracts)
    filter_equity_nifty50(input_file, output_stocks)

    print("\n[✓] Task 01 completed successfully!")


if __name__ == '__main__':
    main()
