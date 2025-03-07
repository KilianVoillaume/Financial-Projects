import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

st.set_page_config(page_title="Options Greeks Visualizer", layout="wide")

#++++++++++++++++++++++++++++
#+++++ FUNCTION SECTION +++++
#++++++++++++++++++++++++++++
def calculate_d1(S, K, T, r, q, sigma):
    return (np.log(S/K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def calculate_d2(d1, sigma, T):
    return d1 - sigma * np.sqrt(T)

def calculate_greeks(option_type, S, K, T, r, q, sigma):
    d1 = calculate_d1(S, K, T, r, q, sigma)
    d2 = calculate_d2(d1, sigma, T)
    
    if option_type == "Call":
        # Call option formulas with dividends
        delta = np.exp(-q * T) * stats.norm.cdf(d1)
        gamma = np.exp(-q * T) * stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = -((S * sigma * np.exp(-q * T) * stats.norm.pdf(d1)) / (2 * np.sqrt(T))) - \
                (r * K * np.exp(-r * T) * stats.norm.cdf(d2)) + \
                (q * S * np.exp(-q * T) * stats.norm.cdf(d1))
        vega = S * np.exp(-q * T) * np.sqrt(T) * stats.norm.pdf(d1) / 100  # Divided by 100 to get the effect of 1% change
        rho = K * T * np.exp(-r * T) * stats.norm.cdf(d2) / 100  # Divided by 100 to get the effect of 1% change
    else:
        # Put option formulas with dividends
        delta = np.exp(-q * T) * (stats.norm.cdf(d1) - 1)
        gamma = np.exp(-q * T) * stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = -((S * sigma * np.exp(-q * T) * stats.norm.pdf(d1)) / (2 * np.sqrt(T))) + \
                (r * K * np.exp(-r * T) * stats.norm.cdf(-d2)) - \
                (q * S * np.exp(-q * T) * stats.norm.cdf(-d1))
        vega = S * np.exp(-q * T) * np.sqrt(T) * stats.norm.pdf(d1) / 100  # Divided by 100 to get the effect of 1% change
        rho = -K * T * np.exp(-r * T) * stats.norm.cdf(-d2) / 100  # Divided by 100 to get the effect of 1% change
    
    return {
        "Delta": delta,
        "Gamma": gamma,
        "Theta": theta / 365,  # Daily theta
        "Vega": vega,
        "Rho": rho
    }

def black_scholes_price(option_type, S, K, T, r, q, sigma):
    d1 = calculate_d1(S, K, T, r, q, sigma)
    d2 = calculate_d2(d1, sigma, T)
    
    if option_type == "Call":
        price = S * np.exp(-q * T) * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    else:  # Put
        price = K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * np.exp(-q * T) * stats.norm.cdf(-d1)
    
    return price


#+++++++++++++++++++++++
#+++++ APP DISPLAY +++++
#+++++++++++++++++++++++
st.title("Options Greeks Visualizer")
st.markdown("""
This app visualizes how option Greeks (Delta, Gamma, Theta, Vega, and Rho) change 
based on various input parameters like stock price, strike price, time to expiration, 
interest rate, dividend yield, and volatility. The graphs show both Call and Put options side by side.
""")

st.sidebar.header("Input Parameters")
S_default = 100.0  # Make sure this is a float
K_default = 100.0  # Make sure this is a float
T_default = 30/365
r_default = 0.05
q_default = 0.02  # Default dividend yield
sigma_default = 0.2

S = st.sidebar.slider("Stock Price ($)", 50.0, 150.0, float(S_default), 1.0)
K = st.sidebar.slider("Strike Price ($)", 50.0, 150.0, float(K_default), 1.0)
T = st.sidebar.slider("Time to Expiration (Days)", 1, 365, int(T_default * 365), 1) / 365
r = st.sidebar.slider("Risk-Free Interest Rate (%)", 0.0, 10.0, float(r_default * 100), 0.25) / 100
q = st.sidebar.slider("Dividend Yield (%)", 0.0, 10.0, float(q_default * 100), 0.25) / 100
sigma = st.sidebar.slider("Volatility (%)", 5.0, 100.0, float(sigma_default * 100), 1.0) / 100

# Calculate current option prices and greeks for both Call and Put
call_price = black_scholes_price("Call", S, K, T, r, q, sigma)
put_price = black_scholes_price("Put", S, K, T, r, q, sigma)
call_greeks = calculate_greeks("Call", S, K, T, r, q, sigma)
put_greeks = calculate_greeks("Put", S, K, T, r, q, sigma)

st.header("Current Option Values")
st.subheader("Call Option")
call_metrics = st.columns(6)
call_metrics[0].metric("Price", f"${call_price:.2f}")
call_metrics[1].metric("Delta", f"{call_greeks['Delta']:.4f}")
call_metrics[2].metric("Gamma", f"{call_greeks['Gamma']:.4f}")
call_metrics[3].metric("Theta", f"${call_greeks['Theta']:.4f}/day")
call_metrics[4].metric("Vega", f"${call_greeks['Vega']:.4f}")
call_metrics[5].metric("Rho", f"${call_greeks['Rho']:.4f}")

st.subheader("Put Option")
put_metrics = st.columns(6)
put_metrics[0].metric("Price", f"${put_price:.2f}")
put_metrics[1].metric("Delta", f"{put_greeks['Delta']:.4f}")
put_metrics[2].metric("Gamma", f"{put_greeks['Gamma']:.4f}")
put_metrics[3].metric("Theta", f"${put_greeks['Theta']:.4f}/day")
put_metrics[4].metric("Vega", f"${put_greeks['Vega']:.4f}")
put_metrics[5].metric("Rho", f"${put_greeks['Rho']:.4f}")

#++++++++++++++++++++++++
#+++++ PLOT SECTION +++++
#++++++++++++++++++++++++
st.header("Greeks Visualization")

# Parameter to visualize against
param_to_visualize = st.selectbox(
    "Select Parameter to Visualize Against", 
    ["Stock Price", "Strike Price", "Time to Expiration", "Interest Rate", "Dividend Yield", "Volatility"]
)

# Set up the range for the selected parameter
if param_to_visualize == "Stock Price":
    param_range = np.linspace(50, 150, 100)
    param_values = param_range
    x_label = "Stock Price ($)"
    
elif param_to_visualize == "Strike Price":
    param_range = np.linspace(50, 150, 100)
    param_values = param_range
    x_label = "Strike Price ($)"
    
elif param_to_visualize == "Time to Expiration":
    param_range = np.linspace(1, 365, 100)
    param_values = param_range / 365  
    x_label = "Time to Expiration (Days)"
    
elif param_to_visualize == "Interest Rate":
    param_range = np.linspace(0, 10, 100)
    param_values = param_range / 100 
    x_label = "Interest Rate (%)"

elif param_to_visualize == "Dividend Yield":
    param_range = np.linspace(0, 10, 100)
    param_values = param_range / 100
    x_label = "Dividend Yield (%)"
    
else:  # Volatility
    param_range = np.linspace(5, 100, 100)
    param_values = param_range / 100 
    x_label = "Volatility (%)"

# Calculate Greeks for each parameter value for both Call and Put
call_delta_values = []
call_gamma_values = []
call_theta_values = []
call_vega_values = []
call_rho_values = []
call_price_values = []

put_delta_values = []
put_gamma_values = []
put_theta_values = []
put_vega_values = []
put_rho_values = []
put_price_values = []

for param_value in param_values:
    if param_to_visualize == "Stock Price":
        call_greeks = calculate_greeks("Call", param_value, K, T, r, q, sigma)
        put_greeks = calculate_greeks("Put", param_value, K, T, r, q, sigma)
        call_price = black_scholes_price("Call", param_value, K, T, r, q, sigma)
        put_price = black_scholes_price("Put", param_value, K, T, r, q, sigma)
    elif param_to_visualize == "Strike Price":
        call_greeks = calculate_greeks("Call", S, param_value, T, r, q, sigma)
        put_greeks = calculate_greeks("Put", S, param_value, T, r, q, sigma)
        call_price = black_scholes_price("Call", S, param_value, T, r, q, sigma)
        put_price = black_scholes_price("Put", S, param_value, T, r, q, sigma)
    elif param_to_visualize == "Time to Expiration":
        # Skip very small T values to avoid division by zero
        if param_value < 0.001:
            continue
        call_greeks = calculate_greeks("Call", S, K, param_value, r, q, sigma)
        put_greeks = calculate_greeks("Put", S, K, param_value, r, q, sigma)
        call_price = black_scholes_price("Call", S, K, param_value, r, q, sigma)
        put_price = black_scholes_price("Put", S, K, param_value, r, q, sigma)
    elif param_to_visualize == "Interest Rate":
        call_greeks = calculate_greeks("Call", S, K, T, param_value, q, sigma)
        put_greeks = calculate_greeks("Put", S, K, T, param_value, q, sigma)
        call_price = black_scholes_price("Call", S, K, T, param_value, q, sigma)
        put_price = black_scholes_price("Put", S, K, T, param_value, q, sigma)
    elif param_to_visualize == "Dividend Yield":
        call_greeks = calculate_greeks("Call", S, K, T, r, param_value, sigma)
        put_greeks = calculate_greeks("Put", S, K, T, r, param_value, sigma)
        call_price = black_scholes_price("Call", S, K, T, r, param_value, sigma)
        put_price = black_scholes_price("Put", S, K, T, r, param_value, sigma)
    else:  # Volatility
        # Skip very small sigma values to avoid division by zero
        if param_value < 0.001:
            continue
        call_greeks = calculate_greeks("Call", S, K, T, r, q, param_value)
        put_greeks = calculate_greeks("Put", S, K, T, r, q, param_value)
        call_price = black_scholes_price("Call", S, K, T, r, q, param_value)
        put_price = black_scholes_price("Put", S, K, T, r, q, param_value)
    
    call_delta_values.append(call_greeks["Delta"])
    call_gamma_values.append(call_greeks["Gamma"])
    call_theta_values.append(call_greeks["Theta"])
    call_vega_values.append(call_greeks["Vega"])
    call_rho_values.append(call_greeks["Rho"])
    call_price_values.append(call_price)
    
    put_delta_values.append(put_greeks["Delta"])
    put_gamma_values.append(put_greeks["Gamma"])
    put_theta_values.append(put_greeks["Theta"])
    put_vega_values.append(put_greeks["Vega"])
    put_rho_values.append(put_greeks["Rho"])
    put_price_values.append(put_price)

greeks_to_show = st.multiselect(
    "Select Greeks to Display", 
    ["Price", "Delta", "Gamma", "Theta", "Vega", "Rho"],
    default=["Delta", "Gamma", "Theta", "Vega", "Rho"]  # All Greeks selected by default
)

if not greeks_to_show:
    st.warning("Please select at least one Greek to display.")
else:
    st.subheader(f"Effect of {param_to_visualize} on Option Greeks")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Custom x-axis values for display
    x_display = param_range
    
    for greek in greeks_to_show:
        if greek == "Price":
            ax1.plot(x_display, call_price_values, label="Price")
        elif greek == "Delta":
            ax1.plot(x_display, call_delta_values, label="Delta")
        elif greek == "Gamma":
            ax1.plot(x_display, call_gamma_values, label="Gamma")
        elif greek == "Theta":
            ax1.plot(x_display, call_theta_values, label="Theta (daily)")
        elif greek == "Vega":
            ax1.plot(x_display, call_vega_values, label="Vega")
        elif greek == "Rho":
            ax1.plot(x_display, call_rho_values, label="Rho")
    
    for greek in greeks_to_show:
        if greek == "Price":
            ax2.plot(x_display, put_price_values, label="Price")
        elif greek == "Delta":
            ax2.plot(x_display, put_delta_values, label="Delta")
        elif greek == "Gamma":
            ax2.plot(x_display, put_gamma_values, label="Gamma")
        elif greek == "Theta":
            ax2.plot(x_display, put_theta_values, label="Theta (daily)")
        elif greek == "Vega":
            ax2.plot(x_display, put_vega_values, label="Vega")
        elif greek == "Rho":
            ax2.plot(x_display, put_rho_values, label="Rho")
    
    ax1.set_title(f"Call Option: Effect of {param_to_visualize}")
    ax2.set_title(f"Put Option: Effect of {param_to_visualize}")
    
    ax1.set_xlabel(x_label)
    ax2.set_xlabel(x_label)
    
    ax1.set_ylabel("Value")
    ax2.set_ylabel("Value")
    
    ax1.legend()
    ax2.legend()
    
    ax1.grid(True)
    ax2.grid(True)
    
    # Add vertical line for current parameter value on both plots
    if param_to_visualize == "Stock Price":
        current_value = S
    elif param_to_visualize == "Strike Price":
        current_value = K
    elif param_to_visualize == "Time to Expiration":
        current_value = T * 365
    elif param_to_visualize == "Interest Rate":
        current_value = r * 100
    elif param_to_visualize == "Dividend Yield":
        current_value = q * 100
    else:  # Volatility
        current_value = sigma * 100
        
    ax1.axvline(x=current_value, color='r', linestyle='--', alpha=0.5)
    ax2.axvline(x=current_value, color='r', linestyle='--', alpha=0.5)
    
    st.pyplot(fig)

with st.expander("Understanding the Greeks (Click to Expand)"):
    st.subheader("Delta")
    st.write("""
    **Delta** measures how much an option's price is expected to change per $1 change in the underlying stock.
    - For call options, delta ranges from 0 to 1
    - For put options, delta ranges from -1 to 0
    - At-the-money options typically have deltas around 0.5 (calls) or -0.5 (puts)
    - Dividends decrease call delta and increase put delta (make it less negative)
    """)
    
    st.subheader("Gamma")
    st.write("""
    **Gamma** measures the rate of change in delta for a $1 change in the underlying stock.
    - High gamma means delta can change rapidly with small movements in the stock
    - Gamma is highest for at-the-money options and decreases as options move deeply in or out of the money
    - Gamma is affected by dividends - higher dividends generally lower gamma slightly
    - Gamma is the same for calls and puts with the same strike and expiration
    """)
    
    st.subheader("Theta")
    st.write("""
    **Theta** measures the rate at which an option loses value due to time decay (per day).
    - Generally negative for both calls and puts (options lose value as time passes)
    - Theta increases (becomes more negative) as expiration approaches
    - At-the-money options typically have the highest theta
    - Dividends typically increase theta for calls (more negative) and decrease theta for puts (less negative)
    """)
    
    st.subheader("Vega")
    st.write("""
    **Vega** measures sensitivity to changes in implied volatility.
    - Higher vega means the option's price is more sensitive to volatility changes
    - Vega is highest for at-the-money options with longer expirations
    - Displayed as the dollar change for a 1% change in volatility
    - Dividends generally reduce vega for all options
    - Vega is the same for calls and puts with the same strike and expiration
    """)
    
    st.subheader("Rho")
    st.write("""
    **Rho** measures sensitivity to changes in interest rates.
    - For call options, rho is positive (calls increase in value as rates rise)
    - For put options, rho is negative (puts decrease in value as rates rise)
    - Displayed as the dollar change for a 1% change in interest rates
    - Rho is more significant for longer-term options
    - Dividends reduce rho for call options and increase rho for put options (make it less negative)
    """)
    
    st.subheader("Dividend Effect on Options")
    st.write("""
    **Dividend Impact:**
    - Higher dividends decrease call option prices and increase put option prices
    - This is because stocks typically drop in price by approximately the dividend amount on the ex-dividend date
    - For American options (not modeled here), high dividends can make early exercise optimal for calls
    - The Black-Scholes model with dividends assumes a continuous dividend yield rather than discrete payments
    """)
