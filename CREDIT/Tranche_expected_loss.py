"""
This simulation analyzes the impact of asset correlation on expected losses in synthetic CDO tranches using a Gaussian copula model.
The model simulates a portfolio of 125 credits with 2% default probability each, varying correlation from 0% to 100%.
Expected losses are calculated for both equity (0-3%) and mezzanine (3-7%) tranches across 50,000 Monte Carlo iterations.
The results demonstrate how correlation affects risk distribution across the capital structure in structured credit products.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd

n_names = 125  # Number of obligors in portfolio
n_simulations = 50000 
default_prob = 0.02 
notional = 100 
correlations = np.arange(0, 1.1, 0.1)  # Correlation levels from 0 to 1

equity_tranche = (0, 0.03)  # 0-3%
mezz_tranche = (0.03, 0.07)  # 3-7%

equity_losses = []
mezz_losses = []

for correlation in correlations:
    print(f"Simulating with correlation = {correlation:.1f}")
    
    tranche_losses = np.zeros((n_simulations, 2))  # [equity, mezzanine]
    
    for sim in range(n_simulations):
        market_factor = np.random.normal(0, 1)
        
        idiosyncratic_factors = np.random.normal(0, 1, n_names)
        asset_values = np.sqrt(correlation) * market_factor + np.sqrt(1 - correlation) * idiosyncratic_factors
        
        default_threshold = norm.ppf(default_prob)
        defaults = asset_values < default_threshold
        
        portfolio_loss = np.sum(defaults) / n_names * notional
        
        equity_loss = min(portfolio_loss, equity_tranche[1] * notional)
        mezz_loss = max(0, min(portfolio_loss - equity_tranche[1] * notional, 
                               (mezz_tranche[1] - mezz_tranche[0]) * notional))
                               
        equity_loss_pct = equity_loss / (equity_tranche[1] * notional)
        mezz_loss_pct = mezz_loss / ((mezz_tranche[1] - mezz_tranche[0]) * notional)
        
        tranche_losses[sim] = [equity_loss_pct, mezz_loss_pct]
    
    avg_losses = np.mean(tranche_losses, axis=0)
    equity_losses.append(avg_losses[0])
    mezz_losses.append(avg_losses[1])

equity_losses = np.array(equity_losses) * 100
mezz_losses = np.array(mezz_losses) * 100

results_df = pd.DataFrame({
    'Correlation': correlations,
    'Equity Tranche (0-3%) Loss %': equity_losses,
    'Mezzanine Tranche (3-7%) Loss %': mezz_losses
})
print(results_df.round(2))

plt.figure(figsize=(10, 6))
plt.plot(correlations * 100, equity_losses, 'o-', label='Equity Tranche (0-3%)', linewidth=2)
plt.plot(correlations * 100, mezz_losses, 's-', label='Mezzanine Tranche (3-7%)', linewidth=2)
plt.xlabel('Asset Correlation (%)', fontsize=12)
plt.ylabel('Expected Loss (%)', fontsize=12)
plt.title('Expected Tranche Losses vs Asset Correlation\nGaussian Copula Model, 125 Names, 2% Default Probability', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.xticks(np.arange(0, 110, 10))
plt.tight_layout()
plt.show()

print("\nExplanation of results:")
print(f"Equity tranche (0-3%): Expected loss ranges from {min(equity_losses):.2f}% to {max(equity_losses):.2f}%")
print(f"Mezzanine tranche (3-7%): Expected loss ranges from {min(mezz_losses):.2f}% to {max(mezz_losses):.2f}%")
