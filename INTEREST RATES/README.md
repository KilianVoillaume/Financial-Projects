# 🧾 Interest Rate Models & Term Structure Analysis

A set of Python tools designed to simulate, calibrate, and visualise interest rate dynamics and forward rate term structures using models like Vasicek, CIR, Hull-White, HJM, and LMM.

---

## 🔍 Model Descriptions

- **Short_rate_model_comparisons.py**  
  Simulates and compares three foundational short-rate models — Vasicek, CIR, and Hull-White — by visualising their dynamics, volatility, and long-term behaviour under common assumptions.

- **Term_structure_evolution_HJM.py**  
  Implements the Heath–Jarrow–Morton (HJM) framework to simulate the evolution of the forward rate curve under different volatility structures (constant, humped, two-factor) with rich 3D and animated visualisations.

- **LMM_forward_rate_vol_surface.py**  
  Calibrates a parametric Libor Market Model (LMM) to synthetic caplet volatility surfaces, producing both 3D surface plots and smile diagnostics across maturities and strikes.

---

*These models are intended for educational and research use only. They rely on stylized assumptions and are not suited for real-time trading or financial forecasting.* ⚠️
