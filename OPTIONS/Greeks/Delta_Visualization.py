import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:  # put
        delta = norm.cdf(d1) - 1
        
    return delta


K = 100  
T = 0.5  
r = 0.05 
sigma = 0.2  
volatilities = [0.1, 0.2, 0.3, 0.4, 0.5]  
stock_prices = np.linspace(50, 150, 100)  

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
plt.subplots_adjust(hspace=0.3, wspace=0.3)

# Delta Call vs Stock Prices (single volatility)
axs[0, 0].set_title('Delta Call vs Stock Prices')
axs[0, 0].set_xlabel('Stock Price ($)')
axs[0, 0].set_ylabel('Delta for Call Options')
axs[0, 0].grid(True)

call_deltas = [black_scholes_delta(S, K, T, r, sigma, 'call') for S in stock_prices]
axs[0, 0].plot(stock_prices, call_deltas, 'b-')
axs[0, 0].set_ylim(0, 1)

# Delta Call vs Stock Prices (different volatilities)
axs[0, 1].set_title('Delta Call vs Stock Prices for Different Volatilities')
axs[0, 1].set_xlabel('Stock Price ($)')
axs[0, 1].set_ylabel('Delta for Call Options')
axs[0, 1].grid(True)

for vol in volatilities:
    call_deltas = [black_scholes_delta(S, K, T, r, vol, 'call') for S in stock_prices]
    axs[0, 1].plot(stock_prices, call_deltas, label=f'Vol: {int(vol*100)}%')
axs[0, 1].legend()
axs[0, 1].set_ylim(0, 1)

# Delta Put vs Stock Prices (single volatility)
axs[1, 0].set_title('Delta Put vs Stock Prices')
axs[1, 0].set_xlabel('Stock Price ($)')
axs[1, 0].set_ylabel('Delta for Put Options')
axs[1, 0].grid(True)

put_deltas = [black_scholes_delta(S, K, T, r, sigma, 'put') for S in stock_prices]
axs[1, 0].plot(stock_prices, put_deltas, 'b-')
axs[1, 0].set_ylim(-1, 0)

# Delta Put vs Stock Prices (different volatilities)
axs[1, 1].set_title('Delta Put vs Stock Prices for Different Volatilities')
axs[1, 1].set_xlabel('Stock Price ($)')
axs[1, 1].set_ylabel('Delta for Put Options')
axs[1, 1].grid(True)

for vol in volatilities:
    put_deltas = [black_scholes_delta(S, K, T, r, vol, 'put') for S in stock_prices]
    axs[1, 1].plot(stock_prices, put_deltas, label=f'Vol: {int(vol*100)}%')
axs[1, 1].legend()
axs[1, 1].set_ylim(-1, 0)

plt.tight_layout()
plt.show()
