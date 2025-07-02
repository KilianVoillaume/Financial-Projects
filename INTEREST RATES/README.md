# Interest Rate Modelling Suite – Short Rates, HJM & Volatility Surfaces

A Python-based toolkit exploring the fundamental models used to simulate and understand the evolution of interest rates, yield curves, and implied volatility structures. This project brings together short-rate models (Vasicek, CIR, Hull-White), forward rate curve dynamics (HJM), and implied volatility surface calibration (LMM).

---

## 📘 Related Article

This project is linked to:  
👉 [Financial_Market_Uncovered_Article11_Interest_Rate_Modelling](https://github.com/KilianVoillaume/Financial_Market_Uncovered_Articles)

---

## 🔍 Overview

Interest rate models form the backbone of pricing and risk management for fixed income products, interest rate derivatives, and structured notes. This suite enables you to:

- Simulate the dynamics of short rates using classical models (Vasicek, CIR, Hull-White)
- Observe how term structures evolve under different volatility assumptions using the **Heath-Jarrow-Morton (HJM)** framework
- Calibrate and visualise implied volatility surfaces for caplets using the **Libor Market Model (LMM)**

Each module is written for clarity, replicability, and educational depth, with plots and diagnostics to interpret model behavior and realism.

---

## 📘 Modules Included

- `short_rate_model_compairons.py`  
  Simulates and compares the stochastic dynamics of Vasicek, CIR, and Hull-White models. Includes forward rate behavior, rolling volatility, and terminal distribution plots.

- `term_structure_evolution_HJM.py`  
  Implements the HJM model with support for constant, humped, and two-factor volatility structures. Simulates the full forward rate surface over time and visualises curve steepening/flattening.

- `LMM_forward_rate_vol_surface.py`  
  Calibrates the LMM volatility surface to synthetic market data using strike, maturity, and moneyness effects. Produces heatmaps, 3D surfaces, and cross-sectional comparisons of market vs. model implied vols.

---

*This suite is intended for educational and analytical purposes only. The models are stylised and should not be used for production risk systems or live pricing.* ⚠️
