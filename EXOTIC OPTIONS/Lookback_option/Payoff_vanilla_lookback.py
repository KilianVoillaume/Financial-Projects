import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.patches import Patch

np.random.seed(42)

# Parameters
S0 = 100      
mu = 0.05     
sigma = 0.25   
T = 1.0       
N = 252        
K = 105        

dt = T/N      
t = np.linspace(0, T, N+1) 

def simulate_gbm_path(S0, mu, sigma, T, N):
    Z = np.random.normal(0, 1, N)
    daily_returns = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
    
    S = np.zeros(N+1)
    S[0] = S0
    
    for i in range(N):
        S[i+1] = S[i] * daily_returns[i]
    
    return S

def find_suitable_path(max_attempts=100):
    for _ in range(max_attempts):
        path = simulate_gbm_path(S0, mu, sigma, T, N)
        
        S_T = path[-1]
        S_min = np.min(path)
        S_max = np.max(path)
        
        # Check if the path meets our criteria:
        # 1. Final price is not at its max
        # 2. There's a meaningful difference between S_T and S_min
        # 3. Final price is below strike (to show lookback advantage)
        if (S_T < S_max and 
            (S_T - S_min) > 5 and 
            S_T < K):
            return path
    
    # If no suitable path, return last one simulated
    return path

# Suitable path
price_path = find_suitable_path()

running_min = np.minimum.accumulate(price_path)
running_max = np.maximum.accumulate(price_path)

final_price = price_path[-1]
min_price = running_min[-1]
max_price = running_max[-1]

strikes = np.linspace(80, 120, 100)

vanilla_payoffs = np.maximum(final_price - strikes, 0)
lookback_payoffs = np.maximum(final_price - running_min, 0)  # Same for all strikes

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), gridspec_kw={'height_ratios': [2, 1]})

ax1.plot(t, price_path, 'b-', linewidth=2, label='Asset Price Path')
ax1.plot(t, running_min, 'r--', linewidth=1.5, label='Running Minimum (Floating Strike)')
ax1.axhline(y=K, color='g', linestyle='-.', label=f'Vanilla Strike (K=${K:.2f})')

ax1.fill_between(t, running_min, price_path, color='lightcoral', alpha=0.3)

ax1.plot(T, final_price, 'bo', markersize=8)
ax1.annotate(f'Final Price: ${final_price:.2f}', 
             xy=(T, final_price), xytext=(T-0.1, final_price+5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=10)

min_idx = np.argmin(price_path)
ax1.plot(t[min_idx], min_price, 'ro', markersize=8)
ax1.annotate(f'Minimum Price: ${min_price:.2f}', 
             xy=(t[min_idx], min_price), xytext=(t[min_idx]-0.35, min_price-10),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=10)

ax1.set_title('Asset Price Path with Running Minimum', fontsize=14)
ax1.set_xlabel('Time (years)', fontsize=12)
ax1.set_ylabel('Price ($)', fontsize=12)
ax1.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:.0f}'))
ax1.grid(True, alpha=0.3)
ax1.legend(loc='best')

vanilla_payoff = max(final_price - K, 0)
lookback_payoff = max(final_price - min_price, 0)

bar_width = 0.3
bar_positions = [1, 2]
payoffs = [vanilla_payoff, lookback_payoff]
labels = ['Vanilla Call', 'Lookback Call']
colors = ['green', 'red']

bars = ax2.bar(bar_positions, payoffs, bar_width, color=colors, alpha=0.7)

for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'${height:.2f}', ha='center', va='bottom', fontsize=12)

ax2.text(1, -3, f'max(S_T - K, 0)\n= max({final_price:.2f} - {K:.2f}, 0)\n= {vanilla_payoff:.2f}', 
         ha='center', va='top', fontsize=10)
ax2.text(2, -3, f'max(S_T - S_min, 0)\n= max({final_price:.2f} - {min_price:.2f}, 0)\n= {lookback_payoff:.2f}', 
         ha='center', va='top', fontsize=10)

ax2.set_title('Payoff Comparison: Lookback Call vs Vanilla Call', fontsize=14)
ax2.set_ylabel('Payoff ($)', fontsize=12)
ax2.set_xticks(bar_positions)
ax2.set_xticklabels(labels, fontsize=12)
ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:.0f}'))
ax2.grid(True, axis='y', alpha=0.3)

ax2.set_ylim([-15, max(payoffs) * 1.2])

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)
plt.show()

plt.figure(figsize=(10, 6))

plt.plot(strikes, vanilla_payoffs, 'g-', linewidth=2, label='Vanilla Call Payoff')
plt.axhline(y=lookback_payoffs[0], color='r', linestyle='-', linewidth=2, 
            label=f'Lookback Call Payoff (${lookback_payoffs[0]:.2f})')

# Mark the chosen strike K
plt.axvline(x=K, color='blue', linestyle='--', label=f'Strike Price K=${K:.2f}')

# Mark the final price
plt.axvline(x=final_price, color='black', linestyle=':', label=f'Final Price S_T=${final_price:.2f}')

# Mark the minimum price 
plt.axvline(x=min_price, color='red', linestyle=':', label=f'Minimum Price S_min=${min_price:.2f}')

plt.title('Payoff Curves: Lookback Call vs Vanilla Call', fontsize=14)
plt.xlabel('Strike Price ($)', fontsize=12)
plt.ylabel('Payoff ($)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(loc='best')

plt.tight_layout()
plt.show()
