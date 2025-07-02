import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.ticker as mticker

np.random.seed(42)

def digital_option_price(S, K, T, r, sigma):
    if T <= 0:
        return 1.0 if S > K else 0.0
    d2 = (np.log(S/K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return np.exp(-r * T) * norm.cdf(d2)

def digital_option_delta(S, K, T, r, sigma):
    if T <= 0 or T < 1e-10:  
        return 0  
    d2 = (np.log(S/K) + (r - 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return np.exp(-r * T) * norm.pdf(d2) / (S * sigma * np.sqrt(T))

K = 100 
r = 0.05  
sigma = 0.2  

time_scenarios = [30, 7, 1, 0.5, 0.1]  # Days to maturity

spot_prices = np.linspace(95, 105, 1000)

plt.figure(figsize=(12, 8))

for days in time_scenarios:
    T = days / 365  # Convert days to years
    deltas = [digital_option_delta(S, K, T, r, sigma) for S in spot_prices]
    plt.plot(spot_prices, deltas, label=f'{days} days to maturity')

plt.axvline(x=K, color='gray', linestyle='--', alpha=0.7)

plt.xlabel('Spot Price', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.title('Digital Option Delta vs Spot Price as Maturity Approaches', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)

def simulate_digital_option_hedging(S0, K, T_days, r, sigma, num_simulations=1):
    T = T_days / 365
    
    remaining_days = np.linspace(T_days, 0, 50)
    time_points = remaining_days / 365
    
    spot_paths = []
    delta_paths = []
    price_paths = []
    
    for sim in range(num_simulations):
        S = S0
        spot_path = [S]
        delta_path = [digital_option_delta(S, K, T, r, sigma)]
        price_path = [digital_option_price(S, K, T, r, sigma)]
        
        for i in range(1, len(time_points)):
            dt = time_points[i-1] - time_points[i]
            dW = np.random.normal(0, np.sqrt(dt))
            S = S * np.exp((r - 0.5 * sigma**2) * dt + sigma * dW)
            spot_path.append(S)
            
            t_remaining = time_points[i]
            if t_remaining <= 0:
                delta = 0  # Delta is undefined at maturity
                price = 1.0 if S > K else 0.0
            else:
                delta = digital_option_delta(S, K, t_remaining, r, sigma)
                price = digital_option_price(S, K, t_remaining, r, sigma)
            
            delta_path.append(delta)
            price_path.append(price)
        
        spot_paths.append(spot_path)
        delta_paths.append(delta_path)
        price_paths.append(price_path)
    
    return remaining_days, spot_paths, delta_paths, price_paths

plt.figure(figsize=(12, 10))

days_remaining, spot_paths, delta_paths, price_paths = simulate_digital_option_hedging(
    S0=99.5, K=100, T_days=30, r=r, sigma=sigma, num_simulations=3
)

plt.subplot(3, 1, 1)
for i in range(len(spot_paths)):
    plt.plot(days_remaining, spot_paths[i], label=f'Simulation {i+1}')
plt.axhline(y=K, color='red', linestyle='--', alpha=0.7, label='Strike')
plt.xlabel('Days to Maturity')
plt.ylabel('Spot Price')
plt.title('Spot Price Path')
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(3, 1, 2)
for i in range(len(delta_paths)):
    plt.plot(days_remaining, delta_paths[i], label=f'Simulation {i+1}')
plt.xlabel('Days to Maturity')
plt.ylabel('Delta')
plt.title('Digital Option Delta Over Time')
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(3, 1, 3)
for i in range(len(price_paths)):
    plt.plot(days_remaining, price_paths[i], label=f'Simulation {i+1}')
plt.xlabel('Days to Maturity')
plt.ylabel('Option Price')
plt.title('Digital Option Price Over Time')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

plt.figure(figsize=(12, 6))

T_tiny = 0.5 / 365  # Half a day to maturity
very_fine_spots = np.linspace(99.5, 100.5, 1000)  # Very narrow range around strike

deltas_tiny = [digital_option_delta(S, K, T_tiny, r, sigma) for S in very_fine_spots]

plt.plot(very_fine_spots, deltas_tiny)
plt.axvline(x=K, color='red', linestyle='--', alpha=0.7, label='Strike')

S1 = 99.95
S2 = 100.05
delta1 = digital_option_delta(S1, K, T_tiny, r, sigma)
delta2 = digital_option_delta(S2, K, T_tiny, r, sigma)

plt.scatter([S1, S2], [delta1, delta2], color='red', s=50)
plt.annotate(f'S={S1}, Δ={delta1:.2f}', (S1, delta1), textcoords="offset points", 
             xytext=(-70,-30), ha='center', arrowprops=dict(arrowstyle="->"))
plt.annotate(f'S={S2}, Δ={delta2:.2f}', (S2, delta2), textcoords="offset points", 
             xytext=(70,-30), ha='center', arrowprops=dict(arrowstyle="->"))

delta_diff = abs(delta2 - delta1)
price_diff = abs(S2 - S1)
plt.annotate(f'Spot change: {price_diff:.2f} (0.1%)\nDelta change: {delta_diff:.2f}', 
             (K, max(deltas_tiny)/2), textcoords="offset points", 
             xytext=(10, 30), ha='left', bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.5))

plt.xlabel('Spot Price')
plt.ylabel('Delta')
plt.title(f'Digital Option Delta Near Strike (T = {T_tiny*365:.1f} days)')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout(rect=[0, 0.07, 1, 0.95])

plt.show()

