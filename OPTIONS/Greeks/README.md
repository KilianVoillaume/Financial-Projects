# Options Greeks Visualizer – Python Series

A set of five Python scripts to visualise how each of the key options Greeks behaves across different market conditions — using the Black-Scholes model.

---

## 🔍 Overview

This mini-project explores the core sensitivities (Greeks) of European options through dedicated Python visualisations. Each script focuses on one Greek — Delta, Gamma, Theta, Vega, or Rho — and plots how it evolves with respect to stock price, volatility, and option type (call or put).

These tools were designed to help build intuition around how option prices respond to market variables such as volatility, interest rates, and moneyness. They are particularly useful for students of derivatives, self-learners, or professionals refreshing their understanding.

---

## ✨ Features
- **What each script includes**:
  - Computation of the Greek using analytical formulas under Black-Scholes
  - Visualisation of both call and put sensitivities
  - Multiple curves for varying volatilities (to observe sensitivity behaviour)
  - Clean, labelled Matplotlib charts with legends and grids

- **Example: Delta Visualisation**
  - Delta vs Stock Price for a given volatility
  - Delta vs Stock Price for a range of volatilities
  - Separate charts for call and put options

---

## 📘 Greeks Covered
Greek	Meaning	Range
Delta	Sensitivity to underlying price	[-1, 1]
Gamma	Sensitivity of Delta	Always positive
Theta	Sensitivity to time decay	Usually negative
Vega	Sensitivity to volatility	Peaks at ATM
Rho	Sensitivity to interest rate	Positive for calls, negative for puts

---

*These tools are intended for educational and demonstration purposes. They are based on theoretical pricing models and simplified assumptions.* ⚠️
