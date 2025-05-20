import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
from typing import List, Tuple, Optional

def fetch_stock_data(stocks: List[str], 
                    start_date: Optional[dt.datetime] = None, 
                    end_date: Optional[dt.datetime] = None) -> Tuple[pd.Series, pd.DataFrame]:
    if end_date is None:
        end_date = dt.datetime.now()
    if start_date is None:
        start_date = end_date - dt.timedelta(days=365)
    
    try:
        stockData = yf.download(stocks, start=start_date, end=end_date)
        stockData = stockData['Close']
        returns = stockData.pct_change().dropna()
        
        meanReturns = returns.mean()
        covMatrix = returns.cov()
        
        print("Stock Data Summary:")
        print(f"Date Range: {start_date.date()} to {end_date.date()}")
        print("\nMean Returns:")
        print(meanReturns)
        
        return meanReturns, covMatrix
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        raise

def generate_random_weights(stocks: List[str], method: str = 'uniform') -> np.ndarray:
    if method == 'uniform':
        weights = np.ones(len(stocks)) / len(stocks)
    elif method == 'random':
        weights = np.random.random(len(stocks))
        weights /= np.sum(weights)
    else:
        raise ValueError("Invalid weight generation method")
    
    print("\nPortfolio Weights:")
    for stock, weight in zip(stocks, weights):
        print(f"{stock}: {weight*100:.2f}%")
    
    return weights

def run_monte_carlo_simulation(meanReturns: pd.Series, 
                             covMatrix: pd.DataFrame, 
                             weights: np.ndarray, 
                             initial_investment: float = 10000,
                             num_simulations: int = 50, 
                             time_horizon: int = 252) -> np.ndarray:
    meanM = np.full(shape=(time_horizon, len(weights)), fill_value=meanReturns)
    meanM = meanM.T
    
    portfolio_sims = np.full(shape=(time_horizon, num_simulations), fill_value=0.0)
    
    # Monte Carlo simulation
    for m in range(num_simulations):
        # Generate random daily returns with historical correlations
        Z = np.random.normal(size=(time_horizon, len(weights)))
        L = np.linalg.cholesky(covMatrix)
        dailyReturns = meanM + np.inner(L, Z)
        
        # Calculate cumulative portfolio returns
        portfolio_sims[:,m] = np.cumprod(
            np.inner(weights, dailyReturns.T) + 1
        ) * initial_investment
    
    return portfolio_sims

def plot_simulations(portfolio_sims: np.ndarray, initial_investment: float):
    plt.figure(figsize=(12, 6))
    
    # Plot individual simulation paths
    for i in range(portfolio_sims.shape[1]):
        plt.plot(portfolio_sims[:, i], linewidth=0.7)
    
    # Calculate and plot percentile lines
    percentiles = [10, 50, 90]
    percentile_values = np.percentile(portfolio_sims, percentiles, axis=1)
    
    colors = ['red', 'blue', 'red']
    labels = ['10th Percentile', 'Median', '90th Percentile']
    
    for i, (perc_line, color, label) in enumerate(zip(percentile_values, colors, labels)):
        plt.plot(perc_line, color=color, linewidth=3, label=label)
    
    plt.title(f'Monte Carlo Simulation: ${initial_investment:,.0f} Portfolio')
    plt.xlabel('Trading Days')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def simulation_summary(portfolio_sims: np.ndarray, initial_investment: float):
    final_values = portfolio_sims[-1, :]
    
    print("\nSimulation Summary:")
    print(f"Initial Investment: ${initial_investment:,.2f}")
    print(f"Number of Simulations: {portfolio_sims.shape[1]}")
    print(f"\nFinal Portfolio Value Statistics:")
    print(f"Minimum: ${final_values.min():,.2f}")
    print(f"Maximum: ${final_values.max():,.2f}")
    print(f"Mean:    ${final_values.mean():,.2f}")
    print(f"Median:  ${np.median(final_values):,.2f}")
    
    # Probability of Profit
    profit_prob = (final_values > initial_investment).mean() * 100
    print(f"\nProbability of Profit: {profit_prob:.2f}%")

def main():
    # Example usage
    stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
    initial_investment = 10000
    
    # Fetch stock data
    meanReturns, covMatrix = fetch_stock_data(stocks)
    
    # Generate weights
    weights = generate_random_weights(stocks, method='random')
    
    # Run simulation
    portfolio_sims = run_monte_carlo_simulation(
        meanReturns=meanReturns,
        covMatrix=covMatrix,
        weights=weights,
        initial_investment=initial_investment,
        num_simulations=80,
        time_horizon=252
    )
    
    # Plot results
    plot_simulations(portfolio_sims, initial_investment)
    
    # Show summary
    simulation_summary(portfolio_sims, initial_investment)

if __name__ == "__main__":
    main()
