import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from matplotlib.ticker import FuncFormatter

np.random.seed(42)

mid_price = 100.0
spread = 0.10  # narrow spread

price_levels_buy = np.arange(mid_price - spread/2 - 1.0, mid_price - spread/2 - 4.0, -0.2)
price_levels_sell = np.arange(mid_price + spread/2, mid_price + spread/2 + 4.0, 0.2)

volumes_buy = np.concatenate([
    [50],  # Small volume at the best bid (shallow)
    np.random.normal(500, 100, len(price_levels_buy) - 1)  # Deeper away from the spread
])
volumes_sell = np.concatenate([
    [60],  # Small volume at the best ask (shallow)
    np.random.normal(450, 100, len(price_levels_sell) - 1)  # Deeper away from the spread
])

# Hidden liquidity (iceberg orders and dark pool liquidity)
hidden_volumes_buy = volumes_buy * 0.6  # 60% additional liquidity hidden
hidden_volumes_sell = volumes_sell * 0.5  # 50% additional liquidity hidden

cum_volumes_buy = np.cumsum(volumes_buy)
cum_volumes_sell = np.cumsum(volumes_sell)
cum_total_buy = np.cumsum(volumes_buy + hidden_volumes_buy)
cum_total_sell = np.cumsum(volumes_sell + hidden_volumes_sell)

plt.figure(figsize=(14, 8))
plt.grid(True, alpha=0.3)

visible_buy_color = '#1f77b4'  # blue
hidden_buy_color = '#94c5eb'   # light blue
visible_sell_color = '#d62728'  # red
hidden_sell_color = '#f2a5a8'   # light red

plt.fill_between(price_levels_buy, cum_volumes_buy, color=visible_buy_color, alpha=0.7, 
                 label='Visible Bid Liquidity', step='post')

plt.fill_between(price_levels_buy, cum_volumes_buy, cum_total_buy, color=hidden_buy_color, 
                 alpha=0.7, label='Hidden Bid Liquidity', step='post')

plt.fill_between(price_levels_sell, cum_volumes_sell, color=visible_sell_color, alpha=0.7, 
                 label='Visible Ask Liquidity', step='post')

plt.fill_between(price_levels_sell, cum_volumes_sell, cum_total_sell, color=hidden_sell_color, 
                 alpha=0.7, label='Hidden Ask Liquidity', step='post')

plt.axvline(x=mid_price - spread/2, color='black', linestyle='--', alpha=0.7)
plt.axvline(x=mid_price + spread/2, color='black', linestyle='--', alpha=0.7)
plt.axvspan(mid_price - spread/2, mid_price + spread/2, alpha=0.1, color='gray')

plt.text(mid_price, np.max(cum_total_sell) * 0.8, f'Spread: {spread:.2f}', 
         ha='center', va='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.7))

plt.annotate('Shallow Depth\n(Low Visible Liquidity)', 
             xy=(price_levels_buy[0], volumes_buy[0] / 2),
             xytext=(price_levels_buy[0] - 1.5, volumes_buy[0] * 2),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=10, ha='center')

plt.annotate('Shallow Depth\n(Low Visible Liquidity)', 
             xy=(price_levels_sell[0], volumes_sell[0] / 2),
             xytext=(price_levels_sell[0] + 1.5, volumes_sell[0] * 2),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=10, ha='center')

plt.annotate('Hidden Iceberg Orders', 
             xy=(price_levels_buy[1], (cum_volumes_buy[1] + cum_total_buy[1]) / 2),
             xytext=(price_levels_buy[1] - 1.2, cum_volumes_buy[1] + 300),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=10, ha='center')

plt.annotate('Hidden Iceberg Orders', 
             xy=(price_levels_sell[2], (cum_volumes_sell[2] + cum_total_sell[2]) / 2),
             xytext=(price_levels_sell[2] + 1.2, cum_volumes_sell[2] + 300),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=10, ha='center')

def thousands_formatter(x, pos):
    return f'{int(x/1000)}K'

plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

rect = patches.Rectangle((mid_price - spread/2, 0), spread, np.max(cum_total_sell) * 0.1, 
                        linewidth=2, edgecolor='black', facecolor='yellow', alpha=0.3)
plt.gca().add_patch(rect)

plt.annotate('Narrow Spread', 
             xy=(mid_price, np.max(cum_total_sell) * 0.05),
             xytext=(mid_price, np.max(cum_total_sell) * 0.2),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=10, ha='center')

plt.xlabel('Price', fontsize=14)
plt.ylabel('Cumulative Volume', fontsize=14)
plt.title('Order Book Depth Chart: Visible vs Hidden Liquidity', fontsize=16)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=4)

best_bid = mid_price - spread/2
best_ask = mid_price + spread/2
plt.figtext(0.5, -0.05, 
            f"Best Bid: ${best_bid:.2f} | Best Ask: ${best_ask:.2f} | Mid Price: ${mid_price:.2f}", 
            ha="center", fontsize=12, bbox={"facecolor":"lightgray", "alpha":0.5, "pad":5})

plt.figtext(0.5, -0.10, 
            "Note: Narrow spread can mask shallow market depth, giving false impression of good liquidity", 
            ha="center", fontsize=10, style='italic')

explanation_text = """Why It Matters:
- Spread is just one dimension of liquidity
- Shallow depth means large orders can move the market significantly
- Hidden liquidity may fill some gaps but is not guaranteed
- Market impact costs can be much higher than the spread suggests"""

plt.figtext(0.15, 0.7, explanation_text, fontsize=12, 
            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

plt.tight_layout()
plt.subplots_adjust(bottom=0.2)
plt.show()

# Function to simulate a large market order to demonstrate market impact
def simulate_market_impact(price_levels, volumes, order_size, side='buy'):
    remaining = order_size
    executed_prices = []
    executed_volumes = []
    
    for price, volume in zip(price_levels, volumes):
        if remaining <= 0:
            break      
        execute = min(volume, remaining)
        executed_prices.append(price)
        executed_volumes.append(execute)
        remaining -= execute
    
    if remaining > 0:
        print(f"Warning: Could not fill entire order. {remaining} units unfilled.")
    if len(executed_volumes) > 0:
        average_price = np.sum(np.array(executed_prices) * np.array(executed_volumes)) / np.sum(executed_volumes)
        if side == 'buy':
            market_impact = average_price - price_levels[0]
        else:
            market_impact = price_levels[0] - average_price
            
        return executed_prices, executed_volumes, average_price, market_impact
    else:
        return [], [], None, None

# Simulating market impact
large_buy_order = 800
executed_prices, executed_volumes, avg_price, impact = simulate_market_impact(
    price_levels_sell, volumes_sell, large_buy_order, side='buy')

if avg_price and impact:
    print(f"\nMarket Impact Simulation for {large_buy_order} unit Buy Order:")
    print(f"Best Ask: ${price_levels_sell[0]:.2f}")
    print(f"Average Execution Price: ${avg_price:.2f}")
    print(f"Market Impact: ${impact:.2f} ({impact/price_levels_sell[0]*100:.2f}% of price)")
    print(f"Total Cost of Spread + Impact: ${(impact + spread):.2f}")
    
    plt.figure(figsize=(12, 6))
    plt.bar(range(len(executed_prices)), executed_prices, width=0.4, alpha=0.7, color='red')
    plt.axhline(y=price_levels_sell[0], color='green', linestyle='-', label=f'Best Ask: ${price_levels_sell[0]:.2f}')
    plt.axhline(y=avg_price, color='red', linestyle='--', label=f'Avg Execution: ${avg_price:.2f}')
    plt.xlabel('Order Execution Sequence')
    plt.ylabel('Price')
    plt.title(f'Market Impact of {large_buy_order} Unit Buy Order')
    plt.legend()
    
    impact_text = f"""Market Impact Analysis:
    - Order Size: {large_buy_order} units
    - Best Ask: ${price_levels_sell[0]:.2f}
    - Average Execution: ${avg_price:.2f}
    - Price Impact: ${impact:.2f} ({impact/price_levels_sell[0]*100:.2f}%)
    - Spread + Impact Cost: ${(impact + spread):.2f}"""
    
    plt.figtext(0.6, 0.15, impact_text, fontsize=12, 
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))
    
    plt.tight_layout()
    plt.show()
