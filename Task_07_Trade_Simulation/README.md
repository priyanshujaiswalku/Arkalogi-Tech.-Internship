# 📌 Task 07: Entry/Exit Trade Simulation (Backend + Frontend)

**Internship Role**: Backend / AI-ML Engineering Intern  
**Intern**: Priyanshu Kumar  
**Company**: Arkalogi

---

## 🎯 Objective
Simulate multi-day intraday trading strategies across historical high-frequency 1-minute candlestick data. Accepts parameter configurations for stock symbol, custom date ranges, execution entry/exit timestamps, and Long/Short trade directions.

---

## ⚙️ Key Capabilities
1. **Intraday Strategy Backtester**:
   - Matches candle close prices at user-specified `entry_time` and `exit_time`.
   - Computes single-trade and cumulative $\text{PnL}$ across single-stock or basket date ranges.
2. **Visual PnL Analytics**:
   - Interactive line chart powered by Chart.js displaying cumulative equity trajectory.
3. **Execution Auditing**:
   - Full console and UI execution logs with trade timestamps, entry prices, exit prices, and realized returns.

---

## 🚀 How to Run

```powershell
python Task_07_Trade_Simulation/app.py
```
Open `http://127.0.0.1:5007` in your browser.
