# 🏛️ Arkalogi Quantitative Analytics & Algorithmic Trading Platform
### Author: Priyanshu Kumar | Backend & Quantitative Trading Engineering Portfolio

[![Live Demo on Vercel](https://img.shields.io/badge/Live%20Demo-Vercel%20Production-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://arkalogi-internship-portfolio.vercel.app)
[![Target Evaluators](https://img.shields.io/badge/Desk%20Standards-Futures%20First%20%7C%20Axxela%20%7C%20AlphaGrep-f59e0b?style=for-the-badge&logo=target)](https://arkalogi-internship-portfolio.vercel.app)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/priyanshujaiswalku/Arkalogi-Tech.-Internship)
[![Build Status](https://img.shields.io/badge/Automated%20Tests-6%2F6%20Passed-10b981?style=for-the-badge)](https://github.com/priyanshujaiswalku/Arkalogi-Tech.-Internship)

🌐 **Live Web Application**: [https://arkalogi-internship-portfolio.vercel.app](https://arkalogi-internship-portfolio.vercel.app)

---

## 🎯 Executive Summary & Prop Trading Desk Alignment

This repository documents the production-grade quantitative finance, derivatives engineering, and high-performance backend systems built by **Priyanshu Kumar** during the **Arkalogi Engineering Internship**.

The architecture was intentionally engineered to meet the evaluation benchmarks of top quantitative proprietary trading firms (**Futures First**, **Axxela**, **AlphaGrep**, **Tower Research**):

| Quantitative Discipline | Prop Firm Focus (Futures First / Axxela) | Architecture Implementation in this Repo |
| :--- | :--- | :--- |
| **Derivatives & Pricing** | Options Greeks, Delta Neutrality, Dynamic Hedging, Volatility Surface | **Task 01 & Task 10**: Black-Scholes analytical $\Delta, \Gamma, \Theta, \mathcal{V}, \rho$, Newton-Raphson IV root-finding, and Multi-leg payoff modeling (Iron Condor, Straddle, Spreads). |
| **Risk Management** | Capital Preservation, Max Drawdown limits, Tail Risk | **Task 02 & Task 10**: Annualized Sharpe Ratio, Sortino Ratio, Calmar Ratio, 95%/99% VaR, Conditional VaR (Expected Shortfall), and Kelly Criterion sizing. |
| **Quantitative Alpha** | Statistical Arbitrage, Predictive Modeling, Feature Engineering | **Task 03 & Task 08**: Random Forest Alpha Regressors, Intraday Liquidity Seasonality, Multi-Indicator Consensus Strategies (SMA, EMA, RSI, StochRSI). |
| **Execution Microstructure** | Transaction Cost Analysis (TCA), Slippage, Exchange Friction | **Task 07**: Intraday 1-min candlestick backtester with realistic Indian exchange statutory charges (STT, NSE turnover, SEBI fee, GST) and basis point slippage. |
| **Defensive Architecture** | Low Latency, Schema Type Safety, Fail-Fast Order Routing | **Task 09 & Web Portal**: Pydantic v2 data validation, zero-regex string parsers ($O(N)$), and Serverless Python API. |

---

## 🏗️ Repository Architecture

```
Arkalogi-Tech.-Internship/
├── Task_01_Option_Filtering/            # Task 01: NIFTY 50 Option Chain & Handcrafted Date Parser ($O(N)$)
│   ├── option_filtering.py
│   ├── README.md
│   └── data/
│
├── Task_02_PnL_Drawdown/                 # Task 02: Trade PnL, Peak Equity & Hedge-Fund Risk Metrics
│   ├── pnl_drawdown_analysis.py
│   ├── README.md
│   └── data/
│
├── Task_03_ML_PnL_Prediction/            # Task 03: ML PnL % Alpha Regressor & Kelly Position Sizing
│   ├── ml_pnl_prediction.py
│   ├── README.md
│   └── data/
│
├── Task_04_CSV_Dict_Converter/           # Task 04: Relational CSV to Hierarchical Dict Converter ($O(N)$)
│   ├── csv_to_dict_converter.py
│   ├── README.md
│   └── data/
│
├── Task_05_Market_Insight_SMA/           # Task 05: Rolling SMA Market Scanner & REST Endpoint
│   ├── app.py
│   ├── sma_insight.py
│   ├── README.md
│   ├── templates/
│   └── data/
│
├── Task_06_Service_Selection_WebApp/     # Task 06: Dynamic Gateway & Service Selector
│   ├── app.py
│   ├── README.md
│   └── templates/
│
├── Task_07_Trade_Simulation/             # Task 07: 1-Min Candlestick Backtester & Indian Exchange Friction
│   ├── app.py
│   ├── simulation_engine.py
│   ├── README.md
│   ├── templates/
│   └── data/
│
├── Task_08_Recommendation_Dashboard/     # Task 08: Multi-Indicator Algorithmic Strategy Engine (SMA/EMA/RSI)
│   ├── app.py
│   ├── indicators.py
│   ├── recommendation.py
│   ├── index_tracker.py
│   ├── README.md
│   ├── templates/
│   └── data/
│
├── Task_09_API_Validation_Pydantic/      # Task 09: Pydantic v2 Type Defense & Defensive Testing
│   ├── schemas.py
│   ├── test_validation.py
│   ├── validator_middleware.py
│   └── README.md
│
├── Task_10_Quant_Risk_Greeks/            # Task 10: Institutional Quant & Options Greeks Engine
│   ├── quant_engine_cli.py
│   └── README.md
│
├── web_portal/                           # Unified Production Web Terminal (Flask + Chart.js)
│   ├── app.py
│   ├── quant_engine.py                  # Core Quantitative & Derivatives Mathematical Library
│   ├── templates/                       # High-Density Dark FinTech UI
│   └── data/
│
├── api/
│   └── index.py                          # Vercel Serverless Function Handler
├── vercel.json                           # Vercel Production Build & Routing Configuration
├── requirements.txt                      # Pinned Dependencies
├── run_all_tasks.py                      # Master Automated Test & Verification Suite
└── main.py                               # Local Web Server Entry Point
```

---

## 📐 Mathematical Formulations

### 1. Black-Scholes Options Greeks Pricing
Given Underlying Spot $S$, Strike $K$, Time to Expiration $T = \frac{\text{DTE}}{365}$, Volatility $\sigma$, Risk-Free Rate $r$:

$$d_1 = \frac{\ln(S/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

- **Call Delta ($\Delta_{CE}$)**: $N(d_1)$
- **Put Delta ($\Delta_{PE}$)**: $N(d_1) - 1$
- **Gamma ($\Gamma$)**: $\frac{N'(d_1)}{S \sigma \sqrt{T}}$
- **Vega ($\mathcal{V}$)**: $\frac{S \sqrt{T} N'(d_1)}{100}$ (Sensitivity to $1\%$ IV shift)
- **Theta ($\Theta$)**: $\left( -\frac{S N'(d_1) \sigma}{2\sqrt{T}} - r K e^{-rT} N(d_2) \right) / 365$

---

### 2. Portfolio Risk & Attribution Engine
- **Annualized Sharpe Ratio**:
  $$\text{Sharpe} = \frac{\mathbb{E}[R_p - R_f]}{\sigma(R_p)} \times \sqrt{252}$$
- **Sortino Ratio**:
  $$\text{Sortino} = \frac{\mathbb{E}[R_p - R_f]}{\sqrt{\frac{1}{N}\sum \min(0, R_p - R_f)^2}} \times \sqrt{252}$$
- **Calmar Ratio**:
  $$\text{Calmar} = \frac{\text{Annualized Return \%}}{\text{Max Drawdown \%}}$$
- **Value at Risk (VaR 95%)**:
  $$\text{VaR}_{0.95} = - \text{Percentile}(R_p, 5\%)$$
- **Expected Shortfall (Conditional VaR)**:
  $$\text{CVaR}_{0.95} = -\mathbb{E}[R_p \mid R_p \le -\text{VaR}_{0.95}]$$
- **Kelly Criterion**:
  $$f^* = p - \frac{1 - p}{b} \quad \text{where } b = \frac{\text{Avg Win}}{\text{Avg Loss}}$$

---

### 3. Realistic Indian Exchange Transaction Cost Model (NSE/BSE)
For Intraday Equity Turnover:
- **STT (Securities Transaction Tax)**: $0.025\%$ on exit turnover
- **Exchange Charges**: $0.00345\%$ of total turnover
- **SEBI Turnover Fee**: $₹10 \text{ per crore}$ ($0.0001\%$)
- **Stamp Duty**: $0.003\%$ on entry turnover
- **Brokerage**: $\min(₹40, 0.03\% \text{ of turnover})$
- **GST**: $18\%$ on (Brokerage + Exchange Charges + SEBI Fees)
- **Execution Slippage**: $2 \text{ bps}$ ($0.02\%$) drag

---

## ⚡ Quick Start & Verification

### 1. Run Automated Test Verification Suite
```bash
python run_all_tasks.py
```
*Executes all 6 validation scripts sequentially with automated exit-code assertions.*

### 2. Launch Local Web Terminal
```bash
python main.py
```
*Access the unified trading portal at [http://127.0.0.1:5000](http://127.0.0.1:5000).*

### 3. Run Standalone Quant Engine (CLI)
```bash
python Task_10_Quant_Risk_Greeks/quant_engine_cli.py
```

---

## 👨‍💻 Developer & Engineer Profile
- **Candidate**: Priyanshu Kumar
- **Role**: Backend & Quantitative Trading Engineering Intern
- **GitHub**: [priyanshujaiswalku](https://github.com/priyanshujaiswalku)
- **Live Deployment**: [https://arkalogi-internship-portfolio.vercel.app](https://arkalogi-internship-portfolio.vercel.app)
