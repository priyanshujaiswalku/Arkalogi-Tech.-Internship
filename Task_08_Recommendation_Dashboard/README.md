# 📌 Task 08: Strategy Recommendation Dashboard

**Internship Role**: Backend / AI-ML Engineering Intern  
**Intern**: Priyanshu Kumar  
**Company**: Arkalogi

---

## 🎯 Objective
Create an interactive technical analysis and strategy recommendation dashboard. Calculates multiple quantitative indicators (SMA, EMA, RSI, Stochastic RSI), evaluates multi-factor buy/sell/hold conditions with confidence percentages, and tracks core benchmark indices.

---

## ⚙️ Technical Indicators
1. **Simple Moving Average (SMA)**: $14$-period moving average of close prices.
2. **Exponential Moving Average (EMA)**: $14$-period exponential decay moving average.
3. **Relative Strength Index (RSI)**: $14$-period momentum oscillator ($0 - 100$).
   - RSI $< 30 \implies$ **Buy Signal (+25% confidence)**
   - RSI $> 70 \implies$ **Sell Signal (+25% confidence)**
4. **Stochastic RSI (StochRSI)**: Relative position of RSI within its rolling min/max.
   - StochRSI $< 0.2 \implies$ **Buy Signal (+15% confidence)**
   - StochRSI $> 0.8 \implies$ **Sell Signal (+15% confidence)**

---

## 🚀 How to Run

```powershell
python Task_08_Recommendation_Dashboard/app.py
```
Open `http://127.0.0.1:5008` in your browser.
