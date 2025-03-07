# Options Greeks Visualizer
## Description
The Options Greeks Visualizer is an interactive web application built with Streamlit that helps traders and finance professionals visualize how option Greeks (Delta, Gamma, Theta, Vega, and Rho) change based on various input parameters. This tool provides a comprehensive view of option pricing dynamics using the Black-Scholes model with dividend adjustments.

## Features
Real-time calculation of option prices and Greeks for both call and put options
Interactive sliders to adjust key parameters:
- Stock Price
- Strike Price
- Time to Expiration
- Risk-Free Interest Rate
- Dividend Yield
- Volatility

Customizable visualization of how option Greeks change for any selected parameter
Side-by-side comparison of call and put option behaviors
Educational explanations of each Greek and dividend effects on options
Vertical display format for clearer comparison of call vs put option metrics

# Installation and Usage
## Setup 
```bash
# Clone the repository
git clone https://github.com/yourusername/options-greeks-visualizer.git
cd options-greeks-visualizer

# Install required packages
pip install streamlit numpy pandas matplotlib scipy
```

## Launch the app
```bash
streamlit run app.py
```
