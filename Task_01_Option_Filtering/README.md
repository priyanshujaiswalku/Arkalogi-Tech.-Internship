# 📌 Task 01: NIFTY50 Option Symbol Filtering (CSV)

**Internship Role**: Backend / AI-ML Engineering Intern  
**Intern**: Priyanshu Kumar  
**Company**: Arkalogi

---

## 🎯 Objective
Extract and process options (`CE`, `PE`) and futures (`FUT`) contracts for NIFTY50 instruments from Zerodha/Kite master instruments CSV (`nse_master_raw.csv`) using handcrafted algorithms without relying on Regular Expressions (`re` module).

---

## ⚙️ Approach & Methodology
1. **Master CSV Parsing**: Ingestion of over 100,000+ instrument records from Zerodha's instrument dump.
2. **NFO Contract Filtering**:
   - Filter records where `exchange` belongs to `NFO`.
   - Filter trading symbols ending with `CE`, `PE`, or `FUT`.
3. **Handcrafted Expiry Extraction (No Regex Constraint)**:
   - Slices and searches for lowercase month tokens (`jan`, `feb`, ... `dec`).
   - Backward character traversal to capture leading numerical digits (e.g. `24JUL`, `30JAN`).
4. **NIFTY50 Equity Filtering**:
   - Filters `NSE:EQ` instruments matching all 50 underlying constituents.
5. **Data Export**:
   - `data/filtered_contracts_with_date.csv`
   - `data/nifty50_stocks.csv`

---

## 🚀 How to Run

```powershell
# From root or Task directory:
python Task_01_Option_Filtering/option_filtering.py
```

---

## 📊 Sample Output
```
[*] Reading master instrument file: nse_master_raw.csv
[+] Total instruments loaded: 114,845
[+] NFO Options & Futures matched: 52,190
[*] Extracting expiry date using handcrafted string slicing (No Regex)...
[✓] Saved filtered contracts to: data/filtered_contracts_with_date.csv
[✓] Saved NIFTY50 stocks to: data/nifty50_stocks.csv
[✓] Task 01 completed successfully!
```
