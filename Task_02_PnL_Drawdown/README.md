# 📌 Task 02: Trade PnL & Drawdown Analysis (JSON / Excel)

**Internship Role**: Backend / AI-ML Engineering Intern  
**Intern**: Priyanshu Kumar  
**Company**: Arkalogi

---

## 🎯 Objective
Analyze trade performance and equity drawdowns from historical execution logs stored in JSON (`task_02.json`) or Excel (`task_02.xlsx`). Calculate individual trade profit/loss, cumulative equity curve, peak equity, drawdowns, and export core trading statistics.

---

## ⚙️ Core Logic & Formulas
1. **Trade PnL**:
   - **BUY (Long)**: $\text{PnL} = (\text{Exit Price} - \text{Entry Price}) \times \text{Quantity}$
   - **SELL (Short)**: $\text{PnL} = (\text{Entry Price} - \text{Exit Price}) \times \text{Quantity}$
2. **Cumulative PnL**: $\text{Cumulative PnL}_t = \sum_{i=1}^t \text{PnL}_i$
3. **Cumulative Peak (Equity High)**: $\text{Peak}_t = \max(\text{Cumulative PnL}_1, \dots, \text{Cumulative PnL}_t)$
4. **Drawdown**: $\text{Drawdown}_t = \text{Cumulative PnL}_t - \text{Peak}_t$
5. **Drawdown %**: $\text{Drawdown \%} = \frac{\text{Drawdown}_t}{\text{Peak}_t} \times 100$

---

## 📊 Performance Metrics Generated
- **Total Trades & Win Rate (%)**
- **Average PnL per Trade (INR)**
- **Gross Profit vs. Gross Loss & Profit Factor**
- **Maximum Drawdown (Max DD in INR and %)**
- **Top 5 Most Profitable Trades**

---

## 🚀 How to Run

```powershell
python Task_02_PnL_Drawdown/pnl_drawdown_analysis.py
```

---

## 📁 Output Artifacts
- `data/result.csv`: Summary statistics table.
- `data/top_5_profits.csv`: Top 5 highest performing trades.
- `data/task_02_with_pnl.xlsx`: Full trade book enriched with PnL, Cumulative PnL, and Drawdowns.
