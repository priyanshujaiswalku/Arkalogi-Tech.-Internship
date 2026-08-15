"""
Task 05: Market Insight (SMA Based API) - Flask Web Application
Arkalogi Internship - Priyanshu Kumar

Endpoints:
- GET  /                     : Form page to enter SMA length
- POST /market_insight       : HTML result page
- GET/POST /api/market_insight : JSON API response
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
from sma_insight import compute_market_insight, DEFAULT_STOCKS

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', default_stocks=[s.replace('.NS', '') for s in DEFAULT_STOCKS])


@app.route('/market_insight', methods=['POST'])
def market_insight():
    try:
        sma_length = int(request.form.get('sma_length', 14))
    except ValueError:
        sma_length = 14

    result = compute_market_insight(sma_length=sma_length, data_dir=DATA_DIR)
    return render_template('result.html', result=result, sma_length=sma_length)


@app.route('/api/market_insight', methods=['GET', 'POST'])
def api_market_insight():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        sma_length = int(data.get('sma_length', 14))
    else:
        sma_length = int(request.args.get('sma_length', 14))

    result = compute_market_insight(sma_length=sma_length, data_dir=DATA_DIR)
    return jsonify(result)


if __name__ == '__main__':
    print("[*] Starting Task 05 Flask Server on http://127.0.0.1:5005 ...")
    app.run(port=5005, debug=True)
