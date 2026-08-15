# 📌 Task 09: API Validation & Security (Pydantic)

**Internship Role**: Backend / AI-ML Engineering Intern  
**Intern**: Priyanshu Kumar  
**Company**: Arkalogi

---

## 🎯 Objective
Establish type safety, parameter constraints, and defensive input sanitization across all financial APIs using Pydantic models. Enforces strict bounds on dates, timestamps, allowed timeframes, ticker symbols, and parameter limits.

---

## ⚙️ Key Validation Rules
1. **Date Validation**: Ensures strict `YYYY-MM-DD` ISO-8601 formatting with calendar verification.
2. **Time Validation**: Enforces 24-hour military timestamp notation (`HH:MM` format).
3. **Timeframe Restraints**: Only authorized resampling periods allowed (`1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `1d`).
4. **Position Types**: Restricts order direction to valid literals (`long`, `short`).
5. **Numerical Guards**: Bounds SMA windows ($2 \le N \le 200$) and support/resistance distances ($\ge 0\%$).

---

## 🚀 How to Run Tests

```powershell
python Task_09_API_Validation_Pydantic/test_validation.py
```
