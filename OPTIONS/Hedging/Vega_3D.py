import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm as N


S_range = np.linspace(50, 200, 200)  
t_range = np.linspace(0.2, 1, 200)   

K = 100    
r = 0.05   
t = 1
q = 0.02   
sigma = 0.2  

# Creating the meshgrid for stock prices and time to maturity
S_range, t_range = np.meshgrid(S_range, t_range)


def vega(S0, K, T, r, Q, vol, underlying_shares=100.0):
    d1 = (np.log(S0/K) + (r - Q + 0.5 * vol**2.0) * T) / (vol * np.sqrt(T))
    return (S0 * np.exp(-Q*T) * N.pdf(d1) * np.sqrt(T)) / underlying_shares

Vegas = vega(S_range, K, t_range, r, q, sigma)

# Vega
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(S_range, t_range, Vegas, cmap='viridis', edgecolor='k', alpha=0.8)
ax.set_title('Vega vs Stock Price ($) & Time to Maturity (Y)')
ax.set_xlabel('Stock Price ($)')
ax.set_ylabel('Time to Maturity (Y)')
ax.set_zlabel('Vega')
fig.colorbar(surf, shrink=0.5, aspect=8, label='Vega')
plt.show()

