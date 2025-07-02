# Credit Triangle Visualization
# 
# This code visualizes the fundamental credit triangle relationship in credit default swaps (CDS).
# The credit triangle states that CDS spread = default probability × (1 - recovery rate).
# This relationship demonstrates how both default risk and recovery expectations affect credit pricing.
# Higher default probability increases CDS spreads, while higher recovery rates decrease them.
# The visualization shows this relationship for three different recovery rates (20%, 40%, 60%).

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

default_probs = np.linspace(0, 0.10, 100)  # 0% to 10%

recovery_rates = [0.20, 0.40, 0.60]  # 20%, 40%, 60%

plt.figure(figsize=(10, 6))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green

for i, recovery_rate in enumerate(recovery_rates):
    cds_spreads = default_probs * (1 - recovery_rate) * 10000 
    
    plt.plot(default_probs * 100, cds_spreads, 
             label=f'Recovery Rate = {int(recovery_rate * 100)}%',
             linewidth=2.5, color=colors[i])

plt.title('Credit Triangle Relationship: CDS Spread vs Default Probability', fontsize=14, fontweight='bold')
plt.xlabel('Default Probability (%)', fontsize=12)
plt.ylabel('CDS Spread (basis points)', fontsize=12)
plt.grid(True, alpha=0.3, linestyle='--')

plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter())
plt.xlim(0, 10)  # 0% to 10%
plt.ylim(0, None)  # Start at 0, let the upper bound be determined automatically

plt.legend(fontsize=11)

formula_text = r'CDS Spread = Default Probability × (1 - Recovery Rate)'
plt.annotate(formula_text, xy=(0.5, 0.02), xycoords='figure fraction', 
             bbox=dict(boxstyle="round,pad=0.5", fc="lighty yellow", ec="orange", alpha=0.8),
             ha='center', fontsize=11)

plt.tight_layout()

plt.show()
