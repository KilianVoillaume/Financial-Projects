# Sidebar inputs - keep these as they were
st.sidebar.header("Input Parameters")
option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"])

S = st.sidebar.slider("Stock Price ($)", 50.0, 150.0, 100.0, 1.0)
K = st.sidebar.slider("Strike Price ($)", 50.0, 150.0, 100.0, 1.0)
T = st.sidebar.slider("Time to Expiration (Years)", 0.01, 10.0, 1.0, 0.01)
r = st.sidebar.slider("Risk-Free Interest Rate (%)", 0.0, 10.0, 5.0, 0.25) / 100
sigma = st.sidebar.slider("Volatility (%)", 5.0, 100.0, 20.0, 1.0) / 100

current_price = black_scholes_price(option_type, S, K, T, r, sigma)import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

st.set_page_config(page_title="Options Price Visualizer", layout="wide")

# CSS to reduce spacing
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    h1, h2, h3 {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .stMetric {
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

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

st.title("Options Price Visualizer", anchor=False)

curr_price_col1, curr_price_col2 = st.columns([2, 3])
with curr_price_col1:
    st.metric("Current Option Price", f"${current_price:.2f}")

# Visualization section
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Visualization Options")
    param_to_visualize = st.selectbox(
        "Select Parameter", 
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
    params = {
        "S": fixed_params[0],
        "K": fixed_params[1],
        "T": fixed_params[2],
        "r": fixed_params[3],
        "sigma": fixed_params[4] if variable_param != "sigma" else param_value
    }
    
    if variable_param == "S":
        S_val = param_value
        price = black_scholes_price(option_type, S_val, K, T, r, sigma)
    elif variable_param == "K":
        K_val = param_value
        price = black_scholes_price(option_type, S, K_val, T, r, sigma)
    elif variable_param == "T":
        T_val = param_value
        price = black_scholes_price(option_type, S, K, T_val, r, sigma)
    elif variable_param == "r":
        r_val = param_value
        price = black_scholes_price(option_type, S, K, T, r_val, sigma)
    else:  # sigma
        sigma_val = param_value
        price = black_scholes_price(option_type, S, K, T, r, sigma_val)
    
    price_values.append(price)

with col2:
    # Create a smaller figure with adjusted figsize
    fig, ax = plt.subplots(figsize=(6, 3))  # Reduced height even more
    ax.plot(param_range, price_values, label="Option Price", color='blue')
    ax.set_xlabel(x_label)
    ax.set_ylabel("Option Price ($)")
    ax.set_title(f"{option_type} Option: Effect of {param_to_visualize}", fontsize=10)
    ax.legend()
    ax.grid(True)

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

    ax.axvline(x=current_value, color='r', linestyle='--', alpha=0.5)

    # Use a height parameter to control the overall container size
    st.pyplot(fig, use_container_width=True)

# Add a container with a custom height to limit the vertical space
st.header("Understanding Option Price", anchor=False)
with st.container():
    st.markdown("""
    <div style="font-size: 0.9em;">
    <p>The Black-Scholes model calculates the theoretical price of an option using various parameters:</p>
    <ul>
    <li><strong>Stock Price (S):</strong> Higher stock price increases call option value and decreases put option value.</li>
    <li><strong>Strike Price (K):</strong> Higher strike price decreases call option value and increases put option value.</li>
    <li><strong>Time to Expiration (T):</strong> More time generally increases option prices due to increased uncertainty.</li>
    <li><strong>Interest Rate (r):</strong> Higher rates increase call option value and decrease put option value.</li>
    <li><strong>Volatility (σ):</strong> Higher volatility increases both call and put option prices.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
