import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.patches import Patch

np.random.seed(42)

S0 = 100  
mu = 0.05  
sigma = 0.2 
T = 1.0 
N = 252 
paths = 3 

dt = T/N  
t = np.linspace(0, T, N+1) 

def simulate_gbm_paths(S0, mu, sigma, T, N, paths):
    Z = np.random.normal(0, 1, size=(paths, N))
    daily_returns = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    
    S = np.zeros((paths, N+1))
    S[:, 0] = S0
    
    for i in range(N):
        S[:, i+1] = S[:, i] * daily_returns[:, i]
    
    return S

price_paths = simulate_gbm_paths(S0, mu, sigma, T, N, paths)

running_max = np.maximum.accumulate(price_paths, axis=1)
running_min = np.minimum.accumulate(price_paths, axis=1)

plt.figure(figsize=(15, 12))
colors = ['#3366CC', '#DC3912', '#FF9900']
line_styles = ['-', '--', '-.']

for i in range(paths):
    plt.subplot(paths, 1, i+1)
    color_index = i % len(colors)
    plt.plot(t, price_paths[i], color=colors[color_index], linewidth=2, label=f'Asset Price Path {i+1}')
    
    plt.plot(t, running_max[i], color='green', linewidth=1.5, linestyle='--', 
             label=f'Running Maximum (Floating Strike for Put)')
    
    plt.plot(t, running_min[i], color='red', linewidth=1.5, linestyle='--',
             label=f'Running Minimum (Floating Strike for Call)')
    
    plt.fill_between(t, price_paths[i], running_max[i], color='green', alpha=0.2)
    
    plt.fill_between(t, running_min[i], price_paths[i], color='red', alpha=0.2)
    
    final_max = running_max[i, -1]
    final_min = running_min[i, -1]
    final_price = price_paths[i, -1]
    
    put_payoff = max(0, final_max - final_price)
    
    call_payoff = max(0, final_price - final_min)
    
    plt.annotate(f'Lookback Put Payoff: ${put_payoff:.2f}', 
                 xy=(0.98, 0.95), xycoords='axes fraction',
                 fontsize=10, ha='right', va='top',
                 bbox=dict(boxstyle='round,pad=0.5', fc='green', alpha=0.2))
    
    plt.annotate(f'Lookback Call Payoff: ${call_payoff:.2f}', 
                 xy=(0.98, 0.85), xycoords='axes fraction',
                 fontsize=10, ha='right', va='top',
                 bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.2))
    
    plt.title(f'Path {i+1}: Asset Price with Running Max and Min', fontsize=14)
    plt.xlabel('Time (years)', fontsize=12)
    plt.ylabel('Price ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper left')
    
    plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:.0f}'))

plt.tight_layout()
plt.suptitle('Monte Carlo Simulation: Path vs Max/Min Evolution for Lookback Options', fontsize=16, y=1.02)

plt.show()

print("\nLookback Options - Key Insights:")
print("--------------------------------")
print("1. Path Dependency: Payoff depends on the entire price path, not just the final price.")
print("2. Floating Strike Call: Pays the difference between final price and minimum observed price.")
print("3. Floating Strike Put: Pays the difference between maximum observed price and final price.")
print("4. Lookback options allow investors to 'look back' and choose the best price retrospectively.")
print("5. These options are more expensive than standard options due to their path-dependent nature.")
