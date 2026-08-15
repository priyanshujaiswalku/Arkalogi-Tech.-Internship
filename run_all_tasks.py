"""
Arkalogi Internship - Master Task Runner & Verification Suite
Priyanshu Kumar

Runs and verifies all individual task scripts sequentially:
- Task 01: Option Symbol Filtering
- Task 02: Trade PnL & Drawdown Analysis
- Task 03: ML-Based PnL Percentage Prediction
- Task 04: CSV to Python Dictionary Converter
- Task 09: Pydantic Validation Unit Tests
"""

import os
import sys
import subprocess

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

TASK_SCRIPTS = [
    ('Task 01: Option Symbol Filtering', os.path.join(ROOT_DIR, 'Task_01_Option_Filtering', 'option_filtering.py')),
    ('Task 02: Trade PnL & Drawdown', os.path.join(ROOT_DIR, 'Task_02_PnL_Drawdown', 'pnl_drawdown_analysis.py')),
    ('Task 03: ML PnL Prediction', os.path.join(ROOT_DIR, 'Task_03_ML_PnL_Prediction', 'ml_pnl_prediction.py')),
    ('Task 04: CSV to Dict Converter', os.path.join(ROOT_DIR, 'Task_04_CSV_Dict_Converter', 'csv_to_dict_converter.py')),
    ('Task 09: Pydantic Validation Tests', os.path.join(ROOT_DIR, 'Task_09_API_Validation_Pydantic', 'test_validation.py')),
]


def run_all():
    print("=" * 75)
    print(" 🚀 ARKALOGI INTERNSHIP: RUNNING ALL VERIFICATION TASKS")
    print("=" * 75)

    passed = 0
    failed = 0

    for name, script_path in TASK_SCRIPTS:
        print(f"\n[▶] Running {name}...")
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=os.path.dirname(script_path),
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60
            )
            if result.returncode == 0:
                print(f"  [✓] {name} SUCCESSFUL")
                passed += 1
            else:
                print(f"  [✗] {name} FAILED (Exit Code: {result.returncode})")
                print("  Error output:\n", result.stderr[:300])
                failed += 1
        except Exception as e:
            print(f"  [✗] Exception running {name}: {e}")
            failed += 1

    print("\n" + "=" * 75)
    print(f" 📊 TEST EXECUTION SUMMARY: {passed} PASSED, {failed} FAILED")
    print("=" * 75)


if __name__ == '__main__':
    run_all()
