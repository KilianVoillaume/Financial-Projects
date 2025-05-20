# 📈 Black-Scholes Pricing & Sensitivity Visualizer Suite

A collection of Python tools to compute, validate, and visualise option prices using the Black-Scholes model — with a focus on parameter sensitivity and pricing intuition.

---

## 🔍 Overview

This suite includes three distinct modules that explore the mechanics and behavior of European options pricing under the Black-Scholes framework. These tools are designed to support both theoretical validation and intuitive understanding of how inputs like time to maturity, volatility, interest rate, and dividends affect option value.

It includes:
- **Analytical price comparison** with a reference implementation
- **2D visualisation** of parameter sensitivities (subplots)
- **Heatmaps** showing how different inputs influence pricing across spot ranges

---

## ✨ Tools Included

### 🔢 `BS_model.py`
- Implements the analytical Black-Scholes formula for call and put options (dividend-adjusted)
- Compares custom implementation with a reference pricing class
- Outputs discrepancies for validation and debugging

### 📊 `Influence_param_on_option_price.py`
- Plots **four subplots** showing the effect of:
  - Time to maturity  
  - Volatility  
  - Interest rate  
  - Dividend yield  
- Separate curves for call and put options
- Highlights how each input shifts pricing and where convexity arises

### 🌡️ `Heatmap_Param_Influence_Jupyter.py`
- Generates **heatmaps** for call and put option prices
- Varies one parameter at a time (time, vol, rates, dividend)
- Shows impact across a range of spot prices for deeper dimensional insight
- Uses Seaborn and Matplotlib for clean, annotated charts

---

## 📘 Concepts Covered

- Black-Scholes option pricing theory  
- Role of inputs: spot price, strike, time, volatility, risk-free rate, dividends  
- Call vs put option behavior  
- Pricing convexity and non-linear sensitivity  
- Visual interpretation of option pricing surfaces  

---

*All scripts provided are for educational and research purposes only. They are based on idealised assumptions and do not constitute trading or investment advice.* ⚠️

