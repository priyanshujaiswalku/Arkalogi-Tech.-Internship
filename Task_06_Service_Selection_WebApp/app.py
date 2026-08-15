"""
Task 06: Service Selection Web App (Flask Architecture)
Arkalogi Internship - Priyanshu Kumar

Multi-page Flask web application with dynamic service discovery and modular routing.
"""

import os
import sys
from flask import Flask, render_template, request, redirect, url_for

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

SERVICES = [
    {
        'id': 'market_insight',
        'title': 'Market Insight Engine',
        'desc': 'SMA-based market scanner identifying bullish and bearish momentum across NIFTY50 equities.',
        'icon': '📊',
        'endpoint': '/service/market_insight'
    },
    {
        'id': 'trade_simulator',
        'title': 'Entry/Exit Trade Simulator',
        'desc': 'Simulate long/short intraday trading strategies across historical minute candle data.',
        'icon': '⚡',
        'endpoint': '/service/trade_simulator'
    },
    {
        'id': 'recommendation_dashboard',
        'title': 'Multi-Indicator Strategy Dashboard',
        'desc': 'Technical indicators (SMA, EMA, RSI, StochRSI) with automated Buy/Sell/Hold confidence scoring.',
        'icon': '🎯',
        'endpoint': '/service/recommendation_dashboard'
    },
    {
        'id': 'ml_predictor',
        'title': 'ML PnL % Predictor',
        'desc': 'Machine learning model predicting expected trade profitability using support/resistance distances.',
        'icon': '🤖',
        'endpoint': '/service/ml_predictor'
    }
]


@app.route('/')
def home():
    return render_template('home.html', services=SERVICES)


@app.route('/select_service')
def service_select():
    return render_template('service_select.html', services=SERVICES)


@app.route('/service/<service_id>')
def view_service(service_id):
    service = next((s for s in SERVICES if s['id'] == service_id), None)
    if not service:
        return redirect(url_for('home'))
    return render_template('service_select.html', services=SERVICES, active_service=service)


if __name__ == '__main__':
    print("[*] Starting Task 06 Service Selection App on http://127.0.0.1:5006 ...")
    app.run(port=5006, debug=True)
