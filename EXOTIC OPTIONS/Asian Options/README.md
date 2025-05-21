# 🧮 Asian Options & Averaging Dynamics

A collection of Python scripts to explore and visualise how **Asian options** behave compared to vanilla options — with a focus on volatility sensitivity, payoff structures, and the averaging process under Monte Carlo simulations.

---

## 🔍 Overview

These tools are designed to build financial intuition around **path-dependent options**. They simulate price paths using geometric Brownian motion and compare the mechanics, pricing, and greeks of **Asian-style options** to traditional vanilla calls. Key concepts such as vega dampening, payoff smoothing, and average vs spot dynamics are all illustrated visually and quantitatively.

---

## 📘 Scripts Included

- **Option_vs_volatility.py**  
  Compares how vanilla and Asian call options respond to changes in implied volatility, both in terms of price and vega sensitivity.

- **Payoff_vanilla_asian.py**  
  Demonstrates the payoff difference between a vanilla call and an Asian call on the same simulated path — highlighting the impact of averaging on payout and risk.

- **MonteCarlo_Avg_vs_Spot.py**  
  Visualises the evolution of spot price vs cumulative average price across multiple simulated paths, showing how averaging affects volatility smoothing and payoff lag.

---

## 🎯 Educational Focus

This suite is especially useful for:
- Understanding how averaging alters risk-return characteristics
- Demonstrating why Asian options have lower Vega than vanilla options
- Visualising the smoothing effect and lag of average-based payoffs
- Comparing Greek sensitivities across path-dependent and standard derivatives

---

*These simulations are intended for educational purposes and do not represent live market pricing or financial advice.* ⚠️
