import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm as N

S_range = np.linspace(50, 150, 150) 
t_range = np.linspace(0.01, 1, 150)  

K = 100   
r = 0.05   
q = 0.02  
sigma = 0.1 

# Creating the meshgrid for stock prices and time to maturity
S_range, t_range = np.meshgrid(S_range, t_range)

def gamma(S0, K, T, r, Q, vol):
    d1 = (np.log(S0/K) + (r - Q + 0.5 * vol**2.0) * T) / (vol * np.sqrt(T))
    return np.exp(-Q*T) * N.pdf(d1) / (S0 * vol * np.sqrt(T))

Gammas = gamma(S_range, K, t_range, r, q, sigma)

# Gamma
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(S_range, t_range, Gammas, cmap='viridis', edgecolor='k', alpha=0.8)
ax.set_title('Gamma vs Stock Price ($) & Time to Maturity (Y)')
ax.set_xlabel('Stock Price ($)')
ax.set_ylabel('Time to Maturity (Y)')
ax.set_zlabel('Gamma')
fig.colorbar(surf, shrink=0.5, aspect=8, label='Gamma')
plt.show()

