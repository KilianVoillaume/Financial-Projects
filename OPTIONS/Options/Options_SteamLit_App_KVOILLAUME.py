import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.set_page_config(page_title="Options Price Visualizer", layout="wide")

def calculate_d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def calculate_d2(d1, sigma, T):
    return d1 - sigma * np.sqrt(T)

def black_scholes_price(option_type, S, K, T, r, sigma):
    d1 = calculate_d1(S, K, T, r, sigma)
    d2 = calculate_d2(d1, sigma, T)
    
    if option_type == "Call":
        price = S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    else:  # Put
        price = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
    
    return price

st.title("Options Price Visualizer")
st.markdown("""
This app visualizes how the Black-Scholes option price changes based on various input parameters:
- Stock price
- Strike price
- Time to expiration
- Interest rate
- Volatility
""")

st.sidebar.markdown(
    """
    <div style='margin-bottom: 25px;'>
        <span style='font-weight: bold; font-size: 18px;'>Created by:</span><br>
        <a href='https://www.linkedin.com/in/kilian-voillaume-880a9217a/' target='_blank' style='text-decoration: none; display: flex; align-items: center; gap: 12px; margin-top: 8px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='32' height='32'/>
            <span style='color: #0A66C2; font-size: 18px; font-weight: bold;'>Kilian Voillaume</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar inputs
st.sidebar.header("Input Parameters")
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])

S = st.sidebar.slider("Stock Price ($)", 50.0, 150.0, 100.0, 1.0)
K = st.sidebar.slider("Strike Price ($)", 50.0, 150.0, 100.0, 1.0)
T = st.sidebar.slider("Time to Expiration (Years)", 0.01, 10.0, 1.0, 0.01)
r = st.sidebar.slider("Risk-Free Interest Rate (%)", 0.0, 10.0, 5.0, 0.25) / 100
sigma = st.sidebar.slider("Volatility (%)", 5.0, 100.0, 20.0, 1.0) / 100

current_price = black_scholes_price(option_type, S, K, T, r, sigma)

st.header("Current Option Price")
st.metric("Option Price", f"${current_price:.2f}")

# Visualization section
st.header("Option Price Visualization")

param_to_visualize = st.selectbox(
    "Select Parameter to Visualize Against", 
    ["Stock Price", "Strike Price", "Time to Expiration", "Interest Rate", "Volatility"]
)

# Set up the range for the selected parameter
if param_to_visualize == "Stock Price":
    param_range = np.linspace(50, 150, 100)
    param_values = param_range
    x_label = "Stock Price ($)"
    variable_param = "S"
    fixed_params = (K, T, r, sigma)
    
elif param_to_visualize == "Strike Price":
    param_range = np.linspace(50, 150, 100)
    param_values = param_range
    x_label = "Strike Price ($)"
    variable_param = "K"
    fixed_params = (S, T, r, sigma)
    
elif param_to_visualize == "Time to Expiration":
    param_range = np.linspace(1, 365, 100)
    param_values = param_range / 365  # Convert to years
    x_label = "Time to Expiration (Days)"
    variable_param = "T"
    fixed_params = (S, K, r, sigma)
    
elif param_to_visualize == "Interest Rate":
    param_range = np.linspace(0, 10, 100)
    param_values = param_range / 100  # Convert to decimal
    x_label = "Interest Rate (%)"
    variable_param = "r"
    fixed_params = (S, K, T, sigma)
    
else:  # Volatility
    param_range = np.linspace(5, 100, 100)
    param_values = param_range / 100  # Convert to decimal
    x_label = "Volatility (%)"
    variable_param = "sigma"
    fixed_params = (S, K, T, r)

price_values = []
for param_value in param_values:
    if variable_param == "S":
        price = black_scholes_price(option_type, param_value, K, T, r, sigma)
    elif variable_param == "K":
        price = black_scholes_price(option_type, S, param_value, T, r, sigma)
    elif variable_param == "T":
        price = black_scholes_price(option_type, S, K, param_value, r, sigma)
    elif variable_param == "r":
        price = black_scholes_price(option_type, S, K, T, param_value, sigma)
    else:  # sigma
        price = black_scholes_price(option_type, S, K, T, r, param_value)
    
    price_values.append(price)
    
# Mark the current parameter value with a vertical line
if param_to_visualize == "Stock Price":
    current_value = S
elif param_to_visualize == "Strike Price":
    current_value = K
elif param_to_visualize == "Time to Expiration":
    current_value = T * 365  # Convert back to days for display
elif param_to_visualize == "Interest Rate":
    current_value = r * 100  # Convert back to percentage for display
else:  # Volatility
    current_value = sigma * 100  # Convert back to percentage for display

fig, ax = plt.subplots(figsize=(6, 3))  # Reduced height
ax.plot(param_range, price_values, label="Option Price", color='blue')
ax.set_xlabel(x_label)
ax.set_ylabel("Option Price ($)")
ax.set_title(f"{option_type} Option: Effect of {param_to_visualize}", fontsize=10)
ax.legend()
ax.grid(True)
ax.axvline(x=current_value, color='r', linestyle='--', alpha=0.5)
st.pyplot(fig)

# Add a container with a custom height to limit the vertical space
st.header("Understanding Option Price", anchor=False)
st.markdown("""
The Black-Scholes model calculates the theoretical price of an option using various parameters:
- **Stock Price (S):** Higher stock price increases the value of call options and decreases the value of put options.
- **Strike Price (K):** Higher strike price decreases call option value and increases put option value.
- **Time to Expiration (T):** More time to expiration generally increases the option price due to increased uncertainty.
- **Interest Rate (r):** Higher interest rates increase the value of call options and decrease the value of put options.
- **Volatility (σ):** Higher volatility increases both call and put option prices, as larger price swings increase the probability of the option finishing in the money.
""")
