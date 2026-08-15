# 📌 Task 03: ML-Based PnL Percentage Prediction

**Internship Role**: Backend / AI-ML Engineering Intern  
**Intern**: Priyanshu Kumar  
**Company**: Arkalogi

---

## 🎯 Objective
Build and evaluate supervised Machine Learning regression models to predict expected trade return percentage ($\text{PnL \%}$) using structural technical features (distance to key support and resistance levels) and time-of-day market seasonality.

---

## 🔬 Feature Engineering & Formulation
1. **Target Variable**:
   $$\text{PnL \%} = \begin{cases} \left(\frac{\text{Exit Price} - \text{Entry Price}}{\text{Entry Price}}\right) \times 100 & \text{if Side} = \text{BUY} \\ \left(\frac{\text{Entry Price} - \text{Exit Price}}{\text{Entry Price}}\right) \times 100 & \text{if Side} = \text{SELL} \end{cases}$$
2. **Feature Matrix**:
   - `entry_support_distance%`: Percentage distance from entry price to nearest underlying support level.
   - `entry_resistance_distance%`: Percentage distance from entry price to nearest underlying resistance level.
   - `entry_minutes`: Elapsed trading minutes from market open (09:15 AM IST).

---

## 🤖 Algorithms Evaluated
- **Random Forest Regressor** (Ensemble Bagging)
- **Gradient Boosting Regressor** (Ensemble Boosting)

---

## 📈 Evaluation Metrics
- **Mean Squared Error (MSE)**
- **Root Mean Squared Error (RMSE)**
- **Mean Absolute Error (MAE)**
- **Coefficient of Determination ($R^2$ Score)**

---

## 🚀 How to Run

```powershell
python Task_03_ML_PnL_Prediction/ml_pnl_prediction.py
```

---

## 📁 Output Artifacts
- `data/task_03.csv`: Prepared dataset with engineered features.
- `data/pnl_prediction_plot.png`: Actual vs. Predicted scatter plot.
