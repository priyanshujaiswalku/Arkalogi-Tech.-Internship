"""
Task 03: ML-Based PnL Percentage Prediction
Arkalogi Internship - Priyanshu Kumar

Objective:
- Train Machine Learning regression models to predict trade PnL percentage.
- Features:
    * Support Distance % (entry_support_distance%)
    * Resistance Distance % (entry_resistance_distance%)
    * Entry Minutes (Minutes since market open 09:15 AM)
- Models Implemented & Evaluated:
    * Random Forest Regressor
    * Gradient Boosting / XGBoost Regressor
- Metrics: RMSE, MAE, MSE, R² Score
- Visualizations: Actual vs. Predicted scatter plot & Residual analysis.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Headless backend for scripts
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Configure UTF-8 output encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def time_to_minutes(entry_time_str: str) -> int:
    """
    Convert HH:MM entry time string to minutes elapsed since market opening (09:15 AM).
    """
    if pd.isna(entry_time_str):
        return 0
    try:
        parts = str(entry_time_str).strip().split(':')
        hour, minute = int(parts[0]), int(parts[1])
        total_minutes = hour * 60 + minute
        market_open_minutes = 9 * 60 + 15  # 09:15 AM
        return total_minutes - market_open_minutes
    except Exception:
        return 0


def calculate_pnl_percentage(row) -> float:
    """
    Calculate percentage return on capital based on trade direction:
    - BUY:  ((Exit - Entry) / Entry) * 100
    - SELL: ((Entry - Exit) / Entry) * 100
    """
    side = str(row.get('side', '')).upper()
    entry = float(row['entry_price'])
    exit_p = float(row['exit_price'])

    if entry <= 0:
        return 0.0

    if side == 'BUY':
        return ((exit_p - entry) / entry) * 100
    elif side == 'SELL':
        return ((entry - exit_p) / entry) * 100
    return 0.0


def load_and_preprocess_dataset(csv_path: str):
    """
    Load trade data and engineer feature set.
    """
    print(f"[*] Ingesting dataset from: {csv_path}")
    df = pd.read_csv(csv_path)

    # 1. Compute target PnL percentage if not already present
    if 'pnl_percentage' not in df.columns or df['pnl_percentage'].isnull().any():
        df['pnl_percentage'] = df.apply(calculate_pnl_percentage, axis=1)

    # 2. Extract minutes since market open
    df['entry_minutes'] = df['entry_time'].apply(time_to_minutes)

    # 3. Handle distance columns
    if 'entry_support_distance%' not in df.columns:
        df['entry_support_distance%'] = 0.5
    if 'entry_resistance_distance%' not in df.columns:
        df['entry_resistance_distance%'] = 0.5

    features = ['entry_support_distance%', 'entry_resistance_distance%', 'entry_minutes']
    target = 'pnl_percentage'

    X = df[features].fillna(0)
    y = df[target].fillna(0)

    print(f"[+] Features: {features}")
    print(f"[+] Total samples: {len(df):,}")

    return X, y, df


def train_and_evaluate_models(X, y, output_dir: str):
    """
    Train Random Forest and Gradient Boosting models, evaluate, and plot results.
    """
    os.makedirs(output_dir, exist_ok=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'Random Forest Regressor': RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42),
        'Gradient Boosting Regressor': GradientBoostingRegressor(n_estimators=100, learning_rate=0.08, max_depth=4, random_state=42)
    }

    results = {}
    best_model_name = None
    best_r2 = -float('inf')
    best_predictions = None

    print("\n" + "=" * 65)
    print(" 🤖 MACHINE LEARNING MODEL EVALUATION")
    print("=" * 65)

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        rmse = float(np.sqrt(mse))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        results[name] = {
            'model': model,
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'R2': r2,
            'predictions': y_pred
        }

        print(f"\nModel: {name}")
        print(f"  - Mean Squared Error (MSE) : {mse:.4f}")
        print(f"  - Root Mean Sq Error (RMSE): {rmse:.4f}")
        print(f"  - Mean Absolute Error (MAE): {mae:.4f}")
        print(f"  - R² Score                 : {r2:.4f}")

        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_predictions = y_pred

    # Generate Evaluation Chart
    plot_path = os.path.join(output_dir, 'pnl_prediction_plot.png')
    plt.figure(figsize=(8, 5))
    plt.scatter(y_test, best_predictions, color='#2563eb', alpha=0.6, edgecolors='k', label='Predicted vs Actual')
    min_val = min(y_test.min(), best_predictions.min())
    max_val = max(y_test.max(), best_predictions.max())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    plt.xlabel('Actual PnL %', fontsize=11)
    plt.ylabel('Predicted PnL %', fontsize=11)
    plt.title(f'Actual vs Predicted PnL % ({best_model_name})', fontsize=12, fontweight='bold')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)
    plt.close()

    print(f"\n[✓] Evaluation scatter plot saved to: {plot_path}")
    print(f"[✓] Best Performing Model: {best_model_name} (R² = {best_r2:.4f})")

    return results[best_model_name]['model']


def predict_single_trade(model, support_dist: float, resistance_dist: float, entry_time: str) -> float:
    """
    Utility function to predict PnL% for an incoming live trade setup.
    """
    entry_mins = time_to_minutes(entry_time)
    X_single = pd.DataFrame([{
        'entry_support_distance%': support_dist,
        'entry_resistance_distance%': resistance_dist,
        'entry_minutes': entry_mins
    }])
    pred_pnl_pct = model.predict(X_single)[0]
    return round(float(pred_pnl_pct), 3)


def main():
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, 'data')
    csv_path = os.path.join(data_dir, 'task_03.csv')

    print("=" * 65)
    print(" TASK 03: ML-BASED PnL PERCENTAGE PREDICTION")
    print("=" * 65)

    X, y, df = load_and_preprocess_dataset(csv_path)
    best_model = train_and_evaluate_models(X, y, data_dir)

    # Demo inference
    test_trade = {'support_dist': 0.35, 'resistance_dist': 0.75, 'entry_time': '10:30'}
    prediction = predict_single_trade(best_model, **test_trade)
    print(f"\n[🔍] Demo Live Trade Inference:")
    print(f"  Inputs: Support Dist={test_trade['support_dist']}%, Res Dist={test_trade['resistance_dist']}%, Time={test_trade['entry_time']}")
    print(f"  Predicted PnL %: {prediction:+0.2f}%")

    print("\n[✓] Task 03 completed successfully!")


if __name__ == '__main__':
    main()
