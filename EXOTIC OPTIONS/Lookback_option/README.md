# Lookback Options – Path Dependency & Payoff Simulation

This toolkit explores the unique characteristics of **lookback options**, which allow investors to "look back" at the most favourable price reached during the option's life. These tools help visualise both the **payoff advantage** and **path dependency** that differentiate lookbacks from standard vanilla options.

---

## 📘 Scripts Included

- **Payoff_vanilla_lookback.py**  
  Compares the payoff of a vanilla call versus a lookback call using a single simulated path. Highlights the gain from replacing a fixed strike with the observed minimum, and visualises payoff improvement as a function of strike.

- **MonteCarlo_lookback.py**  
  Simulates multiple asset price paths and tracks the evolving minimum and maximum for each. Visualises how the lookback call and put payoffs are derived based on the final price relative to historical extrema.

---

## 🎯 Educational Objectives

- Understand how **floating strike lookback options** work  
- Compare payoff outcomes to standard vanilla options  
- Observe the evolution of **running max/min** prices and their impact on final payoff  
- Build intuition for the pricing premium due to **path dependency**  

---

*This material is intended for educational and illustrative purposes only. It does not constitute financial advice or a trading recommendation.* ⚠️
