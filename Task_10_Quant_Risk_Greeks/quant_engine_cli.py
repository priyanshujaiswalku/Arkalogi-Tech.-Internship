"""
Task 10: Institutional Quant & Options Greeks Engine (CLI Runner)
Designed for Proprietary Trading Desks (Futures First / Axxela / AlphaGrep)
Author: Priyanshu Kumar

Executes:
1. Black-Scholes Greeks (Delta, Gamma, Theta, Vega, Rho) & Newton-Raphson IV solver
2. Institutional Risk Scorecard (Sharpe, Sortino, Calmar, VaR 95%/99%, CVaR, Kelly Criterion)
3. Multi-Leg Options Strategy Payoffs (Iron Condor, Straddle, Bull Spread)
4. NSE/BSE Transaction Friction Model
"""

import os
import sys

# Configure UTF-8 output encoding for Windows terminal
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from web_portal.quant_engine import (
    calculate_black_scholes_greeks,
    compute_institutional_risk_metrics,
    generate_option_strategy_payoff,
    calculate_exchange_friction
)

def run_task_10_demo():
    print("=" * 75)
    print(" [*] TASK 10: INSTITUTIONAL QUANT & DERIVATIVES RISK SUITE")
    print(" [*] Standards: Futures First & Axxela Evaluator Benchmark")
    print("=" * 75)

    # 1. Black Scholes Greeks
    spot = 24500.0
    strike = 24500.0
    dte = 7.0
    iv = 0.15
    print(f"\n[1] BLACK-SCHOLES GREEKS (NIFTY Spot={spot}, Strike={strike}, DTE={dte}d, IV={iv*100}%):")
    call_g = calculate_black_scholes_greeks(spot, strike, dte, iv, option_type='CE')
    put_g = calculate_black_scholes_greeks(spot, strike, dte, iv, option_type='PE')
    
    print(f"  (+) CALL (CE): Price=Rs {call_g['price']} | Delta={call_g['delta']} | Gamma={call_g['gamma']} | Theta=Rs {call_g['theta']}/d | Vega=Rs {call_g['vega']}/1%")
    print(f"  (-) PUT  (PE): Price=Rs {put_g['price']} | Delta={put_g['delta']} | Gamma={put_g['gamma']} | Theta=Rs {put_g['theta']}/d | Vega=Rs {put_g['vega']}/1%")

    # 2. Risk Metrics
    synthetic_pnl = [1500, -420, 890, 2100, -1200, 650, 1800, -350, 950, 2400, -750, 1300, 3200, -500, 900]
    print(f"\n[2] HEDGE-FUND RISK SCORECARD (15 Executed Trades):")
    risk = compute_institutional_risk_metrics(synthetic_pnl, initial_capital=100000.0)
    print(f"  - Sharpe Ratio: {risk['sharpe_ratio']} (Ann. Excess Return / Volatility)")
    print(f"  - Sortino Ratio: {risk['sortino_ratio']} (Downside Semi-Variance)")
    print(f"  - Calmar Ratio: {risk['calmar_ratio']} (Ann. Return / Max Drawdown)")
    print(f"  - Max Drawdown: -{risk['max_drawdown_pct']}% (Rs {risk['max_drawdown_val']})")
    print(f"  - 1-Day VaR (95%): {risk['var_95_pct']}% | CVaR (Expected Shortfall): {risk['cvar_95_pct']}%")
    print(f"  - Win Rate: {risk['win_rate_pct']}% | Profit Factor: {risk['profit_factor']}")
    print(f"  - Optimal Kelly Capital Allocation: {risk['kelly_criterion_pct']}%")

    # 3. Payoff Strategy
    condor = generate_option_strategy_payoff('iron_condor', spot_price=spot)
    print(f"\n[3] MULTI-LEG STRATEGY PAYOFF: {condor['strategy_name']}")
    print(f"  - Structure: {condor['description']}")
    print(f"  - Max Profit: {condor['max_reward']} | Max Risk: {condor['max_risk']}")
    print(f"  - Breakeven Points: Rs {condor['breakevens']}")

    # 4. Exchange Friction
    fric = calculate_exchange_friction(turnover_entry=245000, turnover_exit=246000, instrument_type='EQUITY_INTRADAY', slippage_bps=2.0)
    print(f"\n[4] INSTITUTIONAL FRICTION MODEL (Turnover = Rs 4.91 Lakh):")
    print(f"  - Statutory Taxes (STT+NSE+SEBI+GST+Stamp): Rs {fric['total_statutory_charges']}")
    print(f"  - Slippage Cost (2 bps drag): Rs {fric['slippage_cost']}")
    print(f"  - Total Execution Drag: Rs {fric['total_drag']}")

    print("\n" + "=" * 75)
    print(" [✓] Task 10 Quantitative Engine executed successfully!")
    print("=" * 75)

if __name__ == '__main__':
    run_task_10_demo()
