import numpy as np
import matplotlib.pyplot as plt

def simulate_barrier_paths(S0=100, K=100, barrier=120, r=0.05, sigma=0.2, T=1, n_paths=50):
    n_steps = 252
    dt = T / n_steps
    paths = np.zeros((n_steps + 1, n_paths))
    paths[0] = S0
    
    for t in range(1, n_steps + 1):
        z = np.random.standard_normal(n_paths)
        paths[t] = paths[t - 1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    
    crossed = np.any(paths >= barrier, axis=0)
    final_prices = paths[-1]
    payoffs = np.where(crossed, 0, np.maximum(final_prices - K, 0))
    
    return paths, crossed, payoffs

S0, K, barrier = 100, 100, 125
paths, crossed, payoffs = simulate_barrier_paths(S0=S0, K=K, barrier=barrier)

plt.figure(figsize=(10, 6))
time = np.linspace(0, 1, paths.shape[0])

# Non-crossed paths (gray)
plt.plot(time, paths[:, ~crossed], color='gray', alpha=0.3)

# Crossed paths (red, no label)
plt.plot(time, paths[:, crossed], color='red', alpha=0.7)

plt.plot([], [], color='red', alpha=0.7, label='Paths that crossed the barrier')

itm = (payoffs > 0) & (~crossed)
otm = (payoffs == 0) & (~crossed)

plt.scatter([1] * sum(itm), paths[-1][itm], color='green', label='ITM Payoff (price > strike)')
plt.scatter([1] * sum(otm), paths[-1][otm], color='red', label='OTM Payoff (price ≤ strike)')

plt.axhline(barrier, color='black', linestyle='--', label=f'Barrier ({barrier})')
plt.axhline(K, color='blue', linestyle=':', label=f'Strike ({K})')

plt.title('Barrier Option Path Simulation (Up-and-Out)')
plt.xlabel('Time (Years)')
plt.ylabel('Stock Price')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()
