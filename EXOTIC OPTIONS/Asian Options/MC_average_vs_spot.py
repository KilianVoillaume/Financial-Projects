import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm as cm

np.random.seed(42)

S0 = 100  
r = 0.05  
sigma = 0.2  
T = 1.0  
dt = 1/252  
n_steps = int(T / dt) 
n_paths = 15 
time = np.linspace(0, T, n_steps+1)

def simulate_gbm(S0, r, sigma, T, dt, n_steps, n_paths):
    # Initialize arrays
    S = np.zeros((n_paths, n_steps+1))
    S[:, 0] = S0
    
    Z = np.random.normal(0, 1, size=(n_paths, n_steps))
    for t in range(1, n_steps+1):
        S[:, t] = S[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t-1])
    
    return S

def calculate_average(S):
    S_avg = np.zeros_like(S)
    
    for t in range(1, S.shape[1]):
        S_avg[:, t] = np.mean(S[:, 1:t+1], axis=1)
    
    return S_avg

spot_paths = simulate_gbm(S0, r, sigma, T, dt, n_steps, n_paths)
avg_paths = calculate_average(spot_paths)
colors = cm.viridis(np.linspace(0, 0.8, n_paths))
plt.figure(figsize=(12, 8))

for i in range(n_paths):
    plt.plot(time, spot_paths[i], color=colors[i], alpha=0.4, linewidth=1)
    
    plt.plot(time, avg_paths[i], color=colors[i], alpha=0.8, linewidth=1.5, linestyle='--')

plt.title('Monte Carlo Simulation: Evolution of Spot vs Average Price', fontsize=16)
plt.xlabel('Time (years)', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.grid(True, alpha=0.3)

legend_elements = [
    Line2D([0], [0], color='gray', alpha=0.4, linewidth=1.5, label='Spot Price (S_t)'),
    Line2D([0], [0], color='gray', alpha=0.8, linewidth=2, linestyle='--', label='Cumulative Average Price (S̄_t)')
]
plt.legend(handles=legend_elements, loc='upper left', fontsize=12)

plt.annotate('Average price smooths out\nspikes in spot price', 
             xy=(0.5, spot_paths.mean() * 0.85), 
             xytext=(0.5, spot_paths.mean() * 0.7),
             arrowprops=dict(arrowstyle='->'),
             fontsize=10, ha='center')

plt.annotate('Average price lags\nbehind fast movements', 
             xy=(0.2, spot_paths.mean() * 1.1), 
             xytext=(0.2, spot_paths.mean() * 1.25),
             arrowprops=dict(arrowstyle='->'),
             fontsize=10, ha='center')

plt.annotate('Average converges\nover time', 
             xy=(0.85, spot_paths.mean() * 0.95), 
             xytext=(0.8, spot_paths.mean() * 0.6),
             arrowprops=dict(arrowstyle='->'),
             fontsize=10, ha='center')


plt.tight_layout()
plt.savefig('spot_vs_average_price.png', dpi=300)
plt.show()
