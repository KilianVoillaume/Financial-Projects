# Monte Carlo Option Pricing – Basic & Antithetic Variates

A two-part Python toolkit for pricing European options via Monte Carlo simulation, including a baseline implementation and a variance reduction technique using Antithetic Variates for improved accuracy and convergence.

---

## 🔍 Overview

These scripts explore how Monte Carlo methods can be used to estimate the fair value of European-style options. While the Black-Scholes formula provides a closed-form solution, Monte Carlo techniques are particularly valuable for pricing more complex or path-dependent derivatives.

This project includes:
- A foundational implementation of Monte Carlo for option pricing.
- A comparative analysis of pricing accuracy and error reduction using Antithetic Variates.
- Visual tools to illustrate convergence, standard error, and deviations from market price.

---

## ✨ Tools Included

### `MC_Options_Pricing_BASIC.py`
- Simulates option prices under the geometric Brownian motion model.
- Implements:
  - A **slow loop-based** Monte Carlo estimate
  - A **fast vectorised** alternative
  - A **one-step (final state only)** simulation
- Computes:
  - Present value using risk-neutral pricing
  - Standard deviation and standard error of estimate
- Visualises:
  - Option price convergence
  - Standard deviation regions vs theoretical and market value

### `MC_Variance_Reduction_Antithetic_Variates.py`
- Uses **Antithetic Variates** to reduce variance in Monte Carlo estimates
- Compares:
  - Standard Monte Carlo vs. Antithetic-enhanced results
  - Standard error (SE) between methods
  - Market price vs. simulated fair value
- Provides a detailed **distribution plot** showing:
  - Simulated outcome densities
  - One/two standard deviation zones
  - Market price and theoretical value

---

## 📘 Concepts Covered

- Monte Carlo simulation under risk-neutral measure  
- Discrete geometric Brownian motion  
- Antithetic Variates as a variance reduction technique  
- Option payoff averaging  
- Discounting and expectation under Black-Scholes assumptions  
- Convergence diagnostics and distribution visualisation  

---
*These models are educational tools for understanding pricing techniques. They are not designed for use in live trading or production environments.* ⚠️

