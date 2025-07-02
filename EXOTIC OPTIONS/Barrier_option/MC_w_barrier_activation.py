import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap

def simulate_asset_paths(S0, mu, sigma, T, dt, num_paths):
    num_steps = int(T / dt)
    
    Z = np.random.normal(0, 1, size=(num_paths, num_steps))
    
    paths = np.zeros((num_paths, num_steps + 1))
    paths[:, 0] = S0
    
    for t in range(1, num_steps + 1):
        paths[:, t] = paths[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t-1])
    
    return paths

def check_barrier_condition(paths, barrier_level, barrier_type='knock_in'):
    if barrier_type == 'knock_in':
        # Check if path ever goes below barrier
        triggered = np.any(paths <= barrier_level, axis=1)
    else:  # knock_out
        # Check if path ever goes below barrier
        triggered = np.any(paths <= barrier_level, axis=1)
    return triggered

def plot_paths_with_barrier(paths, time_points, barrier_level, triggered, barrier_type):
    plt.figure(figsize=(12, 8))
    
    for i in range(len(paths)):
        if not triggered[i]:
            plt.plot(time_points, paths[i], color='green', alpha=0.3)
    
    for i in range(len(paths)):
        if triggered[i]:
            plt.plot(time_points, paths[i], color='red', alpha=0.3)
    
    plt.axhline(y=barrier_level, color='black', linestyle='--', linewidth=2, label=f'Barrier Level ({barrier_level})')
    
    triggered_count = np.sum(triggered)
    untriggered_count = len(paths) - triggered_count
    
    valid_label = f'Valid Paths (Barrier Untouched): {untriggered_count}'
    invalid_label = f'{"Knocked In" if barrier_type == "knock_in" else "Knocked Out"} Paths (Barrier Touched): {triggered_count}'
    
    plt.plot([], [], color='green', alpha=0.7, label=valid_label)
    plt.plot([], [], color='red', alpha=0.7, label=invalid_label)
    
    barrier_text = "Knock-In" if barrier_type == "knock_in" else "Knock-Out"
    plt.title(f'Monte Carlo Path Simulation with {barrier_text} Barrier', fontsize=16)
    plt.xlabel('Time (Years)', fontsize=12)
    plt.ylabel('Asset Price', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt

def main():
    S0 = 100        
    mu = 0.05         
    sigma = 0.2    
    T = 1.0         
    dt = 0.01        
    num_paths = 500   
    
    barrier_level = 80
    barrier_type = 'knock_in'  # 'knock_in' or 'knock_out'
    
    paths = simulate_asset_paths(S0, mu, sigma, T, dt, num_paths)
    
    num_steps = int(T / dt)
    time_points = np.linspace(0, T, num_steps + 1)
    
    triggered = check_barrier_condition(paths, barrier_level, barrier_type)
    
    plt = plot_paths_with_barrier(paths, time_points, barrier_level, triggered, barrier_type)
    
    print(f"Total paths: {num_paths}")
    print(f"Paths that {'knocked in' if barrier_type == 'knock_in' else 'knocked out'}: {np.sum(triggered)}")
    print(f"Percentage: {np.sum(triggered) / num_paths * 100:.2f}%")
    
    plt.show()

if __name__ == "__main__":
    main()
