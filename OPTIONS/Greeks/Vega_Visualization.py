import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def calculate_vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100  # Divided by 100 for 1% change
    return vega

K = 100 
T_values = [0.25, 0.5, 1.0]  # Time to expiration (3 months, 6 months, 1 year)
r = 0.05  
sigma = 0.2  
volatilities = [0.1, 0.2, 0.3, 0.4, 0.5] 
stock_prices = np.linspace(50, 150, 100)  

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
plt.subplots_adjust(hspace=0.3, wspace=0.3)

# Vega vs Stock Prices (single volatility)
axs[0, 0].set_title('Option Vega vs Stock Prices')
axs[0, 0].set_xlabel('Stock Price ($)')
axs[0, 0].set_ylabel('Vega (ν) for 1% change in volatility')
axs[0, 0].grid(True)

vega_values = [calculate_vega(S, K, T_values[1], r, sigma) for S in stock_prices]
axs[0, 0].plot(stock_prices, vega_values, 'b-')
axs[0, 0].set_ylim(0, max(vega_values) * 1.1)

# Vega vs Stock Prices (different volatilities)
axs[0, 1].set_title('Option Vega vs Stock Prices for Different Volatilities')
axs[0, 1].set_xlabel('Stock Price ($)')
axs[0, 1].set_ylabel('Vega (ν) for 1% change in volatility')
axs[0, 1].grid(True)

for vol in volatilities:
    vega_values = [calculate_vega(S, K, T_values[1], r, vol) for S in stock_prices]
    axs[0, 1].plot(stock_prices, vega_values, label=f'Vol: {int(vol*100)}%')
axs[0, 1].legend()

# Vega vs Stock Prices (different time to expiration)
axs[1, 0].set_title('Option Vega vs Stock Prices for Different Expirations')
axs[1, 0].set_xlabel('Stock Price ($)')
axs[1, 0].set_ylabel('Vega (ν) for 1% change in volatility')
axs[1, 0].grid(True)

for T in T_values:
    vega_values = [calculate_vega(S, K, T, r, sigma) for S in stock_prices]
    axs[1, 0].plot(stock_prices, vega_values, label=f'T: {int(T*12)} months')
axs[1, 0].legend()

# Vega vs Time to Expiration
T_range = np.linspace(0.1, 2, 100)  # Time to expiration from 1.2 months to 2 years
prices_to_plot = [80, 100, 120]  # OTM, ATM, ITM

axs[1, 1].set_title('Option Vega vs Time to Expiration')
axs[1, 1].set_xlabel('Time to Expiration (years)')
axs[1, 1].set_ylabel('Vega (ν) for 1% change in volatility')
axs[1, 1].grid(True)

for price in prices_to_plot:
    vega_values = [calculate_vega(price, K, t, r, sigma) for t in T_range]
    axs[1, 1].plot(T_range, vega_values, label=f'S=${price}')
axs[1, 1].legend()

plt.tight_layout()
plt.show()


