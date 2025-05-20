import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

plt.ion()

def get_data(stocks, start, end):
    stockData = yf.download(stocks, start=start, end=end) 
    stockData = stockData['Close']  
    returns = stockData.pct_change()  
    meanReturns = returns.mean()  
    covMatrix = returns.cov()  
    return meanReturns, covMatrix

stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=365)
mc_sims = 120  
T = 252  
initialPortfolioValue = 10000 
meanReturns, covMatrix = get_data(stocks, startDate, endDate)     

weights = np.random.dirichlet(np.ones(len(meanReturns)), size=1)[0]    

meanM = np.full(shape=(T, len(weights)), fill_value=meanReturns.values)
portfolio_sims = np.full(shape=(T, mc_sims), fill_value=initialPortfolioValue)

# Ensure the covariance matrix is positive semi-definite for Cholesky decomposition
try:
    L = np.linalg.cholesky(covMatrix)   
except np.linalg.LinAlgError:
    eigvals, eigvecs = np.linalg.eigh(covMatrix)  
    eigvals = np.maximum(eigvals, 0)  # Set negative eigenvalues to zero
    covMatrix_fixed = eigvecs @ np.diag(eigvals) @ eigvecs.T  
    L = np.linalg.cholesky(covMatrix_fixed)  

# ------ Monte Carlo simulation of portfolio growth ------
for m in range(mc_sims):
    Z = np.random.normal(size=(T, len(weights)))    
    dailyReturns = meanM + np.dot(Z, L.T)  # Corrected this line
    portfolio_returns = np.dot(weights, dailyReturns.T)  # Portfolio returns for each day
    # Calculate cumulative product of returns
    for t in range(1, T):
        portfolio_sims[t, m] = portfolio_sims[t-1, m] * (1 + portfolio_returns[t])

def VaR(returns, alpha=5):
    if isinstance(returns, pd.Series):
        return np.percentile(returns, alpha)
    else:
        raise TypeError("Expected pandas series")

def CVaR(returns, alpha=5):
    if isinstance(returns, pd.Series):
        belowVaR = returns <= VaR(returns, alpha=alpha)
        return returns[belowVaR].mean()
    else:
        raise TypeError("Expected pandas series")

# ------ Convert portfolio values into percentage returns ------
portfolioReturns = (portfolio_sims[-1, :] - initialPortfolioValue) / initialPortfolioValue  
VaR_percent = VaR(pd.Series(portfolioReturns), alpha=5)   
CVaR_percent = CVaR(pd.Series(portfolioReturns), alpha=5)  
VaR_dollar = VaR_percent * initialPortfolioValue   
CVaR_dollar = CVaR_percent * initialPortfolioValue  

# ------ Compute VaR & CVaR in absolute portfolio value ------
VaR_value = VaR(pd.Series(portfolio_sims[-1, :]), alpha=5)  # 5% percentile portfolio value
CVaR_value = CVaR(pd.Series(portfolio_sims[-1, :]), alpha=5)  # Average worst 5% portfolio value
print(f'Value at Risk (VaR) at 95% confidence level: ${round(VaR_dollar, 2)}')
print(f'Conditional Value at Risk (CVaR) at 95% confidence level: ${round(CVaR_dollar, 2)}')

plt.figure(figsize=(13, 6))

# ------ Histogram of Portfolio Returns with VaR & CVaR ------
plt.subplot(1, 2, 1)
plt.hist(portfolioReturns, bins=50, color="blue", alpha=0.6, label="Simulated Returns")
plt.axvline(VaR_percent, color='red', linestyle='dashed', linewidth=2, label=f"VaR 95%: {VaR_percent:.2%}")
plt.axvline(CVaR_percent, color='green', linestyle='dashed', linewidth=2, label=f"CVaR 95%: {CVaR_percent:.2%}")
plt.xlabel("Portfolio Return (%)")
plt.ylabel("Frequency")
plt.title("Portfolio Return Distribution")
plt.legend(prop={'size': 10})

# ------ Histogram of Portfolio Value with VaR & CVaR ------
plt.subplot(1, 2, 2)
plt.hist(portfolio_sims[-1, :], bins=50, color="purple", alpha=0.6, label="Simulated Portfolio Value")
plt.axvline(VaR_value, color='red', linestyle='dashed', linewidth=2, label=f"VaR 95%: ${VaR_value:,.2f}")
plt.axvline(CVaR_value, color='green', linestyle='dashed', linewidth=2, label=f"CVaR 95%: ${CVaR_value:,.2f}")
plt.xlabel("Portfolio Value ($)")
plt.ylabel("Frequency")
plt.title("Portfolio Value Distribution")
plt.legend(prop={'size': 10})

plt.tight_layout()

# ------ Monte Carlo Simulations of Portfolio Value with VaR & CVaR ------
plt.figure(figsize=(14, 8))
for i in range(mc_sims):
    plt.plot(portfolio_sims[:, i], alpha=0.3)  # Each simulation path
plt.axhline(VaR_value, color='red', linestyle='dashed', linewidth=2, label=f"VaR 95%: ${VaR_value:,.2f}")
plt.axhline(CVaR_value, color='green', linestyle='dashed', linewidth=2, label=f"CVaR 95%: ${CVaR_value:,.2f}")
plt.axhline(initialPortfolioValue, color='black', linestyle='dashed', linewidth=2, label="Initial Value")
plt.xlabel("Days")
plt.ylabel("Portfolio Value ($)")
plt.title("Monte Carlo Simulation of Portfolio Growth")
plt.legend(prop={'size': 10})

plt.show(block=True)
