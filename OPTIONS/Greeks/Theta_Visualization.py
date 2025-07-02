import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def calculate_theta(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    pdf_d1 = norm.pdf(d1)
    
    if option_type == 'call':
        theta = -S * pdf_d1 * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put
        theta = -S * pdf_d1 * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
    
    theta = theta / 365 #Convert to annual
    return theta

K = 100  
T = 0.5  
r = 0.05  
sigma = 0.2  
volatilities = [0.1, 0.2, 0.3, 0.4, 0.5]  
stock_prices = np.linspace(50, 150, 100)  

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
plt.subplots_adjust(hspace=0.3, wspace=0.3)

# Theta Call vs Stock Prices (single volatility)
axs[0, 0].set_title('Theta Call vs Stock Prices')
axs[0, 0].set_xlabel('Stock Price ($)')
axs[0, 0].set_ylabel('Theta (Θ) per day')
axs[0, 0].grid(True)

call_theta = [calculate_theta(S, K, T, r, sigma, 'call') for S in stock_prices]
axs[0, 0].plot(stock_prices, call_theta, 'b-')
axs[0, 0].set_ylim(min(call_theta) * 1.1, max(0, max(call_theta)) * 1.1)

# Theta Call vs Stock Prices (different volatilities)
axs[0, 1].set_title('Theta Call vs Stock Prices for Different Volatilities')
axs[0, 1].set_xlabel('Stock Price ($)')
axs[0, 1].set_ylabel('Theta (Θ) per day')
axs[0, 1].grid(True)

for vol in volatilities:
    call_theta = [calculate_theta(S, K, T, r, vol, 'call') for S in stock_prices]
    axs[0, 1].plot(stock_prices, call_theta, label=f'Vol: {int(vol*100)}%')
axs[0, 1].legend()
axs[0, 1].set_ylim(-0.1, 0.02)  

# Theta Put vs Stock Prices (single volatility)
axs[1, 0].set_title('Theta Put vs Stock Prices')
axs[1, 0].set_xlabel('Stock Price ($)')
axs[1, 0].set_ylabel('Theta (Θ) per day')
axs[1, 0].grid(True)

put_theta = [calculate_theta(S, K, T, r, sigma, 'put') for S in stock_prices]
axs[1, 0].plot(stock_prices, put_theta, 'b-')
axs[1, 0].set_ylim(min(put_theta) * 1.1, max(0, max(put_theta)) * 1.1)

# Theta Put vs Stock Prices (different volatilities)
axs[1, 1].set_title('Theta Put vs Stock Prices for Different Volatilities')
axs[1, 1].set_xlabel('Stock Price ($)')
axs[1, 1].set_ylabel('Theta (Θ) per day')
axs[1, 1].grid(True)

for vol in volatilities:
    put_theta = [calculate_theta(S, K, T, r, vol, 'put') for S in stock_prices]
    axs[1, 1].plot(stock_prices, put_theta, label=f'Vol: {int(vol*100)}%')
axs[1, 1].legend()
axs[1, 1].set_ylim(-0.1, 0.02) 

plt.tight_layout()
plt.show()

