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

def theta(S0, K, T, r, Q, vol, otype='call'):
    d1 = (np.log(S0/K) + (r - Q + 0.5 * vol**2.0) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    
    first_term = -np.exp(-Q*T) * S0 * N.pdf(d1) * vol / (2 * np.sqrt(T))
    
    if otype == 'call':
        second_term = -r * K * np.exp(-r*T) * N.cdf(d2) + Q * S0 * np.exp(-Q*T) * N.cdf(d1)
    elif otype == 'put':
        second_term = r * K * np.exp(-r*T) * N.cdf(-d2) - Q * S0 * np.exp(-Q*T) * N.cdf(-d1)
    else:
        raise ValueError("otype must be 'call' or 'put'")
    
    return (first_term + second_term) / 365.0

theta_call = theta(S, K, t, r, q, Sigma, 'call')
theta_put = theta(S, K, t, r, q, Sigma, 'put')

theta_call_vols = {}
theta_put_vols = {}
for sigma in Volatilities:
    theta_call_vols[sigma] = theta(stock_prices, K, t, r, q, sigma, 'call')
    theta_put_vols[sigma] = theta(stock_prices, K, t, r, q, sigma, 'put')

fig, ax = plt.subplots(2, 2, figsize=(7,7), gridspec_kw={'hspace': 0.3})

# Thetas for call 
ax[0,0].plot(stock_prices, theta_call, label='Theta')
ax[0,0].set_xlabel('Stock Price ($)')
ax[0,0].set_ylabel('Theta for Call Options')
ax[0,0].set_title('Theta Call vs Stock Prices', fontsize=8)
ax[0,0].grid(True)
ax[0,0].legend()

# Thetas for call with different volatility levels
for sigma, prices in theta_call_vols.items():
    ax[0,1].plot(stock_prices, prices, label=f'Vol: {sigma * 100:.0f}%')

ax[0,1].set_title('Theta Call vs Stock Prices for Different Volatilities', fontsize=8)
ax[0,1].set_xlabel('Stock Price ($)')
ax[0,1].set_ylabel('Theta for Call Options')
ax[0,1].legend(fontsize=8)
ax[0,1].grid(True)

# Thetas for put 
ax[1,0].plot(stock_prices, theta_put, label='Theta')
ax[1,0].set_xlabel('Stock Price ($)')
ax[1,0].set_ylabel('Theta for Put Options')
ax[1,0].set_title('Theta Put vs Stock Prices', fontsize=8)
ax[1,0].grid(True)
ax[1,0].legend()

# Thetas for put with different volatility levels
for sigma, prices in theta_put_vols.items():
    ax[1,1].plot(stock_prices, prices, label=f'Vol: {sigma * 100:.0f}%')

ax[1,1].set_title('Theta Put vs Stock Prices for Different Volatilities', fontsize=8)
ax[1,1].set_xlabel('Stock Price ($)')
ax[1,1].set_ylabel('Theta for Put Options')
ax[1,1].legend(fontsize=8)
ax[1,1].grid(True)

plt.show()

