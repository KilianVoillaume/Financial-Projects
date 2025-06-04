# Options Pricing & Payoff Visualizers

Two complementary Python tools designed to demystify options pricing and payoff mechanics — using both static and interactive visualisations.

## https://options-visualizer-kilian-voillaume.streamlit.app/
---

## 🔍 Overview

This mini-suite includes two educational applications aimed at building intuition around options contracts:

1. **📉 Payoff Diagram Generator** (`Options_visualisation.py`)  
   A script-based visualiser that illustrates the payoff profiles of standard options (long/short calls and puts), including breakeven points and strike-related behavior.

2. **📊 Streamlit Pricing App** (`Options_Streamlit.py`)  
   An interactive Black-Scholes calculator that lets users explore how changes in inputs like stock price, volatility, or interest rates impact the price of a European call or put. Includes dynamic plotting and real-time parameter adjustments.

Together, these tools provide both static structural insight and dynamic pricing intuition for beginner-to-intermediate learners in derivatives and options trading.

---

## ✨ Features

### 🧾 Options Payoff Visualizer
- Simulates payoff profiles for:
  - Long Call / Short Call
  - Long Put / Short Put
- Highlights breakeven points
- Customisable strike price and premium
- Matplotlib-based 2x2 subplot layout

### ⚙️ Streamlit Options Pricing App
- Implements the Black-Scholes model for European options
- Interactive controls for:
  - Option type (Call or Put)
  - Stock price, Strike, Volatility
  - Time to expiration, Interest rate
- Real-time calculation of theoretical price
- Dynamic visualisation of price sensitivity to any chosen parameter

---

## 📘 Concepts Covered

- **Payoff structures** and net P&L interpretation
- **Black-Scholes pricing model** and sensitivity to inputs
- Effects of:
  - Moneyness (S vs K)
  - Time value (T)
  - Volatility (σ)
  - Interest rates (r)

---

*These tools are intended for educational and demonstration purposes. They are based on theoretical pricing models and simplified assumptions.* ⚠️

