import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd

np.random.seed(42)

initial_price = 100
volatility = 0.2  
drift = 0.05      
periods = 5      
cap = 0.08        
floor = -0.03     
simulations = 1  

def simulate_asset_path(initial_price, drift, volatility, periods, steps_per_period=252):
    total_steps = periods * steps_per_period
    dt = 1 / steps_per_period
    Z = np.random.normal(0, 1, total_steps)
    daily_returns = np.exp((drift - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * Z)
    price_path = initial_price * np.cumprod(daily_returns)
    
    full_price_path = np.insert(price_path, 0, initial_price)
    return full_price_path

def calculate_cliquet_returns(price_path, periods, steps_per_period, cap, floor):
    reset_indices = [i * steps_per_period for i in range(periods + 1)]
    reset_prices = price_path[reset_indices]
    raw_returns = []
    capped_floored_returns = []
    
    for i in range(1, len(reset_prices)):
        period_return = (reset_prices[i] / reset_prices[i-1]) - 1
        raw_returns.append(period_return)
        capped_floored_return = min(max(period_return, floor), cap)
        capped_floored_returns.append(capped_floored_return)
    return raw_returns, capped_floored_returns

start_date = datetime(2025, 1, 1)
end_date = datetime(2030,1,1)
dates = pd.date_range(start=start_date, end=end_date, freq='AS')  # Annual Start frequency

days_per_period = 252  # Trading days per year
price_path = simulate_asset_path(initial_price, drift, volatility, periods, days_per_period)

raw_returns, capped_floored_returns = calculate_cliquet_returns(price_path, periods, days_per_period, cap, floor)
cum_raw_returns = np.cumprod(np.array(raw_returns) + 1) - 1
cum_capped_floored_returns = np.cumprod(np.array(capped_floored_returns) + 1) - 1

df = pd.DataFrame({
    'Date': dates[1:],
    'Raw Return': raw_returns,
    'Capped/Floored Return': capped_floored_returns,
    'Cumulative Raw Return': cum_raw_returns,
    'Cumulative Capped/Floored Return': cum_capped_floored_returns
})
print(df)

plt.figure(figsize=(14, 10))

plt.subplot(3, 1, 1)
reset_indices = [i * days_per_period for i in range(periods + 1)]
plt.plot(price_path, color='gray', alpha=0.7, linewidth=1)
plt.plot(reset_indices, price_path[reset_indices], 'ro', markersize=8)
plt.grid(True, alpha=0.3)
plt.title('Asset Price Path with Reset Points', fontsize=14)
plt.ylabel('Price', fontsize=12)

plt.subplot(3, 1, 2)
bar_width = 0.35
indices = np.arange(len(raw_returns))
plt.bar(indices - bar_width/2, raw_returns, bar_width, label='Raw Returns', alpha=0.7, color='blue')
plt.bar(indices + bar_width/2, capped_floored_returns, bar_width, label='Capped/Floored Returns', alpha=0.7, color='green')
plt.axhline(y=cap, color='r', linestyle='--', label=f'Cap ({cap*100}%)')
plt.axhline(y=floor, color='orange', linestyle='--', label=f'Floor ({floor*100}%)')
plt.grid(True, alpha=0.3)
plt.title('Period Returns: Raw vs Capped/Floored', fontsize=14)
plt.ylabel('Return', fontsize=12)
plt.xticks(indices, [date.strftime('%Y-%m-%d') for date in dates[1:]], rotation=45)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(cum_raw_returns, 'b-o', linewidth=2, label='Cumulative Raw Return')
plt.plot(cum_capped_floored_returns, 'g-o', linewidth=2, label='Cumulative Capped/Floored Return')
plt.grid(True, alpha=0.3)
plt.title('Cumulative Returns: Raw vs Capped/Floored', fontsize=14)
plt.ylabel('Cumulative Return', fontsize=12)
plt.xticks(range(len(dates[1:])), [date.strftime('%Y-%m-%d') for date in dates[1:]], rotation=45)
plt.legend()

plt.tight_layout()
plt.savefig('cliquet_option_simulation.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nFinal Payoffs:")
print(f"Raw Payoff: {cum_raw_returns[-1]*100:.2f}%")
print(f"Capped/Floored Payoff: {cum_capped_floored_returns[-1]*100:.2f}%")

impact = cum_capped_floored_returns[-1] - cum_raw_returns[-1]
if impact < 0:
    print(f"Impact of Caps/Floors: {impact*100:.2f}% (loss due to caps/floors)")
else:
    print(f"Impact of Caps/Floors: +{impact*100:.2f}% (gain due to caps/floors)")
