# Volatility Analysis & Modelling Suite

A set of Python tools exploring different dimensions of volatility in financial markets — from historical and implied volatility to forward-looking GARCH forecasts and term structure modelling.

---

## 🔍 Overview

This codebase is dedicated to understanding, measuring, and forecasting volatility. Each script focuses on a specific aspect of volatility, using both empirical data and theoretical models to extract insight into market dynamics.

The suite includes tools to:
- Compute **historical volatility** and rolling Sharpe ratios
- Estimate **implied volatility** using Newton’s method
- Simulate **term structure regimes** (contango vs backwardation)
- Forecast and evaluate volatility using **GARCH models**

---

## Scripts Included

- **Historical_volatility.py**  
  Calculates historical volatility and Sharpe ratios for multiple stocks using log returns.

- **Implied_Volatility_NEWTON.py**  
  Solves for implied volatility numerically using Newton’s method and `autograd`.

- **Term_structure.py**  
  Simulates synthetic term structures and volatility regimes in futures markets (contango vs backwardation).

- **Forecasting_GARCH.py**  
  Fits and evaluates GARCH models across different market regimes (e.g., GFC, COVID), comparing predicted vs realized volatility.

---

*All models are provided for academic and research use only. They rely on historical data and stylized assumptions, and are not intended for real-time investment decisions.* ⚠️
