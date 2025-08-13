import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd

st.set_page_config(page_title="Professional Options Analyzer", layout="wide")

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

def calculate_greeks(option_type, S, K, T, r, sigma):
    """Calculate all the Greeks"""
    d1 = calculate_d1(S, K, T, r, sigma)
    d2 = calculate_d2(d1, sigma, T)
    
    # Delta
    if option_type == "Call":
        delta = stats.norm.cdf(d1)
    else:
        delta = stats.norm.cdf(d1) - 1
    
    # Gamma (same for calls and puts)
    gamma = stats.norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    # Theta
    if option_type == "Call":
        theta = (-(S * stats.norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - 
                r * K * np.exp(-r * T) * stats.norm.cdf(d2)) / 365
    else:
        theta = (-(S * stats.norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + 
                r * K * np.exp(-r * T) * stats.norm.cdf(-d2)) / 365
    
    # Vega (same for calls and puts)
    vega = S * stats.norm.pdf(d1) * np.sqrt(T) / 100
    
    # Rho
    if option_type == "Call":
        rho = K * T * np.exp(-r * T) * stats.norm.cdf(d2) / 100
    else:
        rho = -K * T * np.exp(-r * T) * stats.norm.cdf(-d2) / 100
    
    return delta, gamma, theta, vega, rho

def get_moneyness(S, K):
    """Determine if option is ITM, ATM, or OTM"""
    ratio = S / K
    if 0.98 <= ratio <= 1.02:
        return "ATM", "orange"
    elif ratio > 1.02:
        return "ITM", "green"
    else:
        return "OTM", "red"

def calculate_intrinsic_value(option_type, S, K):
    """Calculate intrinsic value"""
    if option_type == "Call":
        return max(0, S - K)
    else:
        return max(0, K - S)

st.title("🎯 Professional Options Analyzer")
st.markdown("""
**Comprehensive Black-Scholes analysis with Greeks, risk metrics, and sensitivity visualization**
""")

# Sidebar with enhanced inputs
st.sidebar.markdown(
    """
    <div style='margin-bottom: 25px; padding: 15px; background-color: #f0f2f6; border-radius: 10px;'>
        <span style='font-weight: bold; font-size: 18px;'>Created by:</span><br>
        <a href='https://www.linkedin.com/in/kilian-voillaume-880a9217a/' target='_blank' style='text-decoration: none; display: flex; align-items: center; gap: 12px; margin-top: 8px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='32' height='32'/>
            <span style='color: #0A66C2; font-size: 18px; font-weight: bold;'>Kilian Voillaume</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("📊 Option Parameters")

# Preset scenarios
preset = st.sidebar.selectbox("Choose Scenario:", 
    ["Custom", "At-The-Money", "Deep ITM Call", "Deep OTM Call", "High Volatility", "Near Expiration"])

# Default values
default_S, default_K, default_T, default_r, default_sigma = 100.0, 100.0, 1.0, 5.0, 20.0

# Apply presets
if preset == "At-The-Money":
    default_S, default_K, default_T, default_r, default_sigma = 100.0, 100.0, 0.25, 5.0, 20.0
elif preset == "Deep ITM Call":
    default_S, default_K, default_T, default_r, default_sigma = 120.0, 100.0, 0.5, 5.0, 25.0
elif preset == "Deep OTM Call":
    default_S, default_K, default_T, default_r, default_sigma = 90.0, 110.0, 0.25, 5.0, 30.0
elif preset == "High Volatility":
    default_S, default_K, default_T, default_r, default_sigma = 100.0, 100.0, 1.0, 5.0, 50.0
elif preset == "Near Expiration":
    default_S, default_K, default_T, default_r, default_sigma = 105.0, 100.0, 0.027, 5.0, 25.0  # ~10 days

option_type = st.sidebar.selectbox("Option Type", ["Call", "Put"], help="Choose between Call or Put option")

S = st.sidebar.slider("Stock Price ($)", 50.0, 200.0, default_S, 0.5, 
                     help="Current price of the underlying asset")
K = st.sidebar.slider("Strike Price ($)", 50.0, 200.0, default_K, 0.5,
                     help="Exercise price of the option")
T = st.sidebar.slider("Time to Expiration (Years)", 0.01, 5.0, default_T, 0.01,
                     help="Time remaining until option expiration")
r = st.sidebar.slider("Risk-Free Interest Rate (%)", 0.0, 15.0, default_r, 0.25,
                     help="Current risk-free interest rate") / 100
sigma = st.sidebar.slider("Volatility (%)", 5.0, 100.0, default_sigma, 1.0,
                         help="Implied volatility of the underlying asset") / 100

# Calculate current metrics
current_price = black_scholes_price(option_type, S, K, T, r, sigma)
delta, gamma, theta, vega, rho = calculate_greeks(option_type, S, K, T, r, sigma)
intrinsic_value = calculate_intrinsic_value(option_type, S, K)
time_value = current_price - intrinsic_value
moneyness, moneyness_color = get_moneyness(S, K)

# Main dashboard
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Option Price", f"${current_price:.3f}")
    st.metric("⚡ Intrinsic Value", f"${intrinsic_value:.3f}")

with col2:
    st.metric("⏰ Time Value", f"${time_value:.3f}")
    st.metric("🎯 Moneyness", moneyness)

with col3:
    st.metric("📈 Delta", f"{delta:.4f}")
    st.metric("⚙️ Gamma", f"{gamma:.6f}")

with col4:
    st.metric("📉 Theta", f"{theta:.4f}")
    st.metric("🌊 Vega", f"{vega:.4f}")

# Enhanced visualization section with uniform 2x3 layout
st.header("📊 Comprehensive Analysis")

# Create a single figure with 2x3 subplot layout
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.patch.set_facecolor('white')

# Define custom colors
colors = {
    'price': '#1f77b4',
    'current': '#2ca02c', 
    'strike': '#d62728',
    'zero': '#808080'
}

# Define parameters for sensitivity analysis
parameters = [
    {
        'name': 'Stock Price',
        'range': np.linspace(max(20, S-50), S+50, 150),
        'current': S,
        'xlabel': 'Stock Price ($)',
        'param': 'S',
        'pos': (0, 0)
    },
    {
        'name': 'Strike Price', 
        'range': np.linspace(max(20, K-50), K+50, 150),
        'current': K,
        'xlabel': 'Strike Price ($)',
        'param': 'K',
        'pos': (0, 1)
    },
    {
        'name': 'Time to Expiration',
        'range': np.linspace(1, 365, 150),
        'current': T * 365,
        'xlabel': 'Days to Expiration',
        'param': 'T',
        'pos': (0, 2)
    },
    {
        'name': 'Interest Rate',
        'range': np.linspace(0, 15, 150),
        'current': r * 100,
        'xlabel': 'Interest Rate (%)',
        'param': 'r',
        'pos': (1, 0)
    },
    {
        'name': 'Volatility',
        'range': np.linspace(5, 100, 150),
        'current': sigma * 100,
        'xlabel': 'Volatility (%)',
        'param': 'sigma',
        'pos': (1, 1)
    }
]

# Plot sensitivity analysis for first 5 parameters
for param_info in parameters:
    row, col = param_info['pos']
    ax = axes[row, col]
    param_range = param_info['range']
    
    price_values = []
    
    for param_value in param_range:
        if param_info['param'] == 'S':
            price = black_scholes_price(option_type, param_value, K, T, r, sigma)
        elif param_info['param'] == 'K':
            price = black_scholes_price(option_type, S, param_value, T, r, sigma)
        elif param_info['param'] == 'T':
            if param_value/365 > 0.001:  # Avoid division by zero
                price = black_scholes_price(option_type, S, K, param_value/365, r, sigma)
            else:
                price = intrinsic_value
        elif param_info['param'] == 'r':
            price = black_scholes_price(option_type, S, K, T, param_value/100, sigma)
        elif param_info['param'] == 'sigma':
            if param_value/100 > 0.001:  # Avoid division by zero
                price = black_scholes_price(option_type, S, K, T, r, param_value/100)
            else:
                price = intrinsic_value
        
        price_values.append(price)
    
    # Plot option price
    ax.plot(param_range, price_values, color=colors['price'], linewidth=2.5, 
            label="Option Price", alpha=0.9)
    
    # Add intrinsic value line for stock price chart
    if param_info['param'] == 'S':
        intrinsic_values = [max(0, (x - K) if option_type == "Call" else (K - x)) 
                          for x in param_range]
        ax.plot(param_range, intrinsic_values, '--', color='purple', alpha=0.6, 
                linewidth=1.5, label="Intrinsic Value")
    
    # Styling
    ax.set_xlabel(param_info['xlabel'], fontsize=11, fontweight='bold')
    ax.set_ylabel("Price ($)", fontsize=11, fontweight='bold')
    ax.set_title(f"Effect of {param_info['name']}", fontsize=12, fontweight='bold', pad=10)
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Current value line
    ax.axvline(x=param_info['current'], color=colors['current'], linestyle=':', 
               alpha=0.8, linewidth=2.5, label=f"Current")
    
    # Strike price reference (for stock price chart)
    if param_info['param'] == 'S':
        ax.axvline(x=K, color=colors['strike'], linestyle='--', alpha=0.6, 
                   linewidth=2, label="Strike Price")
    
    # Zero line
    ax.axhline(y=0, color=colors['zero'], linestyle='-', alpha=0.3, linewidth=1)
    
    # Legend
    ax.legend(fontsize=9, loc='best', framealpha=0.9)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Greeks visualization in the 6th position (bottom right)
ax_greeks = axes[1, 2]

greeks_names = ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho']
greeks_values = [delta, gamma, theta, vega, rho]
colors_greeks = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

bars = ax_greeks.bar(greeks_names, greeks_values, color=colors_greeks, alpha=0.7, 
                     edgecolor='black', linewidth=1)
ax_greeks.set_title('Current Greeks Values', fontsize=12, fontweight='bold', pad=10)
ax_greeks.set_ylabel('Greek Value', fontsize=11, fontweight='bold')
ax_greeks.grid(True, alpha=0.3, axis='y')
ax_greeks.spines['top'].set_visible(False)
ax_greeks.spines['right'].set_visible(False)

# Add value labels on bars
for bar, value in zip(bars, greeks_values):
    height = bar.get_height()
    ax_greeks.text(bar.get_x() + bar.get_width()/2., height + (0.01 if height >= 0 else -0.01),
                   f'{value:.4f}', ha='center', va='bottom' if height >= 0 else 'top', 
                   fontweight='bold', fontsize=9)

# Rotate x-axis labels for better readability
ax_greeks.tick_params(axis='x', rotation=45)

# Overall title for the entire figure
fig.suptitle(f'{option_type} Option Analysis - {moneyness} (S=${S:.1f}, K=${K:.1f})', 
              fontsize=16, fontweight='bold', y=0.98)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to accommodate suptitle
st.pyplot(fig)

# Risk Analysis Section
st.header("⚠️ Risk Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Position Risk Metrics")
    
    # Calculate additional risk metrics
    max_loss = current_price if option_type == "Call" else float('inf')
    max_profit = float('inf') if option_type == "Call" else K - current_price
    
    if option_type == "Call":
        break_even = K + current_price
        st.metric("Break-even Price", f"${break_even:.2f}")
        st.metric("Maximum Loss", f"${max_loss:.2f}")
        st.metric("Maximum Profit", "Unlimited")
    else:
        break_even = K - current_price  
        st.metric("Break-even Price", f"${break_even:.2f}")
        st.metric("Maximum Loss", f"${current_price:.2f}")
        st.metric("Maximum Profit", f"${max_profit:.2f}" if max_profit != float('inf') else "N/A")

with col2:
    st.subheader("📈 Sensitivity Rankings")
    
    # Calculate sensitivity scores (normalized)
    sensitivities = {
        'Stock Price (Delta)': abs(delta),
        'Volatility (Vega)': abs(vega) / 10,  # Normalize per 10% vol change
        'Time (Theta)': abs(theta) * 30,      # Normalize per month
        'Interest Rate (Rho)': abs(rho),      # Per 1% rate change
    }
    
    sorted_sensitivities = sorted(sensitivities.items(), key=lambda x: x[1], reverse=True)
    
    for i, (factor, sensitivity) in enumerate(sorted_sensitivities):
        rank_emoji = ["🥇", "🥈", "🥉", "4️⃣"][i]
        st.metric(f"{rank_emoji} {factor}", f"{sensitivity:.4f}")

# Educational section
with st.expander("🎓 Trading Strategies & Insights", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 When to Buy This Option:**
        - High Delta: Directional plays
        - High Vega: Volatility expansion expected
        - Low Theta: Limited time decay
        
        **🎯 Optimal Conditions:**
        - Calls: Bullish outlook + low volatility
        - Puts: Bearish outlook + low volatility
        """)
    
    with col2:
        st.markdown("""
        **⚠️ Risk Factors:**
        - High Theta: Time decay risk
        - High Vega: Volatility crush risk
        - Low Delta: Limited directional exposure
        
        **💡 Pro Tips:**
        - ATM options have highest Gamma
        - ITM options have higher Delta
        - Time decay accelerates near expiration
        """)

st.info("💡 **Pro Tip:** Use the parameter sliders to see real-time changes across all metrics. The green dotted lines show your current settings!")

# Footer
st.markdown("---")
st.markdown("*This tool is for educational purposes only. Always consult with a financial advisor before making investment decisions.*")
