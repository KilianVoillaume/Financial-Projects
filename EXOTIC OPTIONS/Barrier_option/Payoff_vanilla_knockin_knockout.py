import numpy as np
import matplotlib.pyplot as plt

strike = 100  
barrier = 80 
premium = 5


def plot_option_payoffs(min_price=75):
    spot_prices = np.linspace(40, 160, 1000)
    
    vanilla_payoffs = np.maximum(spot_prices - strike, 0) - premium
    
    barrier_triggered = min_price <= barrier
    if barrier_triggered:
        knock_in_payoffs = np.maximum(spot_prices - strike, 0) - premium
    else:
        knock_in_payoffs = np.zeros_like(spot_prices) - premium
    
    if barrier_triggered:
        knock_out_payoffs = np.zeros_like(spot_prices) - premium
    else:
        knock_out_payoffs = np.maximum(spot_prices - strike, 0) - premium
    
    plt.figure(figsize=(12, 8))
    
    plt.plot(spot_prices, vanilla_payoffs, 'b-', label='Vanilla Call', linewidth=2)
    plt.plot(spot_prices, knock_in_payoffs, 'g--', label='Down-and-In Call', linewidth=2)
    plt.plot(spot_prices, knock_out_payoffs, 'r:', label='Down-and-Out Call', linewidth=2)
    
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    plt.axvline(x=strike, color='k', linestyle='--', alpha=0.3, label='Strike Price')
    plt.axvline(x=barrier, color='k', linestyle=':', alpha=0.3, label='Barrier Level')
    
    plt.title(f'Option Payoff Comparison (Barrier {"Triggered" if barrier_triggered else "Not Triggered"})', fontsize=16)
    plt.xlabel('Spot Price at Expiry', fontsize=14)
    plt.ylabel('Option Payoff', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    # Display whether barrier was triggered during the option's life
    barrier_status = f"Minimum price during option life: {min_price} (Barrier {'triggered' if barrier_triggered else 'not triggered'})"
    plt.figtext(0.5, 0.01, barrier_status, ha='center', fontsize=12, bbox={'facecolor':'orange', 'alpha':0.1, 'pad':5})
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()

print("Scenario 1: Barrier was triggered (minimum price went below barrier)")
plot_option_payoffs(min_price=75)  # Barrier triggered

print("\nScenario 2: Barrier was NOT triggered (minimum price stayed above barrier)")
plot_option_payoffs(min_price=85)  # Barrier not triggered

from ipywidgets import interact, FloatSlider
import ipywidgets as widgets

def plot_interactive_payoffs(min_price=85):
    plot_option_payoffs(min_price)

