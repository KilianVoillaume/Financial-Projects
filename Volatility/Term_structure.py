import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

def generate_futures_data(days=365, start_date=None):
    if start_date is None:
        start_date = datetime(2024, 1, 1)
    
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    spot_price = 100
    spot_prices = [spot_price]
    
    # Randomness and trend
    for i in range(1, days):
        change = np.random.normal(0, 1.5)
        # Small upward trend
        trend = 0.02
        spot_price = max(spot_price + change + trend, 50)  # Min. Price
        spot_prices.append(spot_price)
    
    # Different expiration dates
    futures_data = pd.DataFrame({'Date': dates, 'Spot': spot_prices})
    
    for month in [1, 3, 6]:
        # For contango regime (first half of data)
        contango_prices = []
        for i in range(days//2):
            # Contango: futures price > spot price, premium increases with time to expiration
            premium = month * 2 * (1 + np.random.normal(0, 0.1))
            contango_prices.append(spot_prices[i] + premium)
        
        # For backwardation regime (second half of data)
        backwardation_prices = []
        for i in range(days//2, days):
            # Backwardation: futures price < spot price, discount increases with time to expiration
            discount = month * 1.5 * (1 + np.random.normal(0, 0.1))
            backwardation_prices.append(spot_prices[i] - discount)
        
        futures_data[f'Futures_{month}m'] = contango_prices + backwardation_prices
    
    # Volatility regimes:
    # Contango: Volatility lower
    # Backwardation: Volatility higher
    contango_vol = np.random.normal(10, 2, days//2)
    backwardation_vol = np.random.normal(20, 5, days//2)
    futures_data['Volatility'] = np.concatenate([contango_vol, backwardation_vol])
    
    futures_data['Regime'] = ['Contango'] * (days//2) + ['Backwardation'] * (days//2)
    
    return futures_data

data = generate_futures_data(364)

plt.figure(figsize=(14, 10))

# Futures Curves
plt.subplot(2, 1, 1)
plt.plot(data['Date'], data['Spot'], label='Spot Price', linewidth=2)
plt.plot(data['Date'], data['Futures_1m'], label='1-Month Futures', linestyle='--')
plt.plot(data['Date'], data['Futures_3m'], label='3-Month Futures', linestyle='-.')
plt.plot(data['Date'], data['Futures_6m'], label='6-Month Futures', linestyle=':')

# Highlighting regime change
regime_change_date = data['Date'][len(data)//2]
plt.axvline(x=regime_change_date, color='r', linestyle='-', alpha=0.3, label='Regime Change')

midpoint_contango = data['Date'][len(data)//4]
midpoint_backwardation = data['Date'][len(data)//4*3]
plt.text(midpoint_contango, max(data['Futures_6m'][:len(data)//2]), 'CONTANGO', 
         fontsize=12, ha='center', bbox=dict(facecolor='white', alpha=0.7))
plt.text(midpoint_backwardation, max(data['Futures_6m'][len(data)//2:]), 'BACKWARDATION', 
         fontsize=12, ha='center', bbox=dict(facecolor='white', alpha=0.7))

plt.title('Futures Curves: Contango vs Backwardation')
plt.ylabel('Price')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45)



# Volatility Regimes
plt.subplot(2, 1, 2)
plt.plot(data['Date'], data['Volatility'], label='Volatility', color='purple')

contango_dates = data['Date'][:len(data)//2]
backwardation_dates = data['Date'][len(data)//2:]
plt.fill_between(contango_dates, 0, max(data['Volatility'])*1.1, 
                color='green', alpha=0.2, label='Contango Regime')
plt.fill_between(backwardation_dates, 0, max(data['Volatility'])*1.1, 
                color='red', alpha=0.2, label='Backwardation Regime')

plt.axvline(x=regime_change_date, color='r', linestyle='-', alpha=0.3)

plt.text(midpoint_contango, np.mean(data['Volatility'][:len(data)//2]), 
         'Lower Volatility', fontsize=12, ha='center', va='center',
         bbox=dict(facecolor='white', alpha=0.7))
plt.text(midpoint_backwardation, np.mean(data['Volatility'][len(data)//2:]), 
         'Higher Volatility', fontsize=12, ha='center', va='center',
         bbox=dict(facecolor='white', alpha=0.7))

plt.title('Volatility Regimes: Contango vs Backwardation')
plt.ylabel('Volatility (%)')
plt.legend(loc='best')
plt.grid(True, alpha=0.3)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

contango_data = data[data['Regime'] == 'Contango']
backwardation_data = data[data['Regime'] == 'Backwardation']

# Statistics
print("Contango Regime Statistics:")
print(f"Average Volatility: {contango_data['Volatility'].mean():.2f}%")
print(f"Max Volatility: {contango_data['Volatility'].max():.2f}%")
print(f"Min Volatility: {contango_data['Volatility'].min():.2f}%")
print(f"Spot to 6-Month Futures Spread (Avg): {(contango_data['Futures_6m'] - contango_data['Spot']).mean():.2f}")
print("\nBackwardation Regime Statistics:")
print(f"Average Volatility: {backwardation_data['Volatility'].mean():.2f}%")
print(f"Max Volatility: {backwardation_data['Volatility'].max():.2f}%")
print(f"Min Volatility: {backwardation_data['Volatility'].min():.2f}%")
print(f"Spot to 6-Month Futures Spread (Avg): {(backwardation_data['Futures_6m'] - backwardation_data['Spot']).mean():.2f}")
