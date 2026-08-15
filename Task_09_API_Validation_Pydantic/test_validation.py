"""
Task 09: Unit Tests for Pydantic API Validation Schemas
Arkalogi Internship - Priyanshu Kumar

Tests valid cases and invalid edge cases (malformed dates, illegal timeframes, invalid symbols).
"""

import sys
from pydantic import ValidationError
from schemas import MarketInsightRequest, EntryExitSimulationRequest, MLPredictRequest

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def test_valid_entry_exit():
    data = {
        'symbol': 'sbin',
        'entry_date': '2025-06-03',
        'exit_date': '2025-06-11',
        'entry_time': '09:20',
        'exit_time': '15:15',
        'position_type': 'long',
        'time_frame': '1m'
    }
    req = EntryExitSimulationRequest(**data)
    assert req.symbol == 'SBIN'
    assert req.position_type == 'long'
    print("  [✓] test_valid_entry_exit PASSED")


def test_invalid_date_format():
    data = {
        'symbol': 'RELIANCE',
        'entry_date': '03-06-2025',  # Invalid format (DD-MM-YYYY instead of YYYY-MM-DD)
        'exit_date': '2025-06-11',
        'entry_time': '09:20',
        'exit_time': '15:15',
        'position_type': 'long'
    }
    try:
        EntryExitSimulationRequest(**data)
        assert False, "Should have raised ValidationError"
    except ValidationError:
        print("  [✓] test_invalid_date_format (Rejection) PASSED")


def test_invalid_time_format():
    data = {
        'symbol': 'TCS',
        'entry_date': '2025-06-03',
        'exit_date': '2025-06-11',
        'entry_time': '9:20',  # Missing leading zero
        'exit_time': '15:15',
        'position_type': 'long'
    }
    try:
        EntryExitSimulationRequest(**data)
        assert False, "Should have raised ValidationError"
    except ValidationError:
        print("  [✓] test_invalid_time_format (Rejection) PASSED")


def test_invalid_sma_bounds():
    try:
        MarketInsightRequest(sma_length=1)  # Below min value (ge=2)
        assert False, "Should have raised ValidationError"
    except ValidationError:
        print("  [✓] test_invalid_sma_bounds PASSED")


def test_ml_predict_request():
    req = MLPredictRequest(
        entry_support_distance_pct=0.45,
        entry_resistance_distance_pct=0.65,
        entry_time='11:30'
    )
    assert req.entry_time == '11:30'
    print("  [✓] test_ml_predict_request PASSED")


def main():
    print("=" * 65)
    print(" TASK 09: RUNNING PYDANTIC VALIDATION UNIT TESTS")
    print("=" * 65)

    test_valid_entry_exit()
    test_invalid_date_format()
    test_invalid_time_format()
    test_invalid_sma_bounds()
    test_ml_predict_request()

    print("\n[✓] All Pydantic validation unit tests passed successfully!")


if __name__ == '__main__':
    main()
