# 💼 Arkalogi Internship – Priyanshu Kumar

[![Live Demo on Vercel](https://img.shields.io/badge/Live%20Demo-Vercel%20Deployment-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://arkalogi-internship-portfolio.vercel.app)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/priyanshujaiswalku/Arkalogi-Tech.-Internship)

🌐 **Live Web Application**: [https://arkalogi-internship-portfolio.vercel.app](https://arkalogi-internship-portfolio.vercel.app)

Welcome! This repository documents my backend & AI/ML engineering internship journey at **Arkalogi**. Below is a comprehensive overview of the architecture, tasks assigned, technical approach, mathematical formulations, and instructions for running individual modules or the unified web portal.

---

## 🏗️ Repository Structure

```
Arkalogi-Internship/
├── Task_01_Option_Filtering/            # Task 01: NIFTY50 Options & Futures Handcrafted Filtering
│   ├── option_filtering.py
│   ├── README.md
│   └── data/
│
├── Task_02_PnL_Drawdown/                 # Task 02: Trade PnL, Peak Equity & Drawdown Analysis
│   ├── pnl_drawdown_analysis.py
│   ├── README.md
│   └── data/
│
├── Task_03_ML_PnL_Prediction/            # Task 03: Machine Learning PnL % Regression Models
│   ├── ml_pnl_prediction.py
│   ├── README.md
│   └── data/
│
├── Task_04_CSV_Dict_Converter/           # Task 04: Relational CSV to Nested Python Dict Converter
│   ├── csv_to_dict_converter.py
│   ├── README.md
│   └── data/
│
├── Task_05_Market_Insight_SMA/           # Task 05: Rolling SMA Market Scanner & REST API
│   ├── app.py
│   ├── sma_insight.py
│   ├── README.md
│   ├── templates/
│   └── data/
│
├── Task_06_Service_Selection_WebApp/     # Task 06: Multi-Page Dynamic Service Gateway (Flask)
│   ├── app.py
│   ├── README.md
│   └── templates/
│
├── Task_07_Trade_Simulation/             # Task 07: Intraday 1-Min Candlestick Backtester & Chart.js
│   ├── app.py
│   ├── simulation_engine.py
│   ├── README.md
│   ├── templates/
│   └── data/
│
├── Task_08_Recommendation_Dashboard/     # Task 08: Multi-Indicator Strategy Engine & Indices Tracker
│   ├── app.py
│   ├── indicators.py
│   ├── recommendation.py
│   ├── index_tracker.py
│   ├── README.md
│   ├── templates/
│   └── data/
│
├── Task_09_API_Validation_Pydantic/      # Task 09: Pydantic v2 Type Safety, Defense & Unit Tests
│   ├── schemas.py
│   ├── validator_middleware.py
│   ├── test_validation.py
│   └── README.md
│
├── web_portal/                           # 🌐 Integrated Full-Stack Web Portal
│   ├── app.py                            # Unified Flask application combining Tasks 01–09
│   ├── templates/                        # Modern responsive dark-mode UI
│   └── data/                             # Aggregated high-frequency & cache data
│
├── main.py                               # 🚀 Master Entry Point
├── run_all_tasks.py                      # 🧪 Automated Test & Verification Runner
├── requirements.txt                      # Project Dependencies
└── README.md                             # Repository Documentation
```

---

## 📌 Summary of Assigned Tasks

### 📌 Task 01: NIFTY50 Option Symbol Filtering (CSV)
- **Objective:** Ingest master instruments CSV (`nse_master_raw.csv`) from Zerodha/Kite and extract all option (`CE`, `PE`) and futures (`FUT`) contracts for NIFTY50 constituents.
- **Constraints:** No Regular Expressions (`re` module) allowed. Logic is handcrafted via string slicing and character traversal.
- **Output:** `filtered_contracts_with_date.csv`, `nifty50_stocks.csv`.
- **Run:** `python Task_01_Option_Filtering/option_filtering.py`

---

### 📌 Task 02: Trade PnL & Drawdown Analysis (JSON / Excel)
- **Objective:** Ingest trade execution histories (`task_02.json` / `task_02.xlsx`), compute PnL, cumulative equity curve, and drawdown trajectories.
- **Formulas:**
  - $\text{PnL (Long)} = (\text{Exit Price} - \text{Entry Price}) \times \text{Qty}$
  - $\text{PnL (Short)} = (\text{Entry Price} - \text{Exit Price}) \times \text{Qty}$
  - $\text{Peak Equity} = \text{cummax}(\text{Cumulative PnL})$
  - $\text{Drawdown} = \text{Cumulative PnL} - \text{Peak Equity}$
- **Metrics:** Win Rate (55.43%), Total Net PnL, Profit Factor, Max Drawdown, Top 5 Profitable Trades.
- **Output:** `result.csv`, `top_5_profits.csv`, `task_02_with_pnl.xlsx`.
- **Run:** `python Task_02_PnL_Drawdown/pnl_drawdown_analysis.py`

---

### 📌 Task 03: ML-Based PnL Percentage Prediction
- **Objective:** Supervised regression model predicting expected trade return percentage ($\text{PnL \%}$) from structural support/resistance distances and time-of-day features.
- **Features:** `entry_support_distance%`, `entry_resistance_distance%`, `entry_minutes` (elapsed minutes from market open 09:15 AM).
- **Models:** `RandomForestRegressor`, `GradientBoostingRegressor` (RMSE: 0.4744, R² Score: 0.03).
- **Output:** `pnl_prediction_plot.png`, `task_03.csv`.
- **Run:** `python Task_03_ML_PnL_Prediction/ml_pnl_prediction.py`

---

### 📌 Task 04: CSV to Python Dictionary Converter
- **Objective:** Transform flat tabular CSV files into structured nested Python dictionaries for $O(1)$ in-memory lookups.
- **Capabilities:** Primary key indexing and hierarchical key sequences (`Symbol -> Date -> Trades`).
- **Run:** `python Task_04_CSV_Dict_Converter/csv_to_dict_converter.py`

---

### 📌 Task 05: Market Insight (SMA Based API)
- **Objective:** Build a Flask API and scanner that computes rolling Simple Moving Averages (SMA) across NIFTY50 stocks and classifies them into Bullish (`above_sma`) and Bearish (`below_sma`) cohorts.
- **Run:** `python Task_05_Market_Insight_SMA/app.py` (Runs on `http://127.0.0.1:5005`)

---

### 📌 Task 06: Service Selection Web App (Flask)
- **Objective:** Multipage web application with dynamic service discovery and modular routing.
- **Run:** `python Task_06_Service_Selection_WebApp/app.py` (Runs on `http://127.0.0.1:5006`)

---

### 📌 Task 07: Entry/Exit Trade Simulation (Backend + Frontend)
- **Objective:** Intraday trade strategy backtester across 1-minute historical candlestick data with customizable date ranges, entry/exit times, and long/short directions.
- **Features:** Dynamic candle matching, realized PnL calculations, interactive Chart.js equity curve.
- **Run:** `python Task_07_Trade_Simulation/app.py` (Runs on `http://127.0.0.1:5007`)

---

### 📌 Task 08: Strategy Recommendation Dashboard
- **Objective:** Interactive quantitative analysis dashboard combining SMA (14), EMA (14), RSI (14), and Stochastic RSI with composite Buy/Sell/Hold scoring and live benchmark tracking (NIFTY 50, SENSEX, BSE MidCap).
- **Run:** `python Task_08_Recommendation_Dashboard/app.py` (Runs on `http://127.0.0.1:5008`)

---

### 📌 Task 09: API Validation & Security (Pydantic)
- **Objective:** Type-safe request/response validation schemas using Pydantic v2. Enforces ISO dates (`YYYY-MM-DD`), 24-hr timestamps (`HH:MM`), allowed timeframes, and numerical ranges.
- **Run Tests:** `python Task_09_API_Validation_Pydantic/test_validation.py`

---

## 🌐 Unified Web Portal (All Tasks Integrated)

To launch the complete, production-grade integrated portal containing interactive web pages for all 9 tasks:

```powershell
python main.py
```
Open your browser at: **`http://127.0.0.1:5000`**

---

## 🧪 Master Test & Verification Suite

To run and verify all task scripts in a single command:
```powershell
python run_all_tasks.py
```

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```powershell
   git clone https://github.com/priyanshuj/AI-ML.git
   cd AI-ML
   ```

2. **Install required dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Start the Application**:
   ```powershell
   python main.py
   ```

---

## 📚 Skills Applied
- **Backend Engineering:** Python, Flask (Routing, Blueprints, REST APIs, Jinja2 Templates)
- **Quantitative Trading & Analytics:** Time Series Resampling, Intraday Candlestick Modeling, Drawdown Analysis, Technical Indicators (SMA, EMA, RSI, StochRSI)
- **Machine Learning:** Feature Engineering, Regression Modeling, Random Forest, Scikit-Learn, Evaluation Metrics
- **API Security & Architecture:** Pydantic v2 Schema Modeling, Field Validators, Defense-in-Depth
- **Frontend Integration:** Modern Responsive CSS, HTML5, Chart.js Visualizations

---

**Author:** Priyanshu Kumar  
**GitHub:** [@priyanshuj](https://github.com/priyanshuj)  
**Company:** Arkalogi
