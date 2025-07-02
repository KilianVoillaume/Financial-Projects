from scipy.stats import norm as N
import numpy as np
import matplotlib.pyplot as plt

stock_prices = np.linspace(10, 300, 100)

K = 100  
t = 1  
r = 0.05  
q = 0.02  
Sigma = 0.2  
Volatilities = [0.1, 0.2, 0.35, 0.4]  

def vega(S0, K, T, r, Q, vol, underlying_shares=100.0):
    d1 = (np.log(S0/K) + (r - Q + 0.5 * vol**2.0) * T) / (vol * np.sqrt(T))
    return (S0 * np.exp(-Q*T) * N.pdf(d1) * np.sqrt(T)) / underlying_shares

vegas = vega(stock_prices, K, t, r, q, Sigma)

vegas_vol = {}
for sigma in Volatilities:
    vegas_vol[sigma] = vega(stock_prices, K, t, r, q, sigma)

# Vega
fig, ax = plt.subplots(2, figsize=(6,6), gridspec_kw={'hspace': 0.4})

ax[0].plot(stock_prices, vegas, label='Vega')
ax[0].set_xlabel('Stock Price ($)')
ax[0].set_ylabel('Vega')
ax[0].set_title('Vega vs. Stock Prices')
ax[0].grid(True)
ax[0].legend()

# Vega for different volatility levels
for sigma, prices in vegas_vol.items():
    ax[1].plot(stock_prices, prices, label=f'Volatility: {sigma * 100:.1f}%')

ax[1].set_title('Vega vs. Stock Prices for Different Volatilities', fontsize=10)
ax[1].set_xlabel('Stock Price ($)')
ax[1].set_ylabel('Vega')
ax[1].legend()
ax[1].grid(True)

plt.show()

