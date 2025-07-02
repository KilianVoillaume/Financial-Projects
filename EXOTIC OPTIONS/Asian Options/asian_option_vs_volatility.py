import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.style as style

S0 = 100  
K = 100   
r = 0.05 
T = 1.0 
n_steps = 252  
n_simulations = 10000 
volatility_range = np.linspace(0.1, 0.5, 10)  # Range of volatilities to test

def black_scholes_call(S, K, r, sigma, T):
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def simulate_price_path(S0, r, sigma, T, n_steps):
    dt = T / n_steps
    prices = np.zeros(n_steps + 1)
    prices[0] = S0    
    for i in range(1, n_steps + 1):
        z = np.random.standard_normal()
        prices[i] = prices[i-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)   
    return prices

def price_asian_call(S0, K, r, sigma, T, n_steps, n_simulations):
    option_values = np.zeros(n_simulations)   
    for i in range(n_simulations):
        prices = simulate_price_path(S0, r, sigma, T, n_steps)
        avg_price = np.mean(prices)
        option_values[i] = max(0, avg_price - K)    
    option_price = np.exp(-r * T) * np.mean(option_values)
    return option_price

vanilla_prices = []
asian_prices = []

for sigma in volatility_range:
    vanilla_price = black_scholes_call(S0, K, r, sigma, T)
    vanilla_prices.append(vanilla_price)
    
    asian_price = price_asian_call(S0, K, r, sigma, T, n_steps, n_simulations)
    asian_prices.append(asian_price)
    
    print(f"Volatility: {sigma:.2f}, Vanilla: {vanilla_price:.4f}, Asian: {asian_price:.4f}")

vanilla_vega = np.diff(vanilla_prices) / np.diff(volatility_range)
asian_vega = np.diff(asian_prices) / np.diff(volatility_range)

style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(12, 10))

plt.subplot(2, 1, 1)
plt.plot(volatility_range, vanilla_prices, 'b-', linewidth=2.5, label='Vanilla Call')
plt.plot(volatility_range, asian_prices, 'r-', linewidth=2.5, label='Asian Call')
plt.xlabel('Implied Volatility (σ)', fontsize=12)
plt.ylabel('Option Price', fontsize=12)
plt.title('Option Value vs Volatility: Asian vs Vanilla Call', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)

plt.subplot(2, 1, 2)
mid_points = (volatility_range[:-1] + volatility_range[1:]) / 2
plt.plot(mid_points, vanilla_vega, 'b--', linewidth=2.5, label='Vanilla Call Vega')
plt.plot(mid_points, asian_vega, 'r--', linewidth=2.5, label='Asian Call Vega')
plt.xlabel('Implied Volatility (σ)', fontsize=12)
plt.ylabel('Vega (∂Price/∂σ)', fontsize=12)
plt.title('Option Sensitivity to Volatility (Vega)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)

plt.tight_layout()
plt.show()

vega_ratio = np.mean(asian_vega / vanilla_vega)
print(f"\nOn average, the Asian option's Vega is {vega_ratio:.2f} times that of the Vanilla option")
print(f"This demonstrates that Asian options are less sensitive to volatility changes")
