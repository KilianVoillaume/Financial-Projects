import numpy as np
import matplotlib.pyplot as plt

"""
Survival Probability Analysis in Credit Risk

This script visualizes survival probability curves used in credit risk modeling.
The survival probability P[τ > t] = e^(-λt) represents the probability that default
has not occurred by time t, given a constant default intensity λ. Lower λ values
indicate better credit quality (lower default risk), while higher λ values indicate
poorer credit quality (higher default risk). These curves are fundamental in pricing
credit derivatives and calculating expected loss metrics.
"""

t = np.linspace(0, 10, 1000)

lambda_values = [0.01, 0.05, 0.10]
colors = ['blue', 'green', 'red']
labels = [f'λ = {lambda_val}' for lambda_val in lambda_values]

plt.figure(figsize=(10, 6))

for i, lambda_val in enumerate(lambda_values):
    survival_prob = np.exp(-lambda_val * t)
    plt.plot(t, survival_prob, color=colors[i], linewidth=2, label=labels[i])

plt.title('Survival Probability Curves: P[τ > t] = e^(-λt)', fontsize=14)
plt.xlabel('Time (years)', fontsize=12)
plt.ylabel('Survival Probability', fontsize=12)
plt.grid(True, alpha=0.3)
plt.ylim(0, 1.05)
plt.xlim(0, 10)
plt.legend(loc='best')

plt.text(7, 0.83, 'λ = 0.01: Lower intensity, slower decay', color='blue', fontsize=9)
plt.text(5, 0.68, 'λ = 0.05: Medium intensity', color='green', fontsize=9)
plt.text(2.5, 0.55, 'λ = 0.10: Higher intensity, faster decay', color='red', fontsize=9)

plt.tight_layout()
plt.savefig('survival_probability_curves.png', dpi=300)
plt.show()

print("Survival probabilities at key time points:")
print("-" * 50)
print("Time (years) | λ = 0.01   | λ = 0.05   | λ = 0.10")
print("-" * 50)
for year in [1, 3, 5, 10]:
    survival_01 = np.exp(-0.01 * year)
    survival_05 = np.exp(-0.05 * year)
    survival_10 = np.exp(-0.10 * year)
    print(f"{year:12d} | {survival_01:.6f} | {survival_05:.6f} | {survival_10:.6f}")
