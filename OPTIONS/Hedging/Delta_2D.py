from math import sqrt, pi
from scipy.stats import norm as N
import numpy as np
import matplotlib.pyplot as plt

stock_prices = np.linspace(50, 150, 200)
S = stock_prices

K = 100 
T = 1.0  
r = 0.05  
Q = 0.02  
sigma = 0.1 
vol = [0.1, 0.2, 0.3, 0.4, 0.5] 


def delta(S0, K, T, r, Q, vol, otype='call'):
    d1 = (np.log(S0/K) + (r - Q + 0.5 * vol**2.0) * T) / (vol * np.sqrt(T))
    
    if otype == 'call':
        return np.exp(-Q*T) * N.cdf(d1)
    elif otype == 'put':
        return -np.exp(-Q*T) * N.cdf(-d1)
    else:
        raise ValueError("otype must be 'call' or 'put'")


delta_call = delta(S, K, T, r, Q, sigma, 'call')
delta_put = delta(S, K, T, r, Q, sigma, 'put')

delta_call_vols = {}
delta_put_vols = {}
for sigma in vol:
    delta_call_vols[sigma] = delta(stock_prices, K, T, r, Q, sigma, 'call')
    delta_put_vols[sigma] = delta(stock_prices, K, T, r, Q, sigma, 'put')

fig, ax = plt.subplots(2, 2, figsize=(12,7), gridspec_kw={'hspace': 0.3})

# Deltas for call 
ax[0,0].plot(stock_prices, delta_call, label='Delta')
ax[0,0].set_xlabel('Stock Price ($)')
ax[0,0].set_ylabel('Delta for Call Options')
ax[0,0].set_title('Delta Call vs Stock Prices', fontsize=8)
ax[0,0].grid(True)
ax[0,0].legend()

# Deltas for call with different volatility levels
for sigma, prices in delta_call_vols.items():
    ax[0,1].plot(stock_prices, prices, label=f'Vol: {sigma * 100:.0f}%')

ax[0,1].set_title('Delta Call vs Stock Prices for Different Volatilities', fontsize=8)
ax[0,1].set_xlabel('Stock Price ($)')
ax[0,1].set_ylabel('Delta for Call Options')
ax[0,1].legend(fontsize=8)
ax[0,1].grid(True)

# Deltas for put 
ax[1,0].plot(stock_prices, delta_put, label='Delta')
ax[1,0].set_xlabel('Stock Price ($)')
ax[1,0].set_ylabel('Delta for Put Options')
ax[1,0].set_title('Delta Put vs Stock Prices', fontsize=8)
ax[1,0].grid(True)
ax[1,0].legend()

# Deltas for put  with different volatility levels
for sigma, prices in delta_put_vols.items():
    ax[1,1].plot(stock_prices, prices, label=f'Vol: {sigma * 100:.0f}%')

ax[1,1].set_title('Delta Put vs Stock Prices for Different Volatilities', fontsize=8)
ax[1,1].set_xlabel('Stock Price ($)')
ax[1,1].set_ylabel('Delta for Put Options')
ax[1,1].legend(fontsize=8)
ax[1,1].grid(True)

plt.show()

