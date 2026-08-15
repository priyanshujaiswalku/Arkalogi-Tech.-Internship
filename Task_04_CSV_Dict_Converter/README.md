# 📌 Task 04: CSV to Python Dictionary Converter

**Internship Role**: Backend / AI-ML Engineering Intern  
**Intern**: Priyanshu Kumar  
**Company**: Arkalogi

---

## 🎯 Objective
Convert tabular CSV records into structured, high-performance nested Python dictionaries to enable $O(1)$ memory access, dynamic nesting, and fast lookup in trading and analytics workflows.

---

## ⚙️ Features
1. **Primary Key Indexed Dictionary**:
   - Ingests rows and indexes records by unique identifier (e.g. `id`, `symbol`, or custom key).
   - Automatically handles datatype casting (integers, floats, strings).
2. **Multi-Level Hierarchy Builder**:
   - Constructs nested sub-dictionaries using arbitrary key sequences (e.g. `symbol` $\rightarrow$ `date` $\rightarrow$ `trade list`).
3. **JSON Serialization & Export**:
   - Converts Python dictionary representation directly to formatted JSON.

---

## 🚀 How to Run

```powershell
python Task_04_CSV_Dict_Converter/csv_to_dict_converter.py
```

---

## 📁 Output Artifacts
- `data/employees.csv`: Sample relational data.
- `data/employees_converted.json`: Exported structured JSON dictionary.
