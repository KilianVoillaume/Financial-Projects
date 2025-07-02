import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

def market_impact_model(trade_size, market_depth=1000, alpha=1.5):
    return (trade_size / market_depth) ** alpha * 100  # Convert to percentage

trade_sizes = np.linspace(0, 1000, 100)

low_liquidity_impact = market_impact_model(trade_sizes, market_depth=500, alpha=1.5)
medium_liquidity_impact = market_impact_model(trade_sizes, market_depth=1000, alpha=1.5)
high_liquidity_impact = market_impact_model(trade_sizes, market_depth=2000, alpha=1.5)

plt.figure(figsize=(12, 8))

plt.style.use('seaborn-v0_8-whitegrid')
colors = ['#E63946', '#F4A261', '#2A9D8F']

plt.plot(trade_sizes, low_liquidity_impact, color=colors[0], linewidth=3, label='Low Liquidity')
plt.plot(trade_sizes, medium_liquidity_impact, color=colors[1], linewidth=3, label='Medium Liquidity')
plt.plot(trade_sizes, high_liquidity_impact, color=colors[2], linewidth=3, label='High Liquidity')

reference_sizes = [200, 500, 800]
markers = ['o', 's', 'd']

for i, size in enumerate(reference_sizes):
    idx = np.where(trade_sizes >= size)[0][0]
    plt.scatter(size, low_liquidity_impact[idx], color=colors[0], s=100, marker=markers[i], zorder=5)
    plt.scatter(size, medium_liquidity_impact[idx], color=colors[1], s=100, marker=markers[i], zorder=5)
    plt.scatter(size, high_liquidity_impact[idx], color=colors[2], s=100, marker=markers[i], zorder=5)

for size in reference_sizes:
    plt.axvline(x=size, linestyle='--', color='gray', alpha=0.5)

linear_impact = market_impact_model(trade_sizes, market_depth=1000, alpha=1.0)
plt.plot(trade_sizes, linear_impact, color='gray', linestyle='--', alpha=0.7, label='Linear (Theoretical)')

plt.annotate('Disproportionate\nimpact for large trades', 
             xy=(800, market_impact_model(800, 500, 1.5)), 
             xytext=(650, market_impact_model(800, 500, 1.5) + 2),
             arrowprops=dict(arrowstyle='->', color='black'))

plt.annotate('Small trades have\nminimal impact', 
             xy=(150, market_impact_model(150, 1000, 1.5)), 
             xytext=(50, market_impact_model(150, 1000, 1.5) - 3),
             arrowprops=dict(arrowstyle='->', color='black'))

key_points = pd.DataFrame({
    'Trade Size': reference_sizes,
    'Low Liquidity Impact (%)': [round(market_impact_model(size, 500, 1.5), 2) for size in reference_sizes],
    'Medium Liquidity Impact (%)': [round(market_impact_model(size, 1000, 1.5), 2) for size in reference_sizes],
    'High Liquidity Impact (%)': [round(market_impact_model(size, 2000, 1.5), 2) for size in reference_sizes]
})

plt.table(cellText=key_points.values.round(2),
          colLabels=key_points.columns,
          loc='bottom',
          bbox=[0.0, -0.35, 1.0, 0.2])

plt.title('Market Impact vs Trade Size', fontsize=18, fontweight='bold')
plt.xlabel('Trade Size (Units)', fontsize=14)
plt.ylabel('Price Impact (%)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}%'))
plt.legend(fontsize=12, title='Market Liquidity Conditions')
plt.tight_layout()
plt.subplots_adjust(bottom=0.3)  # Make room for the table
# Add implications for L-VaR
plt.figtext(0.5, -0.05, 
           "Implications for L-VaR: The convex market impact means that L-VaR increases non-linearly with position size.\n"
           "Large positions face significantly higher liquidation costs, potentially underestimated by standard VaR models.",
           ha='center', fontsize=12, bbox=dict(boxstyle='round,pad=1', facecolor='#f0f0f0', alpha=0.5))

plt.savefig('market_impact_vs_trade_size.png', dpi=300, bbox_inches='tight')
plt.show()

def l_var_adjustment(position_size, market_depth=1000, confidence_level=0.95, volatility=0.02, time_horizon=1):
    import scipy.stats as stats
    z_score = stats.norm.ppf(confidence_level)
    standard_var = position_size * volatility * np.sqrt(time_horizon) * z_score
    impact_factor = 1 + market_impact_model(position_size, market_depth, alpha=1.5) / 100
    l_var = standard_var * impact_factor
    
    return l_var, standard_var, impact_factor

position_sizes = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
l_var_results = []

for size in position_sizes:
    l_var, std_var, impact = l_var_adjustment(size)
    l_var_results.append((size, l_var, std_var, impact))

l_var_df = pd.DataFrame(l_var_results, 
                        columns=['Position Size', 'L-VaR', 'Standard VaR', 'Impact Factor'])

plt.figure(figsize=(12, 6))
plt.plot(l_var_df['Position Size'], l_var_df['L-VaR'], 'r-', linewidth=3, label='Liquidity-Adjusted VaR')
plt.plot(l_var_df['Position Size'], l_var_df['Standard VaR'], 'b--', linewidth=2, label='Standard VaR')
plt.fill_between(l_var_df['Position Size'], 
                l_var_df['Standard VaR'], 
                l_var_df['L-VaR'], 
                alpha=0.3, 
                color='red', 
                label='Liquidity Risk Premium')

plt.title('Standard VaR vs Liquidity-Adjusted VaR', fontsize=16)
plt.xlabel('Position Size', fontsize=14)
plt.ylabel('Value at Risk', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('lvar_vs_standard_var.png', dpi=300)
plt.show()

print("Key Insights on Market Impact and L-VaR:")
print("-----------------------------------------")
print("1. Market impact increases convexly with trade size - doubling trade size more than doubles impact")
print("2. Market liquidity significantly affects impact magnitude - low liquidity amplifies impact")
print("3. L-VaR can be substantially higher than standard VaR for large positions")
print("4. Liquidity risk increases non-linearly with position size")
print("\nL-VaR Analysis for different position sizes:")
print(l_var_df.round(2).to_string(index=False))
