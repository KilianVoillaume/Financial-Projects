import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

def fetch_data(tickers, period="1y"):
    data = {}
    for ticker in tickers:
        try:
            stock_data = yf.download(ticker, period=period)
            data[ticker] = stock_data
            time.sleep(10)  # To avoid hitting the API limit
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    return data

def calculate_volatility(data, window=21):
    volatility = {}
    for ticker, df in data.items():
        if not df.empty:
            # Check which column to use for price data
            if 'Adj Close' in df.columns:
                price_col = 'Adj Close'
            elif 'Close' in df.columns:
                price_col = 'Close'
            else:
                print(f"Warning: No price data found for {ticker}. Available columns: {df.columns}")
                continue
            
            df['Returns'] = np.log(df[price_col] / df[price_col].shift(1))
            
            df['Volatility'] = df['Returns'].rolling(window=window).std() * np.sqrt(252)
            
            volatility[ticker] = df['Volatility']
    
    return volatility

def calculate_sharpe_ratio(data, risk_free_rate=0.02, window=252):
    sharpe_ratios = {}
    for ticker, df in data.items():
        if not df.empty:
            if 'Returns' not in df.columns:
                if 'Adj Close' in df.columns:
                    price_col = 'Adj Close'
                elif 'Close' in df.columns:
                    price_col = 'Close'
                else:
                    print(f"Warning: No price data found for {ticker}. Available columns: {df.columns}")
                    continue
                
                df['Returns'] = np.log(df[price_col] / df[price_col].shift(1))
            
            df['Mean_Return'] = df['Returns'].rolling(window=window).mean() * 252
            
            df['Rolling_Vol'] = df['Returns'].rolling(window=window).std() * np.sqrt(252)
            
            df['Sharpe_Ratio'] = np.where(
                df['Rolling_Vol'] > 0,
                (df['Mean_Return'] - risk_free_rate) / df['Rolling_Vol'],
                np.nan
            )
            
            sharpe_ratios[ticker] = df['Sharpe_Ratio']
    
    return sharpe_ratios

def plot_volatility(volatilities, tickers):
    """Create a figure window with two volatility plots (one below the other)"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: First stock's historical volatility (top)
    first_ticker = tickers[0]
    if first_ticker in volatilities:
        volatilities[first_ticker].dropna().plot(ax=ax1, color='blue')
        ax1.set_title(f'{first_ticker} Historical Volatility')
        ax1.set_ylabel('Volatility (Annualized)')
        ax1.grid(True)
    else:
        ax1.text(0.5, 0.5, f"No data for {first_ticker}", 
                 horizontalalignment='center', verticalalignment='center')
    
    # Plot 2: All stocks historical volatility (bottom)
    plot_count = 0
    for ticker, vol in volatilities.items():
        if not vol.dropna().empty:
            vol.dropna().plot(ax=ax2, label=ticker)
            plot_count += 1
    
    if plot_count > 0:
        ax2.set_title('All Stocks Historical Volatility')
        ax2.set_ylabel('Volatility (Annualized)')
        ax2.legend()
        ax2.grid(True)
    else:
        ax2.text(0.5, 0.5, "No volatility data available", 
                 horizontalalignment='center', verticalalignment='center')
    
    plt.tight_layout()
    plt.suptitle("Historical Volatility Analysis", fontsize=16, y=1.02)
    
    return fig

def plot_sharpe_ratio(sharpe_ratios, tickers):
    """Create a figure window with two Sharpe ratio plots (one below the other)"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: First stock's Sharpe ratio (top)
    first_ticker = tickers[0]
    if first_ticker in sharpe_ratios:
        sharpe_ratios[first_ticker].dropna().plot(ax=ax1, color='green')
        ax1.set_title(f'{first_ticker} Sharpe Ratio')
        ax1.set_ylabel('Sharpe Ratio')
        ax1.grid(True)
    else:
        ax1.text(0.5, 0.5, f"No Sharpe ratio data for {first_ticker}", 
                 horizontalalignment='center', verticalalignment='center')
    
    # Plot 2: All stocks Sharpe ratio (bottom)
    plot_count = 0
    for ticker, sharpe in sharpe_ratios.items():
        if not sharpe.dropna().empty:
            sharpe.dropna().plot(ax=ax2, label=ticker)
            plot_count += 1
    
    if plot_count > 0:
        ax2.set_title('All Stocks Sharpe Ratio')
        ax2.set_ylabel('Sharpe Ratio')
        ax2.legend()
        ax2.grid(True)
    else:
        ax2.text(0.5, 0.5, "No Sharpe ratio data available", 
                 horizontalalignment='center', verticalalignment='center')
    
    plt.tight_layout()
    plt.suptitle("Sharpe Ratio Analysis", fontsize=16, y=1.02)
    
    return fig

def debug_data_structure(data):
    for ticker, df in data.items():
        print(f"\nData for {ticker}:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns}")
        print(f"Sample data:")
        print(df.head(3))

def main():
    tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META']
    
    print(f"Fetching data for: {', '.join(tickers)}")
    stock_data = fetch_data(tickers, period="3y")

    debug_data_structure(stock_data)
    volatilities = calculate_volatility(stock_data, window=21)
    sharpe_ratios = calculate_sharpe_ratio(stock_data, risk_free_rate=0.02, window=252)
    vol_fig = plot_volatility(volatilities, tickers)
    sharpe_fig = plot_sharpe_ratio(sharpe_ratios, tickers)
    
    plt.show()
    print("Analysis complete.")

if __name__ == "__main__":
    main()
