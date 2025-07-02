"""
This script visualizes the relationship between expected credit loss and recovery rate for a fixed loan.
Expected Credit Loss (ECL) represents the amount a lender expects to lose on a loan due to default.
It's calculated as: ECL = Notional × Default Probability × (1 - Recovery Rate). As recovery rate increases,
the expected loss decreases linearly. In this example, we use a $10 million notional amount with a 3% 
default probability and examine how expected losses change as recovery rates vary from 0% to 80%.
"""

import numpy as np
import matplotlib.pyplot as plt

notional = 10_000_000  # million
default_probability = 0.03 

# 0% to 80% in 5% increments
recovery_rates = np.arange(0, 0.85, 0.05)

expected_losses = notional * default_probability * (1 - recovery_rates)

plt.figure(figsize=(10, 6))
plt.plot(recovery_rates * 100, expected_losses, marker='o', linestyle='-', linewidth=2, color='blue')

plt.xlabel('Recovery Rate (%)', fontsize=12)
plt.ylabel('Expected Credit Loss ($)', fontsize=12)
plt.title('Expected Credit Loss vs Recovery Rate', fontsize=14)

plt.grid(True, linestyle='--', alpha=0.7)

plt.gca().yaxis.set_major_formatter('${:,.0f}'.format)

plt.tight_layout()
plt.show()

print("Recovery Rate (%) | Expected Credit Loss ($)")
print("-" * 45)
for rate, loss in zip(recovery_rates * 100, expected_losses):
    print(f"{rate:14.1f} | ${loss:,.2f}")
