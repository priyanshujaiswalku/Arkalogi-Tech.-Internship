# 📌 Task 05: Market Insight (SMA Based API)

**Internship Role**: Backend / AI-ML Engineering Intern  
**Intern**: Priyanshu Kumar  
**Company**: Arkalogi

---

## 🎯 Objective
Build a Flask-based Market Insight API and Web Interface that computes Simple Moving Averages (SMA) across NIFTY50 stocks and classifies them into Bullish (`above_sma`) and Bearish (`below_sma`) cohorts based on user-defined SMA parameters.

---

## ⚙️ Features
1. **Dynamic SMA Computation**:
   - Calculates rolling Simple Moving Averages for any user input window length ($N$ days).
2. **Dual Mode Ingestion**:
   - Uses local daily OHLC CSV cache with automatic fallback to live Yahoo Finance (`yfinance`) feeds.
3. **Dual Interface**:
   - Web UI for interactive parameter tuning and visual categorization.
   - RESTful JSON API endpoint (`/api/market_insight`) for programmatic consumption.

---

## 🚀 How to Run

```powershell
python Task_05_Market_Insight_SMA/app.py
```
Open your browser at `http://127.0.0.1:5005`.

---

## 📡 API Example
**Request:**
```http
POST /api/market_insight
Content-Type: application/json

{
    "sma_length": 20
}
```

**Response:**
```json
{
    "sma_length": 20,
    "above_sma": ["RELIANCE", "TCS", "INFY", "HDFCBANK"],
    "below_sma": ["SBIN", "TATAMOTORS", "ITC"],
    "details": [...]
}
```
