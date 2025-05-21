# Cliquet Options – Monte Carlo Simulation & Return Capping

A Python toolkit for simulating and analysing the payoff mechanics of cliquet-style structured products — which feature locally capped and floored returns, and globally bounded outcomes.

---

## 🔍 Overview

Cliquet options are path-dependent products that accumulate a series of capped/floored returns over multiple reset periods. These tools use Monte Carlo simulation and deterministic path logic to illustrate how cliquet structures behave relative to vanilla instruments — both in final payoff distribution and in cumulative return evolution.

---

## 📘 Scripts Included

- **MonteCarlo_final_distribution_cliquet.py**  
  Simulates and compares the final payoff distributions of vanilla call options and cliquet options using 12-month Monte Carlo paths, showing how local caps/floors and global constraints reshape the distribution and reduce volatility.

- **cumulative_payoff_with_without_floor.py**  
  Tracks a single 5-year asset path with annual resets to visualise the difference between raw returns and capped/floored returns over time, including detailed charts of per-period return truncation and cumulative payoff differences.

---

## 🎯 Key Educational Takeaways

- Understand how caps and floors reshape payoff profiles  
- Visualise the smoothing and risk-limiting effect of cliquet mechanisms  
- See how accumulated payoff distributions compare to vanilla exposure  
- Learn about global vs local constraints in structured product engineering  

---

*This code is for educational and exploratory use only. It does not represent investment advice or pricing models for live financial instruments.* ⚠️
