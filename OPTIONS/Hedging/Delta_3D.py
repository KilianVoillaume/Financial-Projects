from math import sqrt, pi
from scipy.stats import norm as N
import numpy as np
import matplotlib.pyplot as plt

S_range = np.linspace(50, 150, 150)
t_range = np.linspace(0.01, 1, 150) 

K = 100    
r = 0.05   
q = 0.02   
sigma = 0.1 

# Creating the meshgrid for stock prices and time to maturity
S_range, t_range = np.meshgrid(S_range, t_range)

def delta(S0, K, T, r, Q, vol, otype='call'):
    d1 = (np.log(S0/K) + (r - Q + 0.5 * vol**2.0) * T) / (vol * np.sqrt(T))
    
    if otype == 'call':
        return np.exp(-Q*T) * N.cdf(d1)
    elif otype == 'put':
        return -np.exp(-Q*T) * N.cdf(-d1)
    else:
        raise ValueError("otype must be 'call' or 'put'")

Deltas_c = delta(S_range, K, t_range, r, q, sigma, 'call')
Deltas_p = delta(S_range, K, t_range, r, q, sigma, 'put')

# Delta call
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(S_range, t_range, Deltas_c, cmap='viridis', alpha=0.8)
ax.set_title('Delta Call Option vs Stock Price ($) & Time to Maturity (Y)')
ax.set_xlabel('Stock Price ($)')
ax.set_ylabel('Time to Expiration (Y)')
ax.set_zlabel('Delta')
fig.colorbar(surf, shrink=0.5, aspect=8, label='Delta')
plt.show()

# Delta put
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(S_range, t_range, Deltas_p, cmap='viridis', alpha=0.8)
ax.set_title('Delta Put Option vs Stock Price ($) & Time to Maturity (Y)')
ax.set_xlabel('Stock Price ($)')
ax.set_ylabel('Time to Expiration (Y)')
ax.set_zlabel('Delta')
fig.colorbar(surf, shrink=0.5, aspect=8, label='Delta')
plt.show()

