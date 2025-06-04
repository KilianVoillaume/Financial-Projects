# EXOTIC OPTIONS – Simulation & Pricing Toolkit

This directory brings together multiple Python-based tools for modelling, simulating, and visualising the behavior of **exotic options** — derivatives whose payoffs depend on paths, conditions, or exotic features beyond standard vanilla contracts.

---

## 📘 **Related Article:**  
See the full write-up and explanation in the companion article:  
👉 [Financial_Market_Uncovered_Article7_Exotic_Options](https://github.com/KilianVoillaume/Financial_Market_Uncovered_Articles)

---

## 🔍 Overview

While vanilla options depend solely on the terminal value of the underlying, exotic options introduce more complex features like path dependency, barrier activation, average pricing, return truncation, or digital payout structures.

This folder includes dedicated scripts to explore:

- **Asian Options**: Averaging mechanics and Vega dampening  
- **Barrier Options**: Knock-in/knock-out activation and Monte Carlo path classification  
- **Cliquet Options**: Accumulated capped/floored returns with smoothing effects  
- **Digital Options**: Discontinuous payouts and sharp delta spikes near maturity  
- **Lookback Options**: Path maxima/minima affecting floating strike valuations  

Each subproject uses either deterministic price paths or Monte Carlo simulations to highlight the unique risk and return characteristics of these instruments.

---

## 🎯 Learning Objectives

Across the tools, users can:

- Build visual intuition around path-dependent payoffs  
- Compare vanilla and exotic sensitivities under the same market conditions  
- Understand how barriers, caps, and averaging alter pricing and hedging  
- Observe risk-limiting features designed into structured products  

---

*These tools are designed for educational and research purposes only. They rely on stylized assumptions and do not represent real-time trading systems or financial advice.* ⚠️

