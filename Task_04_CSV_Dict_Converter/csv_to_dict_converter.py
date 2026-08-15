"""
Task 04: CSV to Python Dictionary Converter
Arkalogi Internship - Priyanshu Kumar

Objective:
- Convert arbitrary CSV records into highly accessible, structured nested Python dictionaries.
- Support single-key indexing (e.g., ID -> Record) and multi-level composite indexing (e.g., Symbol -> Date -> Record).
- Provide clean export utilities (JSON, Pretty Print, In-memory lookup).
"""

import os
import sys
import csv
import json
from typing import Dict, Any, List, Union

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def csv_to_flat_dict(csv_path: str, primary_key: str = 'id') -> Dict[Any, Dict[str, Any]]:
    """
    Convert CSV to a dictionary indexed by a specified primary key column.
    Example: {1: {'name': 'Alice', 'age': 30, 'department': 'Engineering'}, ...}
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    nested_dict = {}
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Type cast key if numeric
            raw_key = row.get(primary_key)
            if raw_key is None:
                raise KeyError(f"Primary key '{primary_key}' not found in CSV headers.")

            key = int(raw_key) if raw_key.isdigit() else raw_key
            record = {}
            for col, val in row.items():
                if col != primary_key:
                    # Attempt automatic type casting
                    if val.isdigit():
                        record[col] = int(val)
                    else:
                        try:
                            record[col] = float(val)
                        except ValueError:
                            record[col] = val
            nested_dict[key] = record

    return nested_dict


def csv_to_multilevel_dict(csv_path: str, key_hierarchy: List[str]) -> Dict[str, Any]:
    """
    Convert CSV into multi-level nested dictionaries.
    Example key_hierarchy: ['symbol', 'entry_date']
    Produces: { 'APOLLOHOSP': { '2024-01-01': [ {...trade...} ] } }
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    result = {}
    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            current_level = result
            for i, key in enumerate(key_hierarchy[:-1]):
                val = row.get(key, 'UNKNOWN')
                if val not in current_level:
                    current_level[val] = {}
                current_level = current_level[val]

            last_key = key_hierarchy[-1]
            last_val = row.get(last_key, 'UNKNOWN')
            if last_val not in current_level:
                current_level[last_val] = []
            current_level[last_val].append(row)

    return result


def main():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    emp_csv = os.path.join(data_dir, 'employees.csv')

    print("=" * 65)
    print(" TASK 04: CSV TO STRUCTURED PYTHON DICTIONARY CONVERTER")
    print("=" * 65)

    if not os.path.exists(emp_csv):
        print(f"[*] Creating sample employees.csv at: {emp_csv}")
        sample_employees = {
            1: {'name': 'Alice', 'age': 30, 'department': 'Engineering'},
            2: {'name': 'Bob', 'age': 25, 'department': 'Marketing'},
            3: {'name': 'Charlie', 'age': 35, 'department': 'Sales'},
            4: {'name': 'Diana', 'age': 28, 'department': 'HR'},
            5: {'name': 'Ethan', 'age': 40, 'department': 'Finance'}
        }
        with open(emp_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'age', 'department'])
            for emp_id, info in sample_employees.items():
                writer.writerow([emp_id, info['name'], info['age'], info['department']])

    # 1. Test Flat Dict Conversion
    print("\n[*] Converting employees.csv to Python dictionary indexed by 'id'...")
    converted_dict = csv_to_flat_dict(emp_csv, primary_key='id')
    print(f"[+] Total records converted: {len(converted_dict)}")
    print("\nSample converted dictionary representation:")
    for k, v in list(converted_dict.items())[:3]:
        print(f"  Key ({k}) -> {v}")

    # 2. Export sample as JSON
    json_export_path = os.path.join(data_dir, 'employees_converted.json')
    with open(json_export_path, 'w', encoding='utf-8') as f:
        json.dump(converted_dict, f, indent=4)
    print(f"\n[✓] Converted dictionary saved to JSON: {json_export_path}")

    print("\n[✓] Task 04 completed successfully!")


if __name__ == '__main__':
    main()
