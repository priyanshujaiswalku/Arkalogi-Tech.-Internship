# 🏛️ Task 10: Institutional Quant & Options Greeks Engine

## 🎯 Target Evaluation
Designed specifically for **Futures First**, **Axxela**, **AlphaGrep**, and quantitative proprietary trading desks.

---

## 📐 Mathematical Models & Architecture

### 1. Black-Scholes-Merton Analytical Greeks
For underlying spot $S$, strike $K$, risk-free rate $r$, volatility $\sigma$, time to expiration $T$:

$$d_1 = \frac{\ln(S/K) + (r + \frac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

- **Call Delta**: $\Delta_{CE} = N(d_1)$
- **Put Delta**: $\Delta_{PE} = N(d_1) - 1$
- **Gamma**: $\Gamma = \frac{N'(d_1)}{S \sigma \sqrt{T}}$
- **Vega**: $\mathcal{V} = \frac{S \sqrt{T} N'(d_1)}{100}$ (per 1% IV shift)
- **Theta**: Time decay per calendar day

---

### 2. Portfolio Risk & Attribution
- **Annualized Sharpe Ratio**: $\frac{\mathbb{E}[R_p - R_f]}{\sigma_p} \times \sqrt{252}$
- **Sortino Ratio**: Excess return normalized strictly by downside semi-variance.
- **Value at Risk (VaR 95% & 99%)**: Maximum probable 1-day tail loss.
- **Conditional VaR (Expected Shortfall)**: Average loss conditioned on breaching the 95% VaR threshold.
- **Kelly Criterion**: $f^* = p - \frac{q}{b}$ for optimal capital allocation.

---

### 3. Execution Friction (Indian Exchange Model)
- **STT (Securities Transaction Tax)**: 0.025% on sell intraday
- **Exchange Charges (NSE)**: 0.00345% of total turnover
- **SEBI Turnover Fee**: ₹10 per crore
- **GST**: 18% on Brokerage & Exchange fees
- **Slippage Drag**: 2 basis points (bps) execution buffer

---

## 🚀 How to Run

```bash
python Task_10_Quant_Risk_Greeks/quant_engine_cli.py
```
