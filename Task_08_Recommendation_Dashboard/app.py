"""
Task 08: Strategy Recommendation Dashboard - Flask Web Application
Arkalogi Internship - Priyanshu Kumar

Endpoints:
- GET  /dashboard           : Technical Strategy Dashboard
- POST /dashboard           : Evaluate Indicator Parameters & Generate Real-Time Recommendation
- GET  /api/indices         : Benchmark Index Performance Feeds (NIFTY50, SENSEX, MidCap)
"""

import os
import sys
import pandas as pd
from flask import Flask, render_template, request, jsonify
from indicators import calculate_sma, calculate_ema, calculate_rsi, calculate_stoch_rsi
from recommendation import generate_recommendation
from index_tracker import get_market_indices

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
STOCK_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Task_07_Trade_Simulation', 'data'))


@app.route('/', methods=['GET'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    indices = get_market_indices(data_dir=DATA_DIR)

    if request.method == 'GET':
        return render_template("dashboard.html", indices=indices)

    symbol = request.form.get('symbol', 'sbin').lower().strip()
    date = request.form.get('date', '2025-06-03').strip()
    selected_indicators = request.form.getlist('indicators') or ['SMA', 'EMA', 'RSI']

    # Locate stock intraday dataset
    file_path = os.path.join(STOCK_DATA_DIR, f"{symbol}_{date}.csv")
    if not os.path.exists(file_path):
        file_path = os.path.join(STOCK_DATA_DIR, f"{symbol.upper()}_{date}.csv")

    if not os.path.exists(file_path):
        error_msg = f"Data not found for {symbol.upper()} on {date}. Please ensure historical candle data exists."
        return render_template("dashboard.html", error=error_msg, indices=indices)

    df = pd.read_csv(file_path)
    df['Symbol'] = symbol.upper()
    df['Date'] = date
    if 'Time' in df.columns:
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'].astype(str), errors='coerce')
    else:
        df['Datetime'] = pd.date_range(start=f"{date} 09:15", periods=len(df), freq='1min')

    if 'SMA' in selected_indicators:
        df = calculate_sma(df, period=14)
    if 'EMA' in selected_indicators:
        df = calculate_ema(df, period=14)
    if 'RSI' in selected_indicators:
        df = calculate_rsi(df, period=14)
    if 'StochRSI' in selected_indicators:
        df = calculate_stoch_rsi(df, period=14)

    rec = generate_recommendation(df, selected_indicators, period=14)

    time_labels = df['Datetime'].dt.strftime('%H:%M').tolist() if hasattr(df['Datetime'].dt, 'strftime') else list(range(len(df)))

    chart_data = {
        "labels": time_labels,
        "close": df['Close'].round(2).tolist(),
        "sma": df['SMA_14'].round(2).fillna(0).tolist() if 'SMA' in selected_indicators and 'SMA_14' in df.columns else [],
        "ema": df['EMA_14'].round(2).fillna(0).tolist() if 'EMA' in selected_indicators and 'EMA_14' in df.columns else [],
        "rsi": df['RSI_14'].round(2).fillna(50).tolist() if 'RSI' in selected_indicators and 'RSI_14' in df.columns else [],
        "stochrsi": (df['StochRSI_14'] * 100).round(2).fillna(50).tolist() if 'StochRSI' in selected_indicators and 'StochRSI_14' in df.columns else []
    }

    return render_template(
        "dashboard.html",
        recommendation=rec,
        indicators=selected_indicators,
        chart_data=chart_data,
        indices=indices,
        current_symbol=symbol.upper(),
        current_date=date
    )


@app.route('/api/indices', methods=['GET'])
def api_indices():
    return jsonify(get_market_indices(data_dir=DATA_DIR))


if __name__ == '__main__':
    print("[*] Starting Task 08 Recommendation Dashboard on http://127.0.0.1:5008 ...")
    app.run(port=5008, debug=True)
