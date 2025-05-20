import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from arch import arch_model
from scipy import stats
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error
import time

# Set random seed for reproducibility
np.random.seed(42)

def get_sp500_data(start_date, end_date):
    data = yf.download('^GSPC', start=start_date, end=end_date)
    
    print("Columns in DataFrame:", data.columns)
    print("Column types:", type(data.columns))
    
    try:
        # Try direct access
        returns = 100 * data['Adj Close'].pct_change()
    except KeyError:
        try:
            # Try MultiIndex access
            returns = 100 * data[('Adj Close',)].pct_change()
        except KeyError:
            # If fails, close price instead
            print("Could not find 'Adj Close' column, using 'Close' instead")
            try:
                returns = 100 * data['Close'].pct_change()
            except KeyError:
                returns = 100 * data[('Close',)].pct_change()
    
    data['returns'] = returns
    return data

def calc_realized_volatility(returns, window=21):
    """Calculate realized volatility as rolling standard deviation of returns"""
    return returns.rolling(window=window).std() * np.sqrt(252)

def fit_garch_model(returns, p=1, q=1, forecast_horizon=1):
    returns = returns.dropna()
    
    model = arch_model(returns, vol='Garch', p=p, q=q, rescale=False)
    model_fit = model.fit(disp='off')
    
    conditional_vol = pd.Series(
        model_fit.conditional_volatility * np.sqrt(252),
        index=returns.index
    )
    
    # Generate out-of-sample forecasts
    forecasts = model_fit.forecast(horizon=forecast_horizon)
    forecast_vol = pd.Series(
        np.sqrt(forecasts.variance.iloc[-1].values) * np.sqrt(252),
        index=pd.date_range(start=returns.index[-1], periods=forecast_horizon+1)[1:]
    )
    
    return model_fit, conditional_vol, forecast_vol

def evaluate_forecasts(realized, forecasted):
    """Evaluate the forecasts against realized values"""
    # Align data
    joined = pd.concat([realized, forecasted], axis=1).dropna()
    realized_aligned = joined.iloc[:, 0]
    forecasted_aligned = joined.iloc[:, 1]
    
    mse = mean_squared_error(realized_aligned, forecasted_aligned)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(realized_aligned, forecasted_aligned)
    
    corr = stats.pearsonr(realized_aligned, forecasted_aligned)[0]
    
    return {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'Correlation': corr
    }


# Crisis and calm periods
periods = {
    'GFC': ('2008-01-01', '2009-06-30'),
    'Calm_Post_GFC': ('2013-01-01', '2014-12-31'),
    'COVID': ('2020-02-01', '2020-06-30'),
    'Calm_Recent': ('2021-06-01', '2022-12-31')
}

def analyze_period(period_name, start_date, end_date):
    print(f"\nAnalyzing {period_name} period from {start_date} to {end_date}")
    
    data = get_sp500_data(start_date, end_date)
    returns = data['returns'].dropna()
    
    realized_vol = calc_realized_volatility(returns)
    
    model_fit, cond_vol, _ = fit_garch_model(returns)
    
    eval_results = evaluate_forecasts(realized_vol, cond_vol)
    
    print("\nGARCH Model Summary:")
    print(model_fit.summary().tables[0].as_text())
    print(model_fit.summary().tables[1].as_text())
    print("\nForecast Evaluation Metrics:")
    for metric, value in eval_results.items():
        print(f"{metric}: {value:.4f}")
    
    plt.figure(figsize=(14, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(returns)
    plt.title(f'S&P 500 Returns ({period_name})')
    plt.ylabel('Returns (%)')
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(realized_vol, label='Realized Volatility (21-day rolling)')
    plt.plot(cond_vol, label='GARCH Conditional Volatility')
    plt.title('Realized vs GARCH Forecasted Volatility')
    plt.ylabel('Annualized Volatility (%)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    forecast_error = realized_vol - cond_vol
    plt.plot(forecast_error)
    plt.title('Forecast Error (Realized - Forecasted)')
    plt.ylabel('Error')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'GARCH_Analysis_{period_name}.png')
    plt.show()
    
    return {
        'returns': returns,
        'realized_vol': realized_vol,
        'cond_vol': cond_vol,
        'eval_results': eval_results,
        'model': model_fit
    }

# Run for each period
results = {}
for period_name, (start_date, end_date) in periods.items():
    try:
        results[period_name] = analyze_period(period_name, start_date, end_date)
        time.sleep(10)  # To avoid hitting API limits
    except Exception as e:
        print(f"Error analyzing {period_name} period: {e}")

# Run comparative analysis if results for at least one period
if results:
    def compare_periods():
        # Get only the periods that were successfully analyzed
        available_periods = list(results.keys())
        
        if len(available_periods) < 2:
            print("\nNot enough periods successfully analyzed for comparison")
            return None
        
        metrics_df = pd.DataFrame({
            period: results[period]['eval_results'] 
            for period in available_periods
        }).T
        
        print("\nComparative Analysis Across Periods:")
        print(metrics_df)
        
        plt.figure(figsize=(14, 12))
        
        plt.subplot(2, 2, 1)
        metrics_df['RMSE'].plot(kind='bar')
        plt.title('RMSE Comparison Across Periods')
        plt.ylabel('RMSE')
        plt.grid(True, axis='y')
        
        plt.subplot(2, 2, 2)
        metrics_df['Correlation'].plot(kind='bar')
        plt.title('Forecast Correlation Comparison Across Periods')
        plt.ylabel('Correlation')
        plt.grid(True, axis='y')
        
        plt.subplot(2, 2, 3)
        metrics_df['MAE'].plot(kind='bar')
        plt.title('MAE Comparison Across Periods')
        plt.ylabel('MAE')
        plt.grid(True, axis='y')
        
        plt.subplot(2, 2, 4)
        for period in available_periods:
            realized = results[period]['realized_vol']
            predicted = results[period]['cond_vol']
            
            joined = pd.concat([realized, predicted], axis=1).dropna()
            if not joined.empty:
                plt.scatter(
                    joined.iloc[:, 0], 
                    joined.iloc[:, 1], 
                    label=period,
                    alpha=0.7
                )
        
        plt.plot([0, 100], [0, 100], 'k--', alpha=0.5)  
        plt.title('Realized vs. Predicted Volatility')
        plt.xlabel('Realized Volatility')
        plt.ylabel('Predicted Volatility')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('GARCH_Period_Comparison.png')
        plt.show()
        
        return metrics_df

    comparison_results = compare_periods()

    print("\nChecking for asymmetric effects by fitting GJR-GARCH model...")
    for period_name in results.keys():
        returns = results[period_name]['returns'].dropna()
        
        try:
            gjr_model = arch_model(returns, vol='GARCH', p=1, q=1, o=1)
            gjr_fit = gjr_model.fit(disp='off')
            
            params = gjr_fit.params
            
            gamma_param = None
            for param_name in params.index:
                if 'gamma' in param_name:
                    gamma_param = param_name
                    break
            
            if gamma_param:
                asymmetry_coef = params[gamma_param]
                print(f"\n{period_name} Period:")
                print(f"Asymmetry coefficient: {asymmetry_coef:.4f}")
                print(f"Significant at 5%: {'Yes' if gjr_fit.pvalues[gamma_param] < 0.05 else 'No'}")
                print(f"p-value: {gjr_fit.pvalues[gamma_param]:.4f}")
            else:
                print(f"\n{period_name} Period: No asymmetry coefficient found in GJR-GARCH model")
        except Exception as e:
            print(f"Error fitting GJR-GARCH for {period_name}: {e}")

    crisis_periods = ['GFC', 'COVID']
    calm_periods = ['Calm_Post_GFC', 'Calm_Recent']
    
    available_crisis = [p for p in crisis_periods if p in results]
    available_calm = [p for p in calm_periods if p in results]
    
    if available_crisis and available_calm:
        print("\n" + "="*60)
        print("FINAL SUMMARY: GARCH FORECAST VS REALIZED VOLATILITY")
        print("="*60)
        print("\nKey Findings:")
        print("1. Crisis vs Calm Period Performance:")
        
        crisis_rmse = sum(results[p]['eval_results']['RMSE'] for p in available_crisis) / len(available_crisis)
        calm_rmse = sum(results[p]['eval_results']['RMSE'] for p in available_calm) / len(available_calm)
        print(f"   - Average RMSE in Crisis Periods: {crisis_rmse:.4f}")
        print(f"   - Average RMSE in Calm Periods: {calm_rmse:.4f}")
        print(f"   - Ratio (Crisis/Calm): {crisis_rmse / calm_rmse:.2f}x")

        # Correlation 
        crisis_corr = sum(results[p]['eval_results']['Correlation'] for p in available_crisis) / len(available_crisis)
        calm_corr = sum(results[p]['eval_results']['Correlation'] for p in available_calm) / len(available_calm)
        print(f"\n2. Forecast Correlation with Realized Volatility:")
        print(f"   - Average Correlation in Crisis Periods: {crisis_corr:.4f}")
        print(f"   - Average Correlation in Calm Periods: {calm_corr:.4f}")

        print("\n3. Model Parameter Stability:")
        for period in results.keys():
            alpha = results[period]['model'].params['alpha[1]']
            beta = results[period]['model'].params['beta[1]']
            persistence = alpha + beta
            print(f"   - {period}: α={alpha:.4f}, β={beta:.4f}, Persistence={persistence:.4f}")

        print("\n4. Conclusion:")
        print("   Based on the analysis, GARCH models show:")
        if crisis_rmse > calm_rmse:
            print(f"   - Higher prediction errors during crisis periods ({crisis_rmse/calm_rmse:.2f}x higher RMSE)")
        else:
            print(f"   - Surprisingly lower prediction errors during crisis periods")
            
        if crisis_corr > calm_corr:
            print(f"   - Stronger correlation with realized volatility during crisis periods")
        else:
            print(f"   - Weaker correlation with realized volatility during crisis periods")
else:
    print("No periods could be successfully analyzed. Please check the data and error messages above.")
