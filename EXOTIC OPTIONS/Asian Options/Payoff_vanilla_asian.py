import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.ticker as mticker

K = 100 
S0 = 100  
r = 0.05 
sigma = 0.2 
T = 1 
n_paths = 50  
n_steps = 252 
np.random.seed(42)  # For reproducibility

dt = T / n_steps
times = np.linspace(0, T, n_steps+1)
price_paths = np.zeros((n_paths, n_steps+1))
price_paths[:, 0] = S0

for i in range(n_paths):
    z = np.random.standard_normal(n_steps)
    for j in range(n_steps):
        price_paths[i, j+1] = price_paths[i, j] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z[j])

avg_prices = np.mean(price_paths, axis=1)

final_prices = price_paths[:, -1]

spot_range = np.linspace(70, 140, 1000)

vanilla_call_payoffs = np.maximum(spot_range - K, 0)

selected_path = 2  # Choose which path to highlight
selected_final_price = final_prices[selected_path]
selected_avg_price = avg_prices[selected_path]

vanilla_payoff = max(selected_final_price - K, 0)
asian_payoff = max(selected_avg_price - K, 0)

plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
for i in range(n_paths):
    if i == selected_path:
        plt.plot(times, price_paths[i], 'b-', linewidth=2, label=f'Selected Path (Path {selected_path+1})')
        plt.axhline(y=avg_prices[i], color='green', linestyle='--', 
                   label=f'Average Price = {avg_prices[i]:.2f}')
    else:
        plt.plot(times, price_paths[i], 'gray', alpha=0.3)

plt.axhline(y=K, color='red', linestyle='-', alpha=0.5, label=f'Strike (K) = {K}')
plt.title('Spot Price Paths')
plt.xlabel('Time to Maturity')
plt.ylabel('Spot Price')
plt.grid(True, alpha=0.3)
plt.legend()
plt.subplot(2, 1, 2)

# Vanilla call payoff curve
plt.plot(spot_range, vanilla_call_payoffs, 'b-', linewidth=2, label='Vanilla Call Payoff')

asian_payoffs = np.ones_like(spot_range) * asian_payoff
plt.plot(spot_range, asian_payoffs, 'g--', linewidth=2, label=f'Asian Call Payoff (avg = {selected_avg_price:.2f})')

plt.plot(selected_final_price, vanilla_payoff, 'bo', markersize=8, 
         label=f'Vanilla Payoff at S_T = {selected_final_price:.2f}: {vanilla_payoff:.2f}')
plt.plot(selected_final_price, asian_payoff, 'go', markersize=8, 
         label=f'Asian Payoff: {asian_payoff:.2f}')

x_fill = np.linspace(K, max(spot_range), 500)
y1 = np.maximum(x_fill - K, 0)
y2 = np.ones_like(x_fill) * asian_payoff
plt.fill_between(x_fill, y1, y2, alpha=0.3, color='red', 
                label='Averaging Effect (Reduction in Payoff)')
plt.axvline(x=K, color='red', linestyle='-', alpha=0.5, label=f'Strike (K) = {K}')

reduction = vanilla_payoff - asian_payoff
plt.annotate(f'Payoff Reduction: {reduction:.2f}',
             xy=(selected_final_price, (vanilla_payoff + asian_payoff)/2),
             xytext=(selected_final_price + 10, (vanilla_payoff + asian_payoff)/2),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=10)

plt.title('Payoff Comparison: Vanilla Call vs Asian Call')
plt.xlabel('Spot Price at Expiry (S_T)')
plt.ylabel('Option Payoff')
plt.grid(True, alpha=0.3)
plt.legend()

plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('$%d'))

plt.tight_layout()
plt.show()

# Add a more comprehensive comparison
print("\nDetailed Comparison:")
print(f"Strike Price (K): {K}")
print(f"Final Spot Price (S_T) for Selected Path: {selected_final_price:.2f}")
print(f"Average Spot Price for Selected Path: {selected_avg_price:.2f}")
print(f"Vanilla Call Payoff: max(S_T - K, 0) = max({selected_final_price:.2f} - {K}, 0) = {vanilla_payoff:.2f}")
print(f"Asian Call Payoff: max(S_avg - K, 0) = max({selected_avg_price:.2f} - {K}, 0) = {asian_payoff:.2f}")
print(f"Reduction in Payoff due to Averaging: {vanilla_payoff - asian_payoff:.2f}")
print(f"Reduction Percentage: {((vanilla_payoff - asian_payoff)/vanilla_payoff*100 if vanilla_payoff > 0 else 0):.2f}%")
