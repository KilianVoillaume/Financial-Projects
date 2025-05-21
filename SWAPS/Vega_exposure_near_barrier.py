import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def black_scholes_vega(S, K, T, r, sigma, barrier=None, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2)) * T
    d1 /= (sigma * np.sqrt(T))
    
    vega = S * np.sqrt(T) * norm.pdf(d1)
    
    # Simple barrier effect approximation - vega increases near barrier
    if barrier is not None:
        distance_to_barrier = np.abs(S - barrier) / barrier
        barrier_effect = 0.2 / (distance_to_barrier + 0.05)  # Scaling factor
        vega *= (1 + barrier_effect)
    return vega

def black_scholes_gamma(S, K, T, r, sigma, barrier=None, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2)) * T
    d1 /= (sigma * np.sqrt(T))
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    # Simple barrier effect approximation
    if barrier is not None:
        distance_to_barrier = np.abs(S - barrier) / barrier
        barrier_effect = 0.1 / (distance_to_barrier + 0.05)  # Smaller effect than vega
        gamma *= (1 + barrier_effect)
    return gamma

K = 100  
barrier = 110  
T = 0.5  
r = 0.03  
sigma = 0.2  

S = np.linspace(70, 130, 500)

vegas = [black_scholes_vega(s, K, T, r, sigma, barrier) for s in S]
gammas = [black_scholes_gamma(s, K, T, r, sigma, barrier) for s in S]

vegas = vegas / np.max(vegas)
gammas = gammas / np.max(gammas)

plt.figure(figsize=(10, 6))
plt.plot(S, vegas, label='Vega Exposure', color='blue', linewidth=2)
plt.plot(S, gammas, label='Gamma Exposure', color='green', linestyle='--', linewidth=2)
plt.axvline(x=barrier, color='red', linestyle=':', label='Barrier Level')

plt.axvspan(barrier-5, barrier+5, color='red', alpha=0.1, label='Barrier Zone')

plt.title('Vega and Gamma Exposure Near a Barrier', fontsize=14)
plt.xlabel('Underlying Price', fontsize=12)
plt.ylabel('Normalized Exposure', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
