"""
Task 07: Entry/Exit Trade Simulation Web Application
Arkalogi Internship - Priyanshu Kumar

Endpoints:
- GET  /           : Trade Simulation Form
- POST /entry_exit : Runs Backtest & Renders Interactive Results Chart + Audit Table
"""

import os
import sys
from flask import Flask, render_template, request
from simulation_engine import simulate_trade_range

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


@app.route('/', methods=['GET'])
@app.route('/entry_exit', methods=['GET', 'POST'])
def entry_exit():
    if request.method == 'GET':
        return render_template('entry_exit.html')

    symbol = request.form.get('symbol', 'sbin')
    entry_date = request.form.get('entry_date', '2025-06-03')
    exit_date = request.form.get('exit_date', '2025-06-11')
    entry_time = request.form.get('entry_time', '09:30')
    exit_time = request.form.get('exit_time', '15:15')
    position_type = request.form.get('position_type', 'long')
    time_frame = request.form.get('time_frame', '1m')

    sim_data = simulate_trade_range(
        symbol=symbol,
        entry_date=entry_date,
        exit_date=exit_date,
        entry_time=entry_time,
        exit_time=exit_time,
        position_type=position_type,
        time_frame=time_frame,
        data_dir=DATA_DIR
    )

    return render_template(
        'Resultout.html',
        results=sim_data['results'],
        log_messages=sim_data['log_messages'],
        pnl_chart=sim_data['pnl_chart'],
        total_pnl=sim_data['total_pnl'],
        total_trades=sim_data['total_trades']
    )


if __name__ == '__main__':
    print("[*] Starting Task 07 Trade Simulation Server on http://127.0.0.1:5007 ...")
    app.run(port=5007, debug=True)
