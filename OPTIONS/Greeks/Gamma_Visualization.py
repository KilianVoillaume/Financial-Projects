import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def calculate_gamma(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    return gamma


K = 100  
T = 0.5  
r = 0.05  
sigma = 0.2 
volatilities = [0.1, 0.2, 0.3, 0.4, 0.5]  
stock_prices = np.linspace(50, 150, 100)  

fig, axs = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(wspace=0.3)

# Gamma vs Stock Prices (single volatility)
axs[0].set_title('Option Gamma vs Stock Prices')
axs[0].set_xlabel('Stock Price ($)')
axs[0].set_ylabel('Gamma (Γ)')
axs[0].grid(True)

gamma_values = [calculate_gamma(S, K, T, r, sigma) for S in stock_prices]
axs[0].plot(stock_prices, gamma_values, 'b-')
axs[0].set_ylim(0, max(gamma_values) * 1.1)

# Gamma vs Stock Prices (different volatilities)
axs[1].set_title('Option Gamma vs Stock Prices for Different Volatilities')
axs[1].set_xlabel('Stock Price ($)')
axs[1].set_ylabel('Gamma (Γ)')
axs[1].grid(True)

for vol in volatilities:
    gamma_values = [calculate_gamma(S, K, T, r, vol) for S in stock_prices]
    axs[1].plot(stock_prices, gamma_values, label=f'Vol: {int(vol*100)}%')
axs[1].legend()
axs[1].set_ylim(0, 0.1)  

plt.tight_layout()
plt.show()

