import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from matplotlib.lines import Line2D

np.random.seed(42)

n_simulations = 1000
n_periods = 12  # Monthly resets for 1 year
dt = 1/12  

S0 = 100  
r = 0.05  
sigma = 0.20 
T = 1.0  
K = S0 

local_cap = 0.05  
local_floor = -0.01
global_cap = 0.20  
global_floor = 0.02 

def simulate_paths():
    paths = np.zeros((n_simulations, n_periods + 1))
    paths[:, 0] = S0
    
    for t in range(1, n_periods + 1):
        z = np.random.normal(0, 1, n_simulations)
        # Calculate price movement using GBM
        paths[:, t] = paths[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)
    
    return paths

def calculate_vanilla_payoff(paths):
    final_prices = paths[:, -1]
    return np.maximum(final_prices - K, 0)

def calculate_cliquet_payoff(paths):
    periodic_returns = np.zeros((n_simulations, n_periods))
    
    for t in range(1, n_periods + 1):
        returns = paths[:, t] / paths[:, t-1] - 1  # Calculate returns
        periodic_returns[:, t-1] = np.clip(returns, local_floor, local_cap)  # Apply local cap and floor
    
    total_returns = np.sum(periodic_returns, axis=1)
    total_returns = np.clip(total_returns, global_floor, global_cap)
    
    return S0 * total_returns

def plot_results(vanilla_payoffs, cliquet_payoffs):
    plt.figure(figsize=(14, 8))
    
    sns.set_style("whitegrid")
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 14,
        'axes.titlesize': 16,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'legend.fontsize': 12,
    })
    sns.histplot(vanilla_payoffs, kde=True, stat="density", alpha=0.5, color="blue", label="Vanilla Call")
    sns.histplot(cliquet_payoffs, kde=True, stat="density", alpha=0.5, color="green", label="Cliquet Option")
    
    vanilla_mean = np.mean(vanilla_payoffs)
    cliquet_mean = np.mean(cliquet_payoffs)
    
    plt.axvline(vanilla_mean, color='blue', linestyle='--', alpha=0.7)
    plt.axvline(cliquet_mean, color='green', linestyle='--', alpha=0.7)
    
    cliquet_floor = S0 * (1 + global_floor)
    cliquet_cap = S0 * (1 + global_cap)
    
    plt.axvline(cliquet_floor, color='red', linestyle='-', alpha=0.7)
    plt.axvline(cliquet_cap, color='purple', linestyle='-', alpha=0.7)
    plt.title("Distribution of Final Payoffs: Cliquet vs Vanilla Call Option", fontweight='bold')
    plt.xlabel("Final Payoff ($)")
    plt.ylabel("Density")
    
    legend_elements = [
        Line2D([0], [0], color='blue', alpha=0.7, label='Vanilla Call'),
        Line2D([0], [0], color='green', alpha=0.7, label='Cliquet Option'),
        Line2D([0], [0], color='red', alpha=0.7, label=f'Floor ({global_floor*100}%): ${cliquet_floor:.2f}'),
        Line2D([0], [0], color='purple', alpha=0.7, label=f'Cap ({global_cap*100}%): ${cliquet_cap:.2f}'),
        Line2D([0], [0], color='black', alpha=0, label=f'Monthly Cap: {local_cap*100}%'),
        Line2D([0], [0], color='black', alpha=0, label=f'Monthly Floor: {local_floor*100}%')    
      ]
    
    plt.legend(handles=legend_elements, loc='upper center')
        
    vanilla_stats = (
        f"Vanilla Stats:\n"
        f"Mean: ${vanilla_mean:.2f}\n"
        f"Min: ${np.min(vanilla_payoffs):.2f}\n"
        f"Max: ${np.max(vanilla_payoffs):.2f}\n"
        f"Std Dev: ${np.std(vanilla_payoffs):.2f}"
    )
    
    cliquet_stats = (
        f"Cliquet Stats:\n"
        f"Mean: ${cliquet_mean:.2f}\n"
        f"Min: ${np.min(cliquet_payoffs):.2f}\n"
        f"Max: ${np.max(cliquet_payoffs):.2f}\n"
        f"Std Dev: ${np.std(cliquet_payoffs):.2f}"
    )
    
    plt.figtext(0.30, 0.5, vanilla_stats, bbox=dict(facecolor='white', alpha=1, edgecolor='blue'))
    plt.figtext(0.55, 0.5, cliquet_stats, bbox=dict(facecolor='white', alpha=1, edgecolor='green'))
    
    plt.tight_layout()
    plt.grid(True, alpha=0.3)
    plt.show()

def main():
    print("Running Monte Carlo simulation with", n_simulations, "paths...")
    paths = simulate_paths()
    
    vanilla_payoffs = calculate_vanilla_payoff(paths)
    cliquet_payoffs = calculate_cliquet_payoff(paths)
    
    print("\nSummary Statistics:")
    print("Vanilla Call Option:")
    print(f"  Mean: ${np.mean(vanilla_payoffs):.2f}")
    print(f"  Min: ${np.min(vanilla_payoffs):.2f}")
    print(f"  Max: ${np.max(vanilla_payoffs):.2f}")
    print(f"  Std Dev: ${np.std(vanilla_payoffs):.2f}")
    
    print("\nCliquet Option:")
    print(f"  Mean: ${np.mean(cliquet_payoffs):.2f}")
    print(f"  Min: ${np.min(cliquet_payoffs):.2f}")
    print(f"  Max: ${np.max(cliquet_payoffs):.2f}")
    print(f"  Std Dev: ${np.std(cliquet_payoffs):.2f}")
    
    plot_results(vanilla_payoffs, cliquet_payoffs)

if __name__ == "__main__":
    main()
