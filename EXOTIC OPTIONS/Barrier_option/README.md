# Barrier Options – Payoff & Path Simulation Toolkit

This toolkit offers visual and quantitative tools to explore how barrier options behave, both in terms of **payoff mechanics** and **path-dependent activation** using Monte Carlo simulations.

---

## 🔍 Overview

Barrier options — like knock-in and knock-out structures — are path-dependent derivatives that only activate (or extinguish) if the underlying asset crosses a predefined barrier. These tools help illustrate:

- The difference in payoff outcomes between vanilla, knock-in, and knock-out options
- How barrier breaches affect path validity in simulations
- The intuition behind dynamic hedging and risk transfer for structured products

---

## 📘 Scripts Included

- **Payoff_Vanilla_KnockIn_KnockOut.py**  
  Visualises and compares the payoff profiles of vanilla, knock-in, and knock-out options across different market scenarios, with interactive controls for minimum price.

- **MonteCarlo_With_BarrierActivation.py**  
  Simulates geometric Brownian motion paths and classifies them based on whether they breach a barrier (for knock-in or knock-out options), showing the ratio of valid vs invalid paths and colouring accordingly.

---

## 🎯 Educational Applications

These scripts are ideal for:
- Understanding how barrier activation affects payouts and pricing
- Teaching the difference between *path-independent* and *path-dependent* derivatives
- Demonstrating the probabilistic nature of activation and extinguishment

---

*All content is for educational purposes only and is not intended for real-time trading or risk management.* ⚠️
