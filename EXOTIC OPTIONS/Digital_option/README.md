# Digital vs Vanilla Options – Pricing & Delta Behavior

This Python toolkit explores the fundamental characteristics of **digital (binary) call options** compared to traditional **vanilla calls**, focusing on payoff profiles, delta behavior, and hedging challenges.

---

## 🔍 Overview

Digital options offer fixed payouts if the underlying finishes in the money, making their pricing and risk profile quite different from vanilla calls. These scripts help illustrate:

- The sharp delta behavior of digital options near expiry
- The hedging instability as maturity approaches
- Payoff and break-even comparisons between digital and vanilla calls

---

## 📘 Scripts Included

- **Dayoff_digital_vanilla.py**  
  Compares net payoffs of a digital call and a vanilla call across a range of spot prices, with clear illustrations of premium, fixed payoff, and break-even points.

- **Delta_vs_spot_price.py**  
  Visualises the extreme sensitivity of digital option delta near the strike and simulates the instability in delta hedging as time to maturity shrinks, showcasing why digital options can be difficult to manage dynamically.

---

## 🎯 Key Learning Objectives

- Understand the non-linear payoff structure of digital calls  
- Explore how digital delta spikes near the strike  
- Observe the hedging nightmare caused by near-zero time to expiry  
- Contrast price sensitivity (delta) between digital and vanilla contracts  

---

*These tools are meant for educational exploration and do not constitute trading models or financial advice.* ⚠️
