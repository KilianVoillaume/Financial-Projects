import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma, q=0):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma, q=0):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    return put_price

def plot_sensitivity(S, K, T, r, sigma, q=0):    
    fig, axes = plt.subplots(2, 2, figsize=(10, 9))  # 2x2 grid of subplots
    
    # Time to Maturity Sensitivity
    T_range = np.linspace(0.1, 2, 50)
    prices_T_call = [black_scholes_call(S, K, t, r, sigma, q) for t in T_range]
    prices_T_put = [black_scholes_put(S, K, t, r, sigma, q) for t in T_range]
    axes[0, 0].plot(T_range, prices_T_call, label=r'$\bf{Call\ Option\ Price}$', color='blue')
    axes[0, 0].plot(T_range, prices_T_put, label=r'$\bf{Put\ Option\ Price}$', linestyle='dashed', color='red')
    axes[0, 0].set_xlabel(r'$\bf{Time\ to\ Maturity\ (Years)}$', fontsize=11)
    axes[0, 0].set_ylabel(r'$\bf{Option\ Price}$', fontsize=11)
    axes[0, 0].set_title(r'$\bf{Impact\ of\ Time\ to\ Maturity}$', fontsize=13)
    axes[0, 0].legend(fontsize=11, loc='best', frameon=True)
    axes[0, 0].grid()

    # Volatility Sensitivity
    sigma_range = np.linspace(0.1, 0.5, 50)
    prices_sigma_call = [black_scholes_call(S, K, T, r, s, q) for s in sigma_range]
    prices_sigma_put = [black_scholes_put(S, K, T, r, s, q) for s in sigma_range]
    axes[1, 0].plot(sigma_range, prices_sigma_call, label=r'$\bf{Call\ Option\ Price}$', color='blue')
    axes[1, 0].plot(sigma_range, prices_sigma_put, label=r'$\bf{Put\ Option\ Price}$', linestyle='dashed', color='red')
    axes[1, 0].set_xlabel(r'$\bf{Volatility}$', fontsize=11)
    axes[1, 0].set_ylabel(r'$\bf{Option\ Price}$', fontsize=11)
    axes[1, 0].set_title(r'$\bf{Impact\ of\ Volatility}$', fontsize=13)
    axes[1, 0].legend(fontsize=11, loc='best', frameon=True)
    axes[1, 0].grid()

    # Risk-free Rate Sensitivity
    r_range = np.linspace(0.01, 0.1, 50)
    prices_r_call = [black_scholes_call(S, K, T, rate, sigma, q) for rate in r_range]
    prices_r_put = [black_scholes_put(S, K, T, rate, sigma, q) for rate in r_range]
    axes[0, 1].plot(r_range, prices_r_call, label=r'$\bf{Call\ Option\ Price}$', color='blue')
    axes[0, 1].plot(r_range, prices_r_put, label=r'$\bf{Put\ Option\ Price}$', linestyle='dashed', color='red')
    axes[0, 1].set_xlabel(r'$\bf{Risk-free\ Rate}$', fontsize=11)
    axes[0, 1].set_ylabel(r'$\bf{Option\ Price}$', fontsize=11)
    axes[0, 1].set_title(r'$\bf{Impact\ of\ Risk-free\ Rate}$', fontsize=13)
    axes[0, 1].legend(fontsize=11, loc='best', frameon=True)
    axes[0, 1].grid()

    # Dividend Yield Sensitivity
    q_range = np.linspace(0.0, 0.06, 50)
    prices_q_call = [black_scholes_call(S, K, T, r, sigma, dividend) for dividend in q_range]
    prices_q_put = [black_scholes_put(S, K, T, r, sigma, dividend) for dividend in q_range]
    axes[1, 1].plot(q_range, prices_q_call, label=r'$\bf{Call\ Option\ Price}$', color='blue')
    axes[1, 1].plot(q_range, prices_q_put, label=r'$\bf{Put\ Option\ Price}$', linestyle='dashed', color='red')
    axes[1, 1].set_xlabel(r'$\bf{Dividend\ Yield}$', fontsize=11)
    axes[1, 1].set_ylabel(r'$\bf{Option\ Price}$', fontsize=11)
    axes[1, 1].set_title(r'$\bf{Impact\ of\ Dividend\ Yield}$', fontsize=13)
    axes[1, 1].legend(fontsize=11, loc='best', frameon=True)
    axes[1, 1].grid()

    plt.tight_layout()  # Adjusts spacing to prevent overlap
    plt.show()

S = 100         
K = 100        
T = 5          
r = 0.05        
sigma = 0.2    
q = 0.03     

plot_sensitivity(S, K, T, r, sigma, q)
