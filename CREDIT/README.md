# Credit Risk & Structured Products – Simulation Toolkit

A suite of Python scripts dedicated to modelling, simulating, and visualising core concepts in credit risk management, credit derivatives, and structured finance products.

---

## 📘 Related Article

This project is developed alongside:  
👉 [Financial_Market_Uncovered_Article8_Credit_Risk_Unveiled](https://github.com/KilianVoillaume/Financial_Market_Uncovered_Articles)

---

## 🔍 Overview

This toolkit provides hands-on tools to explore fundamental credit risk mechanics, ranging from expected loss calculations and rating transitions to portfolio loss distributions and synthetic collateralized debt obligations (CDOs). It is particularly relevant for learners and professionals aiming to understand:

- The mathematical structure of **expected loss and survival models**
- The use of **credit rating transition matrices** in risk modelling
- How **CDS spreads** link to default probabilities and recovery rates
- The simulation of **loss distributions**, **VaR**, and **CVaR** in credit portfolios
- The behavior of **CDO tranche risk** under correlated defaults using Gaussian copulas

---

## 📘 Scripts Included

- `expected_loss.py` — Visualises the impact of recovery rates on expected credit loss  
- `survival_probability_curve.py` — Plots exponential survival curves based on default intensities  
- `credit_rating_transition_matrix.py` — Generates and visualises a synthetic 1-year transition matrix from AAA to default  
- `CDS_spread_vs_default_probability.py` — Demonstrates the credit triangle: how CDS spreads reflect default risk and recovery assumptions  
- `loss_distribution.py` — Simulates credit portfolio loss distributions and computes VaR/CVaR  
- `tranche_expected_loss.py` — Uses a Gaussian copula model to show how correlation affects expected losses in synthetic CDO tranches  

---

## 🎯 Educational Objectives

- Quantify credit risk using analytical and simulation methods  
- Understand how credit rating migrations affect credit portfolio risk  
- Compare tranche risk based on correlation and seniority  
- Visualise key relationships between credit instruments and underlying risk drivers  

---

*This toolkit is designed for educational and analytical purposes only. All models are simplified and based on stylised assumptions. Not intended for live risk management or trading.* ⚠️
