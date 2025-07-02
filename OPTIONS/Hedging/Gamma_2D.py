from scipy.stats import norm as N
import numpy as np
import matplotlib.pyplot as plt

stock_prices = np.linspace(50, 150, 200)
S = stock_prices

K = 100  
t = 1.0 
r = 0.05
q = 0.02 
Sigma = 0.1
Volatilities = [0.1, 0.2, 0.3, 0.4, 0.5]  

def gamma(S0, K, T, r, Q, vol):
    d1 = (np.log(S0/K) + (r - Q + 0.5 * vol**2.0) * T) / (vol * np.sqrt(T))
    return np.exp(-Q*T) * N.pdf(d1) / (S0 * vol * np.sqrt(T))

gammas = gamma(S, K, t, r, q, Sigma)

gamma_vols = {}
for sigma in Volatilities:
    gamma_vols[sigma] = gamma(stock_prices, K, t, r, q, sigma)

fig, ax = plt.subplots(2, figsize=(7,7), gridspec_kw={'hspace': 0.3})

# Gammas vs. Stock Prices
ax[0].plot(stock_prices, gammas, label=f'Vol: {Sigma * 100:.0f}%')
ax[0].set_xlabel('Stock Price ($)')
ax[0].set_ylabel('Gamma')
ax[0].set_title('Gamma vs Stock Prices', fontsize=8)
ax[0].legend(fontsize=8)
ax[0].grid(True)

# Gamma with different volatility levels
for sigma, prices in gamma_vols.items():
    ax[1].plot(stock_prices, prices, label=f'Vol: {sigma * 100:.0f}%')

ax[1].set_title('Gamma vs Stock Prices for Different Volatilities', fontsize=8)
ax[1].set_xlabel('Stock Price ($)')
ax[1].set_ylabel('Gamma')
ax[1].legend(fontsize=8)
ax[1].grid(True)

plt.show()

