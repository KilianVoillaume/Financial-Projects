import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

# Function to fetch stock data & calculate returns
def get_data(stocks, start, end):
    stockData = yf.download(stocks, start=start, end=end)  # Fetch historical stock data
    stockData = stockData['Close']  # Extract closing prices
    returns = stockData.pct_change()  # Calculate daily returns
    meanReturns = returns.mean()  # Compute mean daily return for each stock
    covMatrix = returns.cov()  # Compute covariance matrix of returns
    return meanReturns, covMatrix

# Define stock portfolio
stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']

# Define start and end dates for historical data
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=365)

# Fetch mean returns & covariance matrix from historical data
meanReturns, covMatrix = get_data(stocks, startDate, endDate)     

# Generate better diversified portfolio weights using Dirichlet distribution
weights = np.random.dirichlet(np.ones(len(meanReturns)), size=1)[0]    

# Monte Carlo Simulation Parameters
mc_sims = 250  # Number of Monte Carlo simulations
T = 100  # Time horizon in days
initialPortfolioValue = 10000  # Initial investment amount

# Create mean return matrix
meanM = np.full((T, len(weights)), meanReturns).T   

# Ensure the covariance matrix is positive semi-definite for Cholesky decomposition
try:
    L = np.linalg.cholesky(covMatrix)   
except np.linalg.LinAlgError:
    eigvals, eigvecs = np.linalg.eigh(covMatrix)  
    eigvals = np.maximum(eigvals, 0)  # Set negative eigenvalues to zero
    covMatrix_fixed = eigvecs @ np.diag(eigvals) @ eigvecs.T  
    L = np.linalg.cholesky(covMatrix_fixed)  

# Initialize matrix for storing Monte Carlo simulations
portfolio_sims = np.zeros((T, mc_sims))  

# Monte Carlo simulation of portfolio growth
for m in range(mc_sims):
      Z = np.random.normal(size=(T, len(weights)))    
      dailyReturns = meanM + np.inner(L, Z)     
      portfolio_sims[:,m] = np.cumprod(np.inner(weights, dailyReturns.T) + 1) * initialPortfolioValue   

# Define VaR and CVaR functions
def mcVar(returns, alpha=5):
    """
    Input: pandas series of returns
    Output: percentile (alpha%) return distribution for a given confidence level
    """
    if isinstance(returns, pd.Series):
        return np.percentile(returns, alpha)
    else:
        raise TypeError("Expected pandas series")

def mcCVar(returns, alpha=5):
    """
    Input: pandas series of returns
    Output: CVaR or expected shortfall at a given confidence level
    """
    if isinstance(returns, pd.Series):
        belowVaR = returns <= mcVar(returns, alpha=alpha)
        return returns[belowVaR].mean()
    else:
        raise TypeError("Expected pandas series")

# Convert portfolio values into percentage returns
portfolioReturns = (portfolio_sims[-1, :] - initialPortfolioValue) / initialPortfolioValue  

# Compute VaR & CVaR in percentage terms
VaR_percent = mcVar(pd.Series(portfolioReturns), alpha=5)   
CVaR_percent = mcCVar(pd.Series(portfolioReturns), alpha=5)  

# Convert to dollar values
VaR_dollar = VaR_percent * initialPortfolioValue   
CVaR_dollar = CVaR_percent * initialPortfolioValue  

# Compute VaR & CVaR in absolute portfolio value
VaR_value = mcVar(pd.Series(portfolio_sims[-1, :]), alpha=5)  # 5% percentile portfolio value
CVaR_value = mcCVar(pd.Series(portfolio_sims[-1, :]), alpha=5)  # Average worst 5% portfolio value

# Print results
print(f'Value at Risk (VaR) at 95% confidence level: ${round(VaR_dollar, 2)}')
print(f'Conditional Value at Risk (CVaR) at 95% confidence level: ${round(CVaR_dollar, 2)}')

import matplotlib.pyplot as plt

# Create a figure with 3 subplots in a single row (or stack them in a column)
fig, axes = plt.subplots(3, 1, figsize=(12, 15))  # 3 rows, 1 column

# === PLOT 1: Histogram of Portfolio Returns with VaR & CVaR ===
axes[0].hist(portfolioReturns, bins=50, color="blue", alpha=0.6, label="Simulated Returns")
axes[0].axvline(VaR_percent, color='red', linestyle='dashed', linewidth=2, label=f"VaR 95%: {VaR_percent:.2%}")
axes[0].axvline(CVaR_percent, color='green', linestyle='dashed', linewidth=2, label=f"CVaR 95%: {CVaR_percent:.2%}")
axes[0].set_xlabel("Portfolio Return (%)")
axes[0].set_ylabel("Frequency")
axes[0].set_title("Monte Carlo Simulated Portfolio Return Distribution")
axes[0].legend()

# === PLOT 2: Histogram of Portfolio Value with VaR & CVaR ===
axes[1].hist(portfolio_sims[-1, :], bins=50, color="purple", alpha=0.6, label="Simulated Portfolio Value")
axes[1].axvline(VaR_value, color='red', linestyle='dashed', linewidth=2, label=f"VaR 95%: ${VaR_value:,.2f}")
axes[1].axvline(CVaR_value, color='green', linestyle='dashed', linewidth=2, label=f"CVaR 95%: ${CVaR_value:,.2f}")
axes[1].set_xlabel("Portfolio Value ($)")
axes[1].set_ylabel("Frequency")
axes[1].set_title("Monte Carlo Simulated Portfolio Value Distribution")
axes[1].legend()

# === PLOT 3: Monte Carlo Simulations of Portfolio Value with VaR & CVaR ===
for i in range(mc_sims):
    axes[2].plot(portfolio_sims[:, i], alpha=0.3)  # Each simulation path
axes[2].axhline(VaR_value, color='red', linestyle='dashed', linewidth=2, label=f"VaR 95%: ${VaR_value:,.2f}")
axes[2].axhline(CVaR_value, color='green', linestyle='dashed', linewidth=2, label=f"CVaR 95%: ${CVaR_value:,.2f}")
axes[2].axhline(initialPortfolioValue, color='black', linestyle='dashed', linewidth=2, label="Initial Value")
axes[2].set_xlabel("Days")
axes[2].set_ylabel("Portfolio Value ($)")
axes[2].set_title("Monte Carlo Simulation of Portfolio Growth")
axes[2].legend()

# Adjust layout and show the plots together
plt.tight_layout()
plt.show()



