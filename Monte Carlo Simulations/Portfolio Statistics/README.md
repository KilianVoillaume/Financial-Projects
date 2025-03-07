# Monte Carlo Portfolio Simulation and Risk Analysis

This repository contains two Python scripts that utilize **Monte Carlo simulations** to analyze stock portfolios. The simulations estimate portfolio performance and calculate financial risk measures such as **Value at Risk (VaR)** and **Conditional Value at Risk (CVaR)**.

## Table of Contents
- [MC_Stock_Portfolio.py](#mc_stock_portfoliopy)
- [MC_VaR_CVaR.py](#mc_var_cvarpy)
- [Requirements](#requirements)
- [Usage](#usage)

---

## MC_Stock_Portfolio.py

This script simulates the future value of a stock portfolio using **Monte Carlo simulations**.

### Key Features:
- Retrieves historical stock data using **Yahoo Finance**.
- Computes **mean daily returns** and **covariance matrix** for selected stocks.
- Assigns **random weights** to each stock to create a portfolio.
- Runs **Monte Carlo simulations** to model portfolio value over a specified time horizon.
- Uses the **Cholesky decomposition** to incorporate realistic correlations between assets.
- Visualizes the **distribution of simulated portfolio values** over time.

### Output:
- A **line plot** showing multiple Monte Carlo simulated portfolio paths over time.

---

## MC_VaR_CVaR.py

This script expands on the **Monte Carlo simulation** by calculating financial risk measures:  
**Value at Risk (VaR)** and **Conditional Value at Risk (CVaR).**

### Key Features:
- Fetches historical stock prices and calculates **returns**.
- Uses the **Dirichlet distribution** to generate **better diversified portfolio weights**.
- Ensures the covariance matrix is **positive semi-definite** before applying **Cholesky decomposition**.
- Performs **Monte Carlo simulations** for portfolio value evolution.
- Computes **VaR** (5% worst loss threshold) and **CVaR** (expected shortfall beyond VaR).
- Generates multiple **visualizations**, including:
  - A **histogram of portfolio returns** with VaR & CVaR marked.
  - A **histogram of final portfolio values** with VaR & CVaR levels.
  - A **line plot of Monte Carlo portfolio simulations**.

### Output:
- **Value at Risk (VaR)** and **Conditional Value at Risk (CVaR)** in percentage and absolute dollar terms.
- Three **visualizations** for portfolio risk assessment.

---

## Requirements

Ensure you have the following Python libraries installed:

```bash
pip install numpy pandas matplotlib yfinance
```

## Usage
Run either script to simulate stock portfolio performance and risk:
```bash
python MC_Stock_Portfolio.py
```
```bash
python MC_VaR_CVaR.py
```
Modify the stocks list in each script to analyze different stock portfolios

# Author
Kilian Voillaume





