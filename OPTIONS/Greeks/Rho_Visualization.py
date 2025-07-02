import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def calculate_rho(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100  # Divided by 100 for 1% change
    else:  # put
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100  # Divided by 100 for 1% change
    
    return rho

K = 100  
T_values = [0.25, 0.5, 1.0, 2.0]  # Time to expiration (3m, 6m, 1y, 2y)
r = 0.05  
sigma = 0.2  
stock_prices = np.linspace(50, 150, 100)  

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
plt.subplots_adjust(hspace=0.3, wspace=0.3)

# Rho Call vs Stock Prices
axs[0, 0].set_title('Rho Call vs Stock Prices')
axs[0, 0].set_xlabel('Stock Price ($)')
axs[0, 0].set_ylabel('Rho (ρ) for 1% change in interest rate')
axs[0, 0].grid(True)

call_rho = [calculate_rho(S, K, T_values[1], r, sigma, 'call') for S in stock_prices]
axs[0, 0].plot(stock_prices, call_rho, 'b-')
axs[0, 0].set_ylim(0, max(call_rho) * 1.1)

# Rho Put vs Stock Prices
axs[0, 1].set_title('Rho Put vs Stock Prices')
axs[0, 1].set_xlabel('Stock Price ($)')
axs[0, 1].set_ylabel('Rho (ρ) for 1% change in interest rate')
axs[0, 1].grid(True)

put_rho = [calculate_rho(S, K, T_values[1], r, sigma, 'put') for S in stock_prices]
axs[0, 1].plot(stock_prices, put_rho, 'b-')
axs[0, 1].set_ylim(min(put_rho) * 1.1, 0)

# Rho Call vs Stock Prices for Different Time to Expiration
axs[1, 0].set_title('Rho Call vs Stock Prices for Different Expirations')
axs[1, 0].set_xlabel('Stock Price ($)')
axs[1, 0].set_ylabel('Rho (ρ) for 1% change in interest rate')
axs[1, 0].grid(True)

for T in T_values:
    call_rho = [calculate_rho(S, K, T, r, sigma, 'call') for S in stock_prices]
    axs[1, 0].plot(stock_prices, call_rho, label=f'T: {int(T*12)} months')
axs[1, 0].legend()

# Rho Put vs Stock Prices for Different Time to Expiration
axs[1, 1].set_title('Rho Put vs Stock Prices for Different Expirations')
axs[1, 1].set_xlabel('Stock Price ($)')
axs[1, 1].set_ylabel('Rho (ρ) for 1% change in interest rate')
axs[1, 1].grid(True)

for T in T_values:
    put_rho = [calculate_rho(S, K, T, r, sigma, 'put') for S in stock_prices]
    axs[1, 1].plot(stock_prices, put_rho, label=f'T: {int(T*12)} months')
axs[1, 1].legend()

plt.tight_layout()
plt.show()

