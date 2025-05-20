# Options Greeks – 2D & 3D Visualizer Suite

A collection of Python scripts that graphically explore the core sensitivities (Greeks) of European options using both 2D and 3D plots. These tools are designed to build deep visual intuition around Delta, Gamma, Theta, Vega, and Rho — across different market scenarios.

---

## 🔍 Overview

This suite provides a visual breakdown of how each Greek behaves with respect to:
- Underlying stock price
- Time to maturity
- Volatility

The 2D versions explore cross-sectional relationships (e.g. Greek vs Stock Price), while the 3D versions render surface plots to reveal richer sensitivities across two variables simultaneously.

Each script is self-contained and focuses on a single Greek, making it ideal for both educational use and deeper quantitative exploration.

---

## Included Visualizers

### Delta
- `Delta_2D.py`: Delta for calls and puts across stock prices, for different volatilities
- `Delta_3D.py`: Delta surfaces vs stock price and time to maturity

### Gamma
- `Gamma_2D.py`: Gamma across stock prices at different volatilities
- `Gamma_3D.py`: Gamma surface vs stock price and time to maturity

### Theta
- `Theta_2D.py`: Theta decay for calls and puts across stock prices and volatilities

### Vega
- `Vega_2D.py`: Vega curve for different volatilities vs stock prices
- `Vega_3D.py`: Vega surface over stock price and time to maturity

### Rho
- `Rho_3D.py`: Rho surface for both call and put options vs time and stock price

---

## 📘 Concepts Covered

Each script is based on the analytical Greeks from the Black-Scholes model and reflects:

- ✅ Moneyness impact (Stock price vs Strike)
- ✅ Volatility sensitivity
- ✅ Time decay behavior
- ✅ Surface-level interdependencies between Greeks and pricing variables
- ✅ Dividend-adjusted models (where applicable)

---

*This project is for educational and research purposes only. The visualisations are based on theoretical models and should not be used for live trading decisions.* ⚠️

