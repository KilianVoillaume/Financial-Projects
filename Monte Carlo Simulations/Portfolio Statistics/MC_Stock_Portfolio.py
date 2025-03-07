import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

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

meanReturns, covMatrix = get_data(stocks, startDate, endDate)     
            #The mean returns provide the expected daily return for each stock, while the covariance matrix measures how the stock returns move together (volatility and correlation).

weights = np.random.random(len(meanReturns))    
            #Random weights for each stock
weights /= np.sum(weights)    
            #Normalize the weights to sum up to 1

# Monte Carlo Method

mc_sims = 250
T = 100 #timeframe in days
meanM = np.full(shape=(T, len(weights)), fill_value=meanReturns)  
            #Creates a T*len(weights) matrix where each row is the meanReturns
meanM = meanM.T   
            #Transpose the matrix so that each column is the meanReturns

portfolio_sims = np.full(shape=(T, mc_sims), fill_value=0.0)

initialPortfolioValue = 10000

for m in range(0,mc_sims):
      #MC Loops
      Z = np.random.normal(size=(T, len(weights)))    
                  #This simulates random daily shocks to stock returns (similar to how real market prices fluctuate randomly)
      L = np.linalg.cholesky(covMatrix)   
                  #The Cholesky decomposition is used to generate realistic correlated returns.
                  #It ensures that the simulated asset prices respect historical covariances.
                  #Without it, stock returns would be modeled as independent, which is unrealistic.
      dailyReturns = meanM + np.inner(L, Z)     
                  #Multiply random shocks by the Cholesky matrix to introduce correlations between assets. Creates realistic daily returns for each stock.
      portfolio_sims[:,m] = np.cumprod(np.inner(weights, dailyReturns.T) + 1)*initialPortfolioValue   
                  #Uses cumlulative to siulative compounded growth. 

plt.plot(portfolio_sims)
plt.xlabel('Days')
plt.ylabel('Portfolio value ($)')
plt.title('Monte Carlo Simulation of Stock Portfolio')
plt.show()
