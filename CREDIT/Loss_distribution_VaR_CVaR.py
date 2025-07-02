"""
Credit Portfolio Loss Distribution Simulation
This script simulates the distribution of potential losses in a credit portfolio using
a normal distribution approximation. It calculates two important risk metrics:
- Value at Risk (VaR): The maximum loss expected at a given confidence level (e.g., 99%)
- Conditional Value at Risk (CVaR): The average loss in the worst cases that exceed VaR
These metrics help financial institutions quantify portfolio risk and set appropriate reserves.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

np.random.seed(42)

mean_loss = 0.05  
std_dev_loss = 0.03  
num_simulations = 100000  

simulated_losses = np.random.normal(mean_loss, std_dev_loss, num_simulations)
confidence_level = 0.99
var_99 = np.percentile(simulated_losses, confidence_level * 100)
cvar_99 = simulated_losses[simulated_losses >= var_99].mean()

plt.figure(figsize=(12, 8))
sns.set_style('whitegrid')

# Losses with KDE
sns.histplot(simulated_losses, bins=100, kde=True, color='skyblue', alpha=0.7)

plt.axvline(x=var_99, color='red', linestyle='--', linewidth=2, 
            label=f'99% VaR: {var_99:.2%}')

plt.axvline(x=cvar_99, color='darkred', linestyle='-', linewidth=2, 
            label=f'99% CVaR: {cvar_99:.2%}')

plt.xlabel('Portfolio Loss', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.title('Credit Portfolio Loss Distribution Simulation', fontsize=16, fontweight='bold')
plt.legend(fontsize=12)

plt.annotate(f"Mean: {mean_loss:.2%}\nStd Dev: {std_dev_loss:.2%}\nSimulations: {num_simulations:,}", 
             xy=(0.02, 0.95), xycoords='axes fraction', 
             fontsize=12, bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.8))

print(f"Portfolio Loss Distribution Summary:")
print(f"Mean Loss: {mean_loss:.2%}")
print(f"Standard Deviation: {std_dev_loss:.2%}")
print(f"99% Value at Risk (VaR): {var_99:.2%}")
print(f"99% Conditional Value at Risk (CVaR): {cvar_99:.2%}")
print(f"Ratio of CVaR to VaR: {cvar_99/var_99:.2f}")

plt.tight_layout()
plt.show()
