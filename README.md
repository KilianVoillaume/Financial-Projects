# 🧠 Financial Market Notebooks

A personal collection of Python notebooks and visual tools exploring advanced concepts in financial markets — from options and Greeks to volatility, swaps, credit, and market microstructure.

---

## 🔍 Overview

This repository brings together a series of independent yet thematically connected projects built to deepen understanding of how financial instruments behave, how markets function, and how quantitative models can be implemented and visualised.

Each module focuses on a specific concept — such as options pricing, volatility modelling, or execution mechanics — and is supported by real mathematical foundations and coding practices drawn from quantitative finance literature and practitioner insights. The goal is not only to compute, but to **understand**.

These tools are designed to be educational, intuitive, and extendable — serving traders, students, researchers, and curious minds looking to bridge theory and practice in markets.

---

## ✨ Topics Covered

The repository spans a wide range of market-relevant themes, including:

- **📘 Options & Derivatives**
  - Black-Scholes pricing
  - Option Greeks (Delta, Gamma, Theta, Vega, Rho)
  - Payoff visualisations (long/short calls & puts)
  - Exotic options (barriers, binaries, Asians, etc.)

- **🌪️ Volatility Modelling**
  - Historical vs. implied volatility
  - Smiles, skews, and surfaces
  - Volatility dynamics and risk-neutral interpretation

- **📈 Market Microstructure**
  - Order book dynamics
  - Execution strategies (TWAP, VWAP, Sniper)
  - Spread, slippage, and latency mechanics

- **💵 Interest Rates & Swaps**
  - Fixed vs. floating structures
  - DV01, PVBP, and swap curve mechanics
  - Pricing and sensitivity of swaps under different curves

- **⚠️ Credit & Risk**
  - Credit default swaps (CDS) mechanics
  - Risk metrics (VaR, CVaR, Expected Shortfall)
  - Portfolio Greeks and exposure visualisation

- **🧮 Quantitative Methods**
  - Monte Carlo simulations
  - Stochastic processes (Brownian motion, jump diffusion)
  - Analytical vs. numerical solution methods

- **...and more...**
---

## 🛠 Structure & Usage

Each project is self-contained, usually in the form of a Python script or Jupyter notebook. Several projects include:

- Mathematical explanations or derivations
- Interactive visualisations (via Matplotlib or Streamlit)
- Modular functions for further development

---

## 📚 Data & References
Most projects are based on analytical models and use no external data. When data is needed, it is either:
- Simulated using numpy or scipy
- Sourced from public APIs or open datasets (Yahoo Finance, FRED, etc.)

Foundational references used across this repository include:
- Hull, Options, Futures, and Other Derivatives
- Glasserman, Monte Carlo Methods in Financial Engineering
- Gatheral, The Volatility Surface
- Bouchaud et al., Market Microstructure and Liquidity
- Wilmott, Paul Wilmott Introduces Quantitative Finance
- ...

---
*All material is provided for educational and research purposes only. This repository does not constitute financial advice or a recommendation to trade any financial instrument.* ⚠️
