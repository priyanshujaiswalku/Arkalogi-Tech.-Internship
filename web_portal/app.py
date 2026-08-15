"""
Unified Arkalogi Financial Analytics & Backtesting Web Portal
Arkalogi Internship - Priyanshu Kumar

Integrates all 9 internship tasks into a production-grade Flask web portal.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, send_file
from pydantic import ValidationError

# Add root and task directories to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Import task calculation modules
from Task_01_Option_Filtering.option_filtering import extract_date_handcrafted
from Task_02_PnL_Drawdown.pnl_drawdown_analysis import (
    load_trade_data, calculate_trade_pnl, calculate_drawdown_metrics
)
from Task_03_ML_PnL_Prediction.ml_pnl_prediction import (
    load_and_preprocess_dataset, train_and_evaluate_models, predict_single_trade
)
from Task_04_CSV_Dict_Converter.csv_to_dict_converter import (
    csv_to_flat_dict
)
from Task_05_Market_Insight_SMA.sma_insight import compute_market_insight, DEFAULT_STOCKS
from Task_07_Trade_Simulation.simulation_engine import simulate_trade_range
from Task_08_Recommendation_Dashboard.indicators import (
    calculate_sma, calculate_ema, calculate_rsi, calculate_stoch_rsi
)
from Task_08_Recommendation_Dashboard.recommendation import generate_recommendation
from Task_08_Recommendation_Dashboard.index_tracker import get_market_indices
from Task_09_API_Validation_Pydantic.schemas import (
    EntryExitSimulationRequest, MarketInsightRequest, MLPredictRequest
)

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Pre-train/Load ML model for Task 03 fast inference
TASK3_CSV = os.path.join(ROOT_DIR, 'Task_03_ML_PnL_Prediction', 'data', 'task_03.csv')
ml_model = None
if os.path.exists(TASK3_CSV):
    try:
        X_ml, y_ml, _ = load_and_preprocess_dataset(TASK3_CSV)
        from sklearn.ensemble import RandomForestRegressor
        ml_model = RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42)
        ml_model.fit(X_ml, y_ml)
    except Exception as e:
        print(f"[!] Warning: Could not pretrain ML model: {e}")


# ==========================================
# 0. MAIN HUB / PORTAL ROUTE
# ==========================================
@app.route('/')
def home():
    indices = get_market_indices(data_dir=os.path.join(ROOT_DIR, 'Task_08_Recommendation_Dashboard', 'data'))
    return render_template('index.html', indices=indices)


# ==========================================
# 1. TASK 01: OPTION FILTERING
# ==========================================
@app.route('/task01', methods=['GET'])
def task01_options():
    csv_path = os.path.join(ROOT_DIR, 'Task_01_Option_Filtering', 'data', 'filtered_contracts_with_date.csv')
    stocks_path = os.path.join(ROOT_DIR, 'Task_01_Option_Filtering', 'data', 'nifty50_stocks.csv')
    
    contracts_sample = []
    total_contracts = 0
    total_stocks = 0
    
    if os.path.exists(csv_path):
        df_c = pd.read_csv(csv_path, nrows=50)
        contracts_sample = df_c.to_dict(orient='records')
        total_contracts = 38349  # cached count
    
    if os.path.exists(stocks_path):
        df_s = pd.read_csv(stocks_path)
        total_stocks = len(df_s)

    return render_template(
        'task01_options.html',
        contracts=contracts_sample,
        total_contracts=total_contracts,
        total_stocks=total_stocks
    )


# ==========================================
# 2. TASK 02: TRADE PnL & DRAWDOWN
# ==========================================
@app.route('/task02', methods=['GET'])
def task02_pnl():
    json_path = os.path.join(ROOT_DIR, 'Task_02_PnL_Drawdown', 'data', 'task_02.json')
    top5_path = os.path.join(ROOT_DIR, 'Task_02_PnL_Drawdown', 'data', 'top_5_profits.csv')
    result_path = os.path.join(ROOT_DIR, 'Task_02_PnL_Drawdown', 'data', 'result.csv')

    summary_metrics = []
    top5_trades = []
    chart_data = {"labels": [], "pnl": [], "cum_pnl": []}

    if os.path.exists(result_path):
        df_res = pd.read_csv(result_path)
        summary_metrics = df_res.to_dict(orient='records')

    if os.path.exists(top5_path):
        df_top = pd.read_csv(top5_path)
        top5_trades = df_top.to_dict(orient='records')

    if os.path.exists(json_path):
        df_t = load_trade_data(json_path=json_path)
        df_t = calculate_trade_pnl(df_t)
        df_t = calculate_drawdown_metrics(df_t)
        sample_df = df_t.tail(60)
        chart_data = {
            "labels": [str(d)[:10] for d in sample_df['parsed_date']],
            "pnl": sample_df['pnl'].tolist(),
            "cum_pnl": sample_df['cumulative_pnl'].tolist(),
            "drawdown": sample_df['drawdown'].tolist()
        }

    return render_template(
        'task02_pnl.html',
        summary=summary_metrics,
        top5=top5_trades,
        chart_data=chart_data
    )


# ==========================================
# 3. TASK 03: ML PnL PREDICTOR
# ==========================================
@app.route('/task03', methods=['GET', 'POST'])
def task03_ml():
    prediction = None
    inputs = {'support_dist': 0.45, 'resistance_dist': 0.85, 'entry_time': '10:30'}
    
    if request.method == 'POST':
        try:
            inputs['support_dist'] = float(request.form.get('support_dist', 0.45))
            inputs['resistance_dist'] = float(request.form.get('resistance_dist', 0.85))
            inputs['entry_time'] = request.form.get('entry_time', '10:30').strip()

            # Pydantic validation
            MLPredictRequest(
                entry_support_distance_pct=inputs['support_dist'],
                entry_resistance_distance_pct=inputs['resistance_dist'],
                entry_time=inputs['entry_time']
            )

            if ml_model:
                prediction = predict_single_trade(
                    ml_model,
                    support_dist=inputs['support_dist'],
                    resistance_dist=inputs['resistance_dist'],
                    entry_time=inputs['entry_time']
                )
        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render_template('task03_ml.html', prediction=prediction, inputs=inputs)


# ==========================================
# 4. TASK 04: CSV TO DICTIONARY CONVERTER
# ==========================================
@app.route('/task04', methods=['GET'])
def task04_converter():
    emp_csv = os.path.join(ROOT_DIR, 'Task_04_CSV_Dict_Converter', 'data', 'employees.csv')
    converted = {}
    if os.path.exists(emp_csv):
        converted = csv_to_flat_dict(emp_csv, primary_key='id')
    return render_template('task04_converter.html', data_dict=converted)


# ==========================================
# 5. TASK 05: SMA MARKET INSIGHT
# ==========================================
@app.route('/task05', methods=['GET', 'POST'])
def task05_sma():
    sma_len = 14
    if request.method == 'POST':
        try:
            sma_len = int(request.form.get('sma_length', 14))
        except ValueError:
            sma_len = 14

    data_dir = os.path.join(ROOT_DIR, 'Task_05_Market_Insight_SMA', 'data')
    result = compute_market_insight(sma_length=sma_len, data_dir=data_dir)
    return render_template('task05_sma.html', result=result, sma_length=sma_len)


# ==========================================
# 6. TASK 06: SERVICE SELECTION
# ==========================================
@app.route('/services')
def task06_services():
    return render_template('task06_services.html')


# ==========================================
# 7. TASK 07: ENTRY/EXIT TRADE SIMULATOR
# ==========================================
@app.route('/task07', methods=['GET', 'POST'])
def task07_simulator():
    data_dir = os.path.join(ROOT_DIR, 'Task_07_Trade_Simulation', 'data')
    
    if request.method == 'GET':
        return render_template('task07_simulator.html')

    form = request.form
    try:
        req = EntryExitSimulationRequest(
            symbol=form.get('symbol', 'sbin'),
            entry_date=form.get('entry_date', '2025-06-03'),
            exit_date=form.get('exit_date', '2025-06-11'),
            entry_time=form.get('entry_time', '09:20'),
            exit_time=form.get('exit_time', '14:45'),
            position_type=form.get('position_type', 'long'),
            time_frame=form.get('time_frame', '1m')
        )
    except ValidationError as ve:
        error_msg = "; ".join([f"{e['loc'][0]}: {e['msg']}" for e in ve.errors()])
        return render_template('task07_simulator.html', error=error_msg)

    sim_data = simulate_trade_range(
        symbol=req.symbol,
        entry_date=req.entry_date,
        exit_date=req.exit_date,
        entry_time=req.entry_time,
        exit_time=req.exit_time,
        position_type=req.position_type,
        time_frame=req.time_frame,
        data_dir=data_dir
    )

    return render_template(
        'task07_simulator.html',
        results=sim_data['results'],
        log_messages=sim_data['log_messages'],
        pnl_chart=sim_data['pnl_chart'],
        total_pnl=sim_data['total_pnl'],
        total_trades=sim_data['total_trades'],
        selected_symbol=req.symbol,
        selected_pos=req.position_type
    )


# ==========================================
# 8. TASK 08: RECOMMENDATION DASHBOARD
# ==========================================
@app.route('/task08', methods=['GET', 'POST'])
def task08_dashboard():
    data_dir = os.path.join(ROOT_DIR, 'Task_08_Recommendation_Dashboard', 'data')
    stock_data_dir = os.path.join(ROOT_DIR, 'Task_07_Trade_Simulation', 'data')
    indices = get_market_indices(data_dir=data_dir)

    if request.method == 'GET':
        return render_template("task08_dashboard.html", indices=indices)

    symbol = request.form.get('symbol', 'sbin').lower().strip()
    date = request.form.get('date', '2025-06-03').strip()
    selected_indicators = request.form.getlist('indicators') or ['SMA', 'EMA', 'RSI']

    file_path = os.path.join(stock_data_dir, f"{symbol}_{date}.csv")
    if not os.path.exists(file_path):
        file_path = os.path.join(stock_data_dir, f"{symbol.upper()}_{date}.csv")

    if not os.path.exists(file_path):
        error_msg = f"Historical data not found for {symbol.upper()} on {date}."
        return render_template("task08_dashboard.html", error=error_msg, indices=indices)

    df = pd.read_csv(file_path)
    df['Symbol'] = symbol.upper()
    df['Date'] = date
    if 'Time' in df.columns:
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'].astype(str), errors='coerce')
    else:
        df['Datetime'] = pd.date_range(start=f"{date} 09:15", periods=len(df), freq='1min')

    if 'SMA' in selected_indicators: df = calculate_sma(df, 14)
    if 'EMA' in selected_indicators: df = calculate_ema(df, 14)
    if 'RSI' in selected_indicators: df = calculate_rsi(df, 14)
    if 'StochRSI' in selected_indicators: df = calculate_stoch_rsi(df, 14)

    rec = generate_recommendation(df, selected_indicators, 14)
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
        "task08_dashboard.html",
        recommendation=rec,
        indicators=selected_indicators,
        chart_data=chart_data,
        indices=indices,
        current_symbol=symbol.upper(),
        current_date=date
    )


# ==========================================
# 9. TASK 09: API VALIDATION SANDBOX
# ==========================================
@app.route('/task09', methods=['GET', 'POST'])
def task09_validator():
    test_result = None
    if request.method == 'POST':
        action = request.form.get('schema_type')
        try:
            if action == 'simulation':
                req = EntryExitSimulationRequest(
                    symbol=request.form.get('symbol', ''),
                    entry_date=request.form.get('entry_date', ''),
                    exit_date=request.form.get('exit_date', ''),
                    entry_time=request.form.get('entry_time', ''),
                    exit_time=request.form.get('exit_time', ''),
                    position_type=request.form.get('position_type', ''),
                    time_frame=request.form.get('time_frame', '')
                )
                test_result = {"status": "SUCCESS", "message": "Pydantic Validation Passed!", "validated_data": req.model_dump()}
            elif action == 'sma':
                req = MarketInsightRequest(sma_length=int(request.form.get('sma_length', 14)))
                test_result = {"status": "SUCCESS", "message": "Pydantic Validation Passed!", "validated_data": req.model_dump()}
            elif action == 'ml':
                req = MLPredictRequest(
                    entry_support_distance_pct=float(request.form.get('support_dist', 0)),
                    entry_resistance_distance_pct=float(request.form.get('resistance_dist', 0)),
                    entry_time=request.form.get('entry_time', '')
                )
                test_result = {"status": "SUCCESS", "message": "Pydantic Validation Passed!", "validated_data": req.model_dump()}
        except (ValidationError, ValueError) as e:
            test_result = {"status": "ERROR", "message": str(e)}

    return render_template('task09_validator.html', test_result=test_result)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[*] Starting Unified Arkalogi Portal on http://127.0.0.1:{port} ...")
    app.run(host='0.0.0.0', port=port, debug=True)
