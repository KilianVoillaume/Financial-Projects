import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from numpy import log, sqrt, exp

def calculate_black_scholes(time_to_maturity, strike, current_price, volatility, interest_rate, dividend_yield=0):
    d1 = (
        log(current_price / strike)
        + (interest_rate - dividend_yield + 0.5 * volatility ** 2) * time_to_maturity
    ) / (volatility * sqrt(time_to_maturity))
    d2 = d1 - volatility * sqrt(time_to_maturity)

    call_price = current_price * exp(-dividend_yield * time_to_maturity) * norm.cdf(d1) - (
        strike * exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
    )
    put_price = (
        strike * exp(-interest_rate * time_to_maturity) * norm.cdf(-d2)
    ) - current_price * exp(-dividend_yield * time_to_maturity) * norm.cdf(-d1)
    
    return call_price, put_price

def calculate_prices_matrix(param_range, param_name, fixed_params, spot_range):
    call_prices = np.zeros((len(param_range), len(spot_range)))
    put_prices = np.zeros((len(param_range), len(spot_range)))
    
    for i, param in enumerate(param_range):
        for j, spot in enumerate(spot_range):
            # Update only the parameter being varied
            time_to_maturity = param if param_name == 'Time to maturity' else fixed_params['Time to maturity']
            volatility = param if param_name == 'Volatility' else fixed_params['Volatility']
            interest_rate = param if param_name == 'Interest rate' else fixed_params['Interest rate']
            dividend_yield = param if param_name == 'Dividend yield' else fixed_params['Dividend yield']
            
            call_price, put_price = calculate_black_scholes(
                time_to_maturity=time_to_maturity,
                strike=fixed_params['strike'],
                current_price=spot,
                volatility=volatility,
                interest_rate=interest_rate,
                dividend_yield=dividend_yield
            )
            
            call_prices[i, j] = call_price
            put_prices[i, j] = put_price
    
    return call_prices, put_prices

def plot_all_heatmaps():
    # Fixed parameters
    fixed_params = {
        'Time to maturity': 5,
        'strike': 100,
        'current_price': 100,
        'Volatility': 0.2,
        'Interest rate': 0.05,
        'Dividend yield': 0.02
    }

    # Parameter ranges
    time_range = np.linspace(0.1, 2, 10)
    vol_range = np.linspace(0.1, 0.5, 10)
    rate_range = np.linspace(0.01, 0.1, 10)
    dividend_range = np.linspace(0, 0.05, 10)
    spot_range = np.linspace(80, 120, 10)

    param_ranges = [
        (time_range, 'Time to maturity'),
        (vol_range, 'Volatility'),
        (rate_range, 'Interest rate'),
        (dividend_range, 'Dividend yield')
    ]

    fig_call, axes_call = plt.subplots(2, 2, figsize=(13, 10))
    fig_put, axes_put = plt.subplots(2, 2, figsize=(13, 10))
    
    axes_call = axes_call.flatten()
    axes_put = axes_put.flatten()
    
    fig_call.suptitle('Call Option Price Heatmaps', fontsize=16)
    fig_put.suptitle('Put Option Price Heatmaps', fontsize=16)

    for idx, (param_range, param_name) in enumerate(param_ranges):
        call_prices, put_prices = calculate_prices_matrix(param_range, param_name, fixed_params, spot_range)
        
        # Call heatmap
        sns.heatmap(call_prices, 
                   xticklabels=np.round(spot_range, 2), 
                   yticklabels=np.round(param_range, 2), 
                   annot=True, fmt=".2f", cmap="viridis", 
                   ax=axes_call[idx])
        axes_call[idx].set_title(f"Impact of {param_name}")
        axes_call[idx].set_xlabel("Spot Price")
        axes_call[idx].set_ylabel(param_name)
        
        # Put heatmap
        sns.heatmap(put_prices, 
                   xticklabels=np.round(spot_range, 2), 
                   yticklabels=np.round(param_range, 2), 
                   annot=True, fmt=".2f", cmap="viridis", 
                   ax=axes_put[idx])
        axes_put[idx].set_title(f"Impact of {param_name}")
        axes_put[idx].set_xlabel("Spot Price")
        axes_put[idx].set_ylabel(param_name)
    
    plt.tight_layout()
    plt.show()

plot_all_heatmaps()
