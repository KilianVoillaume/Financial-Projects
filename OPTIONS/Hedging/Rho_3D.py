import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm as N

S_range = np.linspace(50, 150, 150) 
t_range = np.linspace(0.01, 5, 150)  

K = 100    
r = 0.05   
q = 0.02   
sigma = 0.1  

# Meshgrid for stock prices and time to maturity
S_range, t_range = np.meshgrid(S_range, t_range)

def rho(S0, K, T, r, Q, vol, underlying_shares=100.0, otype='call'):
    d2 = (np.log(S0/K) + (r - Q - 0.5 * vol**2.0) * T) / (vol * np.sqrt(T))
    
    if otype == 'call':
        return (K * T * np.exp(-r*T) * N.cdf(d2)) 
    elif otype == 'put':
        return (-K * T * np.exp(-r*T) * N.cdf(-d2)) 
    else:
        raise ValueError("otype must be 'call' or 'put'")

Rhos_c = rho(S_range, K, t_range, r, q, sigma, 'call')
Rhos_p = rho(S_range, K, t_range, r, q, sigma, 'put')

# Rho for Call 
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(S_range, t_range, Rhos_c, cmap='viridis', alpha=0.8)
ax.set_title('Rho Call Option vs Stock Price ($) & Time to Maturity (Y)')
ax.set_xlabel('Stock Price ($)')
ax.set_ylabel('Time to Maturity (Y)')
ax.set_zlabel('Rho')
fig.colorbar(surf, shrink=0.5, aspect=8, label='Rho')
plt.show()

# Rho for Put 
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(S_range, t_range, Rhos_p, cmap='viridis', alpha=0.8)
ax.set_title('Rho Put Option vs Stock Price ($) & Time to Maturity (Y)')
ax.set_xlabel('Stock Price ($)')
ax.set_ylabel('Time to Maturity (Y)')
ax.set_zlabel('Rho')
fig.colorbar(surf, shrink=0.5, aspect=8, label='Rho')
plt.show()

