"""
Quantitative Finance, Derivatives & Risk Management Engine
Built for Proprietary Trading & Market Making Evaluation (Futures First / Axxela Focus)
Author: Priyanshu Kumar

Modules:
1. Black-Scholes Pricing & Options Greeks (Delta, Gamma, Theta, Vega, Rho, IV solver)
2. Institutional Quant Risk Metrics (Sharpe, Sortino, Calmar, VaR 95%/99%, CVaR, Max Drawdown, Kelly Criterion)
3. Multi-Leg Options Strategy Payoff Visualizer (Straddle, Strangle, Bull Call Spread, Iron Condor)
4. Indian Exchange Friction & Transaction Cost Model (STT, Exchange Charges, SEBI, GST, Stamp Duty, Slippage)
"""

import numpy as np
import pandas as pd
import math
from typing import Dict, Any, List, Tuple


# =====================================================================
# 1. BLACK-SCHOLES OPTIONS PRICING & GREEKS ENGINE
# =====================================================================

def standard_normal_cdf(x: float) -> float:
    """Cumulative Distribution Function of standard normal distribution."""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def standard_normal_pdf(x: float) -> float:
    """Probability Density Function of standard normal distribution."""
    return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * x * x)

def calculate_black_scholes_greeks(
    spot: float,
    strike: float,
    dte_days: float,
    volatility: float = 0.20,
    risk_free_rate: float = 0.065,
    option_type: str = 'CE'
) -> Dict[str, float]:
    """
    Computes theoretical Black-Scholes price and analytical Greeks.
    
    Parameters:
    - spot: Current Underlying Asset Price
    - strike: Option Strike Price
    - dte_days: Days to Expiration (DTE)
    - volatility: Annualized Implied Volatility (e.g. 0.20 for 20%)
    - risk_free_rate: Annualized Risk-Free Rate (e.g. 0.065 for 6.5% RBI repo-aligned)
    - option_type: 'CE' (Call) or 'PE' (Put)
    """
    if spot <= 0 or strike <= 0 or volatility <= 0:
        return {"price": 0.0, "delta": 0.0, "gamma": 0.0, "theta": 0.0, "vega": 0.0, "rho": 0.0, "moneyness": "ATM"}

    T = max(dte_days / 365.0, 1e-5)
    r = risk_free_rate
    sigma = max(volatility, 1e-4)
    S = spot
    K = strike

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    pdf_d1 = standard_normal_pdf(d1)
    cdf_d1 = standard_normal_cdf(d1)
    cdf_d2 = standard_normal_cdf(d2)
    cdf_neg_d1 = standard_normal_cdf(-d1)
    cdf_neg_d2 = standard_normal_cdf(-d2)

    is_call = option_type.upper() in ['CE', 'CALL']

    if is_call:
        price = S * cdf_d1 - K * math.exp(-r * T) * cdf_d2
        delta = cdf_d1
        theta = (- (S * pdf_d1 * sigma) / (2.0 * math.sqrt(T)) - r * K * math.exp(-r * T) * cdf_d2) / 365.0
        rho = (K * T * math.exp(-r * T) * cdf_d2) / 100.0
    else:
        price = K * math.exp(-r * T) * cdf_neg_d2 - S * cdf_neg_d1
        delta = cdf_d1 - 1.0
        theta = (- (S * pdf_d1 * sigma) / (2.0 * math.sqrt(T)) + r * K * math.exp(-r * T) * cdf_neg_d2) / 365.0
        rho = (-K * T * math.exp(-r * T) * cdf_neg_d2) / 100.0

    gamma = pdf_d1 / (S * sigma * math.sqrt(T))
    vega = (S * math.sqrt(T) * pdf_d1) / 100.0  # Per 1% vol change

    # Moneyness classification
    moneyness_ratio = S / K
    if is_call:
        if moneyness_ratio > 1.02: moneyness = "ITM (In-The-Money)"
        elif moneyness_ratio < 0.98: moneyness = "OTM (Out-of-The-Money)"
        else: moneyness = "ATM (At-The-Money)"
    else:
        if moneyness_ratio < 0.98: moneyness = "ITM (In-The-Money)"
        elif moneyness_ratio > 1.02: moneyness = "OTM (Out-of-The-Money)"
        else: moneyness = "ATM (At-The-Money)"

    return {
        "price": round(max(0.0, price), 2),
        "delta": round(delta, 4),
        "gamma": round(gamma, 6),
        "theta": round(theta, 2),  # 1-day decay in Rs
        "vega": round(vega, 2),    # 1% IV change in Rs
        "rho": round(rho, 4),
        "moneyness": moneyness,
        "intrinsic_value": round(max(0.0, S - K) if is_call else max(0.0, K - S), 2),
        "time_value": round(max(0.0, price - (max(0.0, S - K) if is_call else max(0.0, K - S))), 2)
    }


def implied_volatility_newton_raphson(
    market_price: float,
    spot: float,
    strike: float,
    dte_days: float,
    risk_free_rate: float = 0.065,
    option_type: str = 'CE',
    max_iterations: int = 100,
    tolerance: float = 1e-4
) -> float:
    """
    Solves for Black-Scholes Implied Volatility (IV) using Newton-Raphson numerical root finding.
    """
    sigma = 0.25  # Initial guess (25% IV)
    T = max(dte_days / 365.0, 1e-5)
    
    for _ in range(max_iterations):
        greeks = calculate_black_scholes_greeks(spot, strike, dte_days, sigma, risk_free_rate, option_type)
        diff = greeks['price'] - market_price
        if abs(diff) < tolerance:
            return round(sigma * 100.0, 2)
        vega = greeks['vega'] * 100.0  # Raw vega
        if abs(vega) < 1e-6:
            break
        sigma = sigma - diff / vega
        if sigma <= 0.001:
            sigma = 0.001

    return round(sigma * 100.0, 2)


# =====================================================================
# 2. QUANT RISK METRICS & PERFORMANCE ATTRIBUTION
# =====================================================================

def compute_institutional_risk_metrics(
    pnl_series: List[float],
    initial_capital: float = 100000.0,
    risk_free_rate: float = 0.065,
    trading_days_per_year: int = 252
) -> Dict[str, Any]:
    """
    Computes hedge-fund / prop-desk grade performance and risk metrics:
    - Annualized Return, Sharpe Ratio, Sortino Ratio, Calmar Ratio
    - Maximum Drawdown (MDD) in % and Currency
    - Historical & Parametric Value at Risk (VaR 95%, 99%)
    - Conditional Value at Risk (CVaR / Expected Shortfall)
    - Win Rate %, Profit Factor, Trade Expectancy, Kelly Criterion %
    """
    if not pnl_series or len(pnl_series) < 2:
        return {
            "total_trades": len(pnl_series),
            "total_pnl": sum(pnl_series) if pnl_series else 0.0,
            "win_rate_pct": 0.0,
            "sharpe_ratio": 0.0,
            "sortino_ratio": 0.0,
            "calmar_ratio": 0.0,
            "max_drawdown_pct": 0.0,
            "max_drawdown_val": 0.0,
            "var_95_pct": 0.0,
            "cvar_95_pct": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "kelly_criterion_pct": 0.0
        }

    pnls = np.array(pnl_series, dtype=float)
    total_trades = len(pnls)
    total_pnl = float(np.sum(pnls))
    
    # Returns relative to running capital
    running_capital = initial_capital + np.cumsum(pnls)
    trade_returns = pnls / initial_capital

    wins = pnls[pnls > 0]
    losses = pnls[pnls < 0]
    
    win_count = len(wins)
    loss_count = len(losses)
    win_rate = (win_count / total_trades) * 100.0 if total_trades > 0 else 0.0
    
    gross_profit = float(np.sum(wins)) if len(wins) > 0 else 0.0
    gross_loss = float(abs(np.sum(losses))) if len(losses) > 0 else 0.0
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (99.0 if gross_profit > 0 else 0.0)

    avg_win = float(np.mean(wins)) if len(wins) > 0 else 0.0
    avg_loss = float(abs(np.mean(losses))) if len(losses) > 0 else 0.0
    win_loss_ratio = (avg_win / avg_loss) if avg_loss > 0 else 1.0

    # Expectancy ($ per trade) = (Win% * AvgWin) - (Loss% * AvgLoss)
    p_win = win_rate / 100.0
    p_loss = 1.0 - p_win
    expectancy = (p_win * avg_win) - (p_loss * avg_loss)

    # Kelly Criterion = p - (q / b) where b is avg_win / avg_loss
    kelly_pct = 0.0
    if win_loss_ratio > 0:
        kelly_fraction = p_win - (p_loss / win_loss_ratio)
        kelly_pct = max(0.0, round(kelly_fraction * 100.0, 2))  # Fractional/Half Kelly commonly used in props

    # Cumulative equity & Peak Drawdown
    equity_curve = initial_capital + np.concatenate(([0], np.cumsum(pnls)))
    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (running_max - equity_curve)
    drawdowns_pct = (drawdowns / running_max) * 100.0
    
    max_drawdown_val = float(np.max(drawdowns))
    max_drawdown_pct = float(np.max(drawdowns_pct))

    # Annualized Return & Risk
    mean_ret = float(np.mean(trade_returns))
    std_ret = float(np.std(trade_returns)) if len(trade_returns) > 1 else 1e-4
    
    # Scale to annual
    scale = math.sqrt(trading_days_per_year)
    ann_return = mean_ret * trading_days_per_year
    ann_std = std_ret * scale
    daily_rf = risk_free_rate / trading_days_per_year
    
    # Sharpe Ratio
    excess_ret = trade_returns - daily_rf
    sharpe = (float(np.mean(excess_ret)) / std_ret * scale) if std_ret > 1e-6 else 0.0

    # Sortino Ratio (Downside deviation only)
    downside_returns = excess_ret[excess_ret < 0]
    downside_std = float(np.std(downside_returns)) if len(downside_returns) > 1 else 1e-4
    sortino = (float(np.mean(excess_ret)) / downside_std * scale) if downside_std > 1e-6 else 0.0

    # Calmar Ratio = Annualized Return % / Max Drawdown %
    calmar = (ann_return * 100.0 / max_drawdown_pct) if max_drawdown_pct > 0.01 else 0.0

    # Value-at-Risk (VaR 95% & 99% 1-period)
    var_95 = float(abs(np.percentile(trade_returns, 5))) * 100.0
    var_99 = float(abs(np.percentile(trade_returns, 1))) * 100.0

    # Conditional VaR (Expected Shortfall CVaR 95%)
    tail_losses = trade_returns[trade_returns <= np.percentile(trade_returns, 5)]
    cvar_95 = float(abs(np.mean(tail_losses))) * 100.0 if len(tail_losses) > 0 else var_95

    return {
        "total_trades": total_trades,
        "win_count": win_count,
        "loss_count": loss_count,
        "win_rate_pct": round(win_rate, 2),
        "total_pnl": round(total_pnl, 2),
        "gross_profit": round(gross_profit, 2),
        "gross_loss": round(gross_loss, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "profit_factor": round(profit_factor, 2),
        "expectancy": round(expectancy, 2),
        "kelly_criterion_pct": kelly_pct,
        "sharpe_ratio": round(sharpe, 2),
        "sortino_ratio": round(sortino, 2),
        "calmar_ratio": round(calmar, 2),
        "max_drawdown_pct": round(max_drawdown_pct, 2),
        "max_drawdown_val": round(max_drawdown_val, 2),
        "var_95_pct": round(var_95, 2),
        "var_99_pct": round(var_99, 2),
        "cvar_95_pct": round(cvar_95, 2)
    }


# =====================================================================
# 3. MULTI-LEG OPTION STRATEGY PAYOFF ENGINE
# =====================================================================

def generate_option_strategy_payoff(
    strategy_name: str,
    spot_price: float = 24500.0,
    strike_offset_pct: float = 1.0,
    iv: float = 0.15,
    dte: float = 7.0
) -> Dict[str, Any]:
    """
    Generates multi-strike payoff diagrams for institutional options strategies:
    - Long Straddle (Vol breakout)
    - Short Straddle (Delta-neutral gamma scalping)
    - Bull Call Spread (Defined-risk directional)
    - Bear Put Spread (Defined-risk bearish)
    - Iron Condor (Non-directional range market making)
    """
    S = spot_price
    atm_strike = round(S / 50.0) * 50.0
    otm_call_strike = round((S * (1.0 + strike_offset_pct / 100.0)) / 50.0) * 50.0
    otm_put_strike = round((S * (1.0 - strike_offset_pct / 100.0)) / 50.0) * 50.0
    far_otm_call = round((S * (1.0 + (strike_offset_pct * 2) / 100.0)) / 50.0) * 50.0
    far_otm_put = round((S * (1.0 - (strike_offset_pct * 2) / 100.0)) / 50.0) * 50.0

    # Pricing individual legs
    call_atm_p = calculate_black_scholes_greeks(S, atm_strike, dte, iv, option_type='CE')['price']
    put_atm_p = calculate_black_scholes_greeks(S, atm_strike, dte, iv, option_type='PE')['price']
    call_otm_p = calculate_black_scholes_greeks(S, otm_call_strike, dte, iv, option_type='CE')['price']
    put_otm_p = calculate_black_scholes_greeks(S, otm_put_strike, dte, iv, option_type='PE')['price']
    call_far_p = calculate_black_scholes_greeks(S, far_otm_call, dte, iv, option_type='CE')['price']
    put_far_p = calculate_black_scholes_greeks(S, far_otm_put, dte, iv, option_type='PE')['price']

    # Generate price domain across +/- 6%
    underlying_range = np.linspace(S * 0.94, S * 1.06, 60)
    payoffs = []

    strategy = strategy_name.lower().replace(' ', '_')

    if strategy in ['long_straddle', 'straddle']:
        # Buy ATM Call + Buy ATM Put
        net_premium = call_atm_p + put_atm_p
        desc = f"Long {atm_strike} Call (@₹{call_atm_p}) + Long {atm_strike} Put (@₹{put_atm_p})"
        max_risk = round(net_premium, 2)
        max_reward = "Unlimited (Volatility Breakout)"
        breakevens = [round(atm_strike - net_premium, 1), round(atm_strike + net_premium, 1)]
        
        for p in underlying_range:
            call_payoff = max(0, p - atm_strike) - call_atm_p
            put_payoff = max(0, atm_strike - p) - put_atm_p
            payoffs.append(round(call_payoff + put_payoff, 2))

    elif strategy in ['short_straddle']:
        # Sell ATM Call + Sell ATM Put
        net_premium = call_atm_p + put_atm_p
        desc = f"Short {atm_strike} Call (@₹{call_atm_p}) + Short {atm_strike} Put (@₹{put_atm_p})"
        max_risk = "Unlimited (Requires Dynamic Delta Hedging)"
        max_reward = f"₹{round(net_premium, 2)} (Max Premium Collected)"
        breakevens = [round(atm_strike - net_premium, 1), round(atm_strike + net_premium, 1)]
        
        for p in underlying_range:
            call_payoff = call_atm_p - max(0, p - atm_strike)
            put_payoff = put_atm_p - max(0, atm_strike - p)
            payoffs.append(round(call_payoff + put_payoff, 2))

    elif strategy in ['bull_call_spread', 'bull_spread']:
        # Buy ATM Call + Sell OTM Call
        net_debit = call_atm_p - call_otm_p
        spread_width = otm_call_strike - atm_strike
        desc = f"Long {atm_strike} Call (@₹{call_atm_p}) + Short {otm_call_strike} Call (@₹{call_otm_p})"
        max_risk = f"₹{round(net_debit, 2)}"
        max_reward = f"₹{round(spread_width - net_debit, 2)}"
        breakevens = [round(atm_strike + net_debit, 1)]
        
        for p in underlying_range:
            c1 = max(0, p - atm_strike) - call_atm_p
            c2 = call_otm_p - max(0, p - otm_call_strike)
            payoffs.append(round(c1 + c2, 2))

    elif strategy in ['bear_put_spread', 'bear_spread']:
        # Buy ATM Put + Sell OTM Put
        net_debit = put_atm_p - put_otm_p
        spread_width = atm_strike - otm_put_strike
        desc = f"Long {atm_strike} Put (@₹{put_atm_p}) + Short {otm_put_strike} Put (@₹{put_otm_p})"
        max_risk = f"₹{round(net_debit, 2)}"
        max_reward = f"₹{round(spread_width - net_debit, 2)}"
        breakevens = [round(atm_strike - net_debit, 1)]
        
        for p in underlying_range:
            p1 = max(0, atm_strike - p) - put_atm_p
            p2 = put_otm_p - max(0, otm_put_strike - p)
            payoffs.append(round(p1 + p2, 2))

    else:
        # Default: Iron Condor (Sell OTM Put + Buy Far OTM Put + Sell OTM Call + Buy Far OTM Call)
        strategy = 'iron_condor'
        net_credit = (put_otm_p - put_far_p) + (call_otm_p - call_far_p)
        spread_width = otm_call_strike - otm_put_strike
        wing_width = far_otm_call - otm_call_strike
        desc = f"Short {otm_put_strike}P/Long {far_otm_put}P + Short {otm_call_strike}C/Long {far_otm_call}C"
        max_reward = f"₹{round(net_credit, 2)} (Net Credit)"
        max_risk = f"₹{round(wing_width - net_credit, 2)}"
        breakevens = [round(otm_put_strike - net_credit, 1), round(otm_call_strike + net_credit, 1)]

        for p in underlying_range:
            put_spread = (put_otm_p - max(0, otm_put_strike - p)) + (max(0, far_otm_put - p) - put_far_p)
            call_spread = (call_otm_p - max(0, p - otm_call_strike)) + (max(0, p - far_otm_call) - call_far_p)
            payoffs.append(round(put_spread + call_spread, 2))

    return {
        "strategy_name": strategy.replace('_', ' ').title(),
        "description": desc,
        "spot_price": S,
        "max_risk": max_risk,
        "max_reward": max_reward,
        "breakevens": breakevens,
        "underlying_prices": [round(x, 1) for x in underlying_range.tolist()],
        "payoffs": payoffs
    }


# =====================================================================
# 4. INSTITUTIONAL TRANSACTION FRICTION & SLIPPAGE MODEL (NSE / BSE)
# =====================================================================

def calculate_exchange_friction(
    turnover_entry: float,
    turnover_exit: float,
    instrument_type: str = 'EQUITY_INTRADAY',
    slippage_bps: float = 2.0
) -> Dict[str, float]:
    """
    Computes precise transaction taxes & exchange frictions (India NSE/BSE rules):
    - STT (Securities Transaction Tax)
    - Exchange Turnover Fee (NSE 0.00345%)
    - SEBI Turnover Charges (₹10 / crore)
    - Stamp Duty (0.003% on buy intraday)
    - GST (18% on Brokerage + Exchange Fees + SEBI charges)
    - Realistic Quant Desk Slippage in Basis Points (bps)
    """
    total_turnover = turnover_entry + turnover_exit

    if instrument_type.upper() == 'EQUITY_INTRADAY':
        # STT: 0.025% on sell side only
        stt = turnover_exit * 0.00025
        exchange_charges = total_turnover * 0.0000345
        sebi_charges = total_turnover * 0.000001
        stamp_duty = turnover_entry * 0.00003
        brokerage = min(40.0, total_turnover * 0.0003)
        gst = (brokerage + exchange_charges + sebi_charges) * 0.18
        slippage_cost = total_turnover * (slippage_bps / 10000.0)

    elif instrument_type.upper() == 'FUTURES':
        # STT: 0.0125% on sell
        stt = turnover_exit * 0.000125
        exchange_charges = total_turnover * 0.00002
        sebi_charges = total_turnover * 0.000001
        stamp_duty = turnover_entry * 0.00002
        brokerage = min(40.0, total_turnover * 0.0002)
        gst = (brokerage + exchange_charges + sebi_charges) * 0.18
        slippage_cost = total_turnover * (slippage_bps / 10000.0)

    else:  # OPTIONS
        # STT: 0.0625% on sell premium
        stt = turnover_exit * 0.000625
        exchange_charges = total_turnover * 0.0005
        sebi_charges = total_turnover * 0.000001
        stamp_duty = turnover_entry * 0.00003
        brokerage = 40.0
        gst = (brokerage + exchange_charges + sebi_charges) * 0.18
        slippage_cost = total_turnover * (slippage_bps / 10000.0)

    total_taxes = stt + exchange_charges + sebi_charges + stamp_duty + gst + brokerage
    total_drag = total_taxes + slippage_cost

    return {
        "stt": round(stt, 2),
        "exchange_charges": round(exchange_charges, 2),
        "sebi_charges": round(sebi_charges, 4),
        "stamp_duty": round(stamp_duty, 2),
        "brokerage": round(brokerage, 2),
        "gst": round(gst, 2),
        "slippage_cost": round(slippage_cost, 2),
        "total_statutory_charges": round(total_taxes, 2),
        "total_drag": round(total_drag, 2)
    }
