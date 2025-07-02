import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

np.random.seed(42)

class LMMCalibration:
    def __init__(self, maturities, strikes, market_vols):
        self.maturities = maturities
        self.strikes = strikes
        self.market_vols = market_vols
        
        self.beta = 0.5  # Mean reversion 
        self.a = 0.1     # Level 
        self.b = 0.3     # Slope 
        self.c = 0.5     # Curvature 
        self.d = 0.2     # Skew 
        
    def vol_param(self, params, maturity, strike, forward_rate):
        beta, a, b, c, d = params
        
        # Maturity effect (term structure)
        maturity_effect = a + b * np.exp(-beta * maturity)
        
        # Moneyness effect (smile/skew)
        moneyness = strike / forward_rate - 1.0
        smile_effect = c * moneyness**2 + d * moneyness
        
        return maturity_effect * (1 + smile_effect)
    
    def lmm_implied_vol(self, params, maturity, strike, forward_rate):
        beta, a, b, c, d = params
        
        inst_vol = self.vol_param(params, maturity, strike, forward_rate)
        smile_adjustment = 1 + c * ((strike / forward_rate - 1.0) ** 2)
        decay_factor = (1 - np.exp(-beta * maturity)) / (beta * maturity) if beta > 0.001 else 1.0
        
        return inst_vol * decay_factor * smile_adjustment
    
    def calibration_error(self, params):
        beta, a, b, c, d = params
        
        # Reasonable ranges
        if beta < 0 or a < 0 or a > 1:
            return 1e10      
        errors = []
        forward_rates = 0.03 + 0.005 * np.sqrt(self.maturities)
        
        for i, maturity in enumerate(self.maturities):
            for j, strike in enumerate(self.strikes):
                forward_rate = forward_rates[i]
                model_vol = self.lmm_implied_vol(params, maturity, strike, forward_rate)
                market_vol = self.market_vols[i, j]
                errors.append((model_vol - market_vol) ** 2)
        
        return np.sum(errors)
    
    def calibrate(self):
        initial_params = (self.beta, self.a, self.b, self.c, self.d)
        bounds = ((0.01, 2.0), (0.01, 0.5), (0.01, 1.0), (0.0, 2.0), (-0.5, 0.5))
        
        result = minimize(
            self.calibration_error,
            initial_params,
            method='L-BFGS-B',
            bounds=bounds
        )
        
        self.beta, self.a, self.b, self.c, self.d = result.x
        return result.x
    
    def get_model_vols(self):
        model_vols = np.zeros_like(self.market_vols)
        forward_rates = 0.03 + 0.005 * np.sqrt(self.maturities)
        
        for i, maturity in enumerate(self.maturities):
            for j, strike in enumerate(self.strikes):
                params = (self.beta, self.a, self.b, self.c, self.d)
                model_vols[i, j] = self.lmm_implied_vol(params, maturity, strike, forward_rates[i])
        
        return model_vols
    
    def plot_vol_surface(self, vols, title):
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        X, Y = np.meshgrid(self.strikes, self.maturities)
        
        surf = ax.plot_surface(X, Y, vols, cmap=cm.coolwarm, alpha=0.8, 
                               linewidth=0, antialiased=True)
        
        ax.set_xlabel('Strike')
        ax.set_ylabel('Maturity (years)')
        ax.set_zlabel('Implied Volatility')
        ax.set_title(title)
        
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        
        return fig
    
    def plot_vol_heatmap(self, vols, title):
        fig, ax = plt.subplots(figsize=(10, 8))
        
        im = ax.imshow(vols, cmap='viridis', aspect='auto', origin='lower',
                      extent=[min(self.strikes), max(self.strikes), 
                              min(self.maturities), max(self.maturities)])
        
        ax.set_xlabel('Strike')
        ax.set_ylabel('Maturity (years)')
        ax.set_title(title)
        
        cbar = fig.colorbar(im)
        cbar.set_label('Implied Volatility')
        
        # Add contour lines
        X, Y = np.meshgrid(self.strikes, self.maturities)
        CS = ax.contour(X, Y, vols, colors='white', alpha=0.5)
        ax.clabel(CS, inline=True, fontsize=8)
        
        return fig
    
    def plot_vol_comparison(self, model_vols):
        maturities_to_plot = [0, len(self.maturities)//3, 2*len(self.maturities)//3, -1]
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        axes = axes.flatten()
        
        for i, mat_idx in enumerate(maturities_to_plot):
            maturity = self.maturities[mat_idx]
            axes[i].plot(self.strikes, self.market_vols[mat_idx], 'o-', label='Market')
            axes[i].plot(self.strikes, model_vols[mat_idx], 's--', label='LMM')
            axes[i].set_xlabel('Strike')
            axes[i].set_ylabel('Implied Volatility')
            axes[i].set_title(f'Maturity: {maturity:.2f} years')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig

def create_synthetic_market_data():
    maturities = np.linspace(0.5, 10, 20)
    strikes = np.linspace(0.01, 0.06, 15)
    
    market_vols = np.zeros((len(maturities), len(strikes)))
    
    a_market = 0.2
    b_market = 0.1
    beta_market = 0.5
    c_market = 8.0
    d_market = -0.5
    
    forward_rates = 0.03 + 0.005 * np.sqrt(maturities)
    
    for i, maturity in enumerate(maturities):
        for j, strike in enumerate(strikes):
            # Term structure
            vol = a_market + b_market * np.exp(-beta_market * maturity)
            
            # Smile effect
            moneyness = strike / forward_rates[i] - 1.0
            vol *= (1 + c_market * moneyness**2 + d_market * moneyness)
            
            # Noise
            vol += np.random.normal(0, 0.002)
            
            market_vols[i, j] = max(vol, 0.05)  # Positive volatility
    return maturities, strikes, market_vols


def main(): 
    print("Generating synthetic market data...")
    maturities, strikes, market_vols = create_synthetic_market_data()
    
    print("Initializing LMM calibration...")
    lmm = LMMCalibration(maturities, strikes, market_vols)
    
    print("Calibrating LMM model to market data...")
    params = lmm.calibrate()
    print(f"Calibrated parameters: β={params[0]:.4f}, a={params[1]:.4f}, b={params[2]:.4f}, c={params[3]:.4f}, d={params[4]:.4f}")
    
    model_vols = lmm.get_model_vols()
    
    mse = np.mean((model_vols - market_vols)**2)
    print(f"Mean squared calibration error: {mse:.8f}")
    
    fig_market = lmm.plot_vol_surface(market_vols, "Market Implied Volatility Surface")
    fig_market.savefig("market_vol_surface.png", dpi=300, bbox_inches='tight')
    
    fig_model = lmm.plot_vol_surface(model_vols, "LMM Calibrated Volatility Surface")
    fig_model.savefig("lmm_vol_surface.png", dpi=300, bbox_inches='tight')
    
    fig_heat_market = lmm.plot_vol_heatmap(market_vols, "Market Implied Volatility Heatmap")
    fig_heat_market.savefig("market_vol_heatmap.png", dpi=300, bbox_inches='tight')
    
    fig_heat_model = lmm.plot_vol_heatmap(model_vols, "LMM Calibrated Volatility Heatmap")
    fig_heat_model.savefig("lmm_vol_heatmap.png", dpi=300, bbox_inches='tight')
    
    fig_comparison = lmm.plot_vol_comparison(model_vols)
    fig_comparison.savefig("vol_comparison.png", dpi=300, bbox_inches='tight')
    
    error_matrix = np.abs(model_vols - market_vols)
    max_error = np.max(error_matrix)
    avg_error = np.mean(error_matrix)
    print(f"Maximum calibration error: {max_error:.6f}")
    print(f"Average calibration error: {avg_error:.6f}")
    
    selected_mats = [1, 3, 5, 10]
    mat_indices = [np.abs(maturities - mat).argmin() for mat in selected_mats]
    
    forward_rates = 0.03 + 0.005 * np.sqrt(maturities)
    
    print("\nVolatility smile at selected maturities:")
    for idx in mat_indices:
        mat = maturities[idx]
        atm_idx = np.abs(strikes - forward_rates[idx]).argmin()
        atm_vol_market = market_vols[idx, atm_idx]
        atm_vol_model = model_vols[idx, atm_idx]
        print(f"Maturity {mat:.2f} years:")
        print(f"  ATM Strike: {strikes[atm_idx]:.4f}, Market Vol: {atm_vol_market:.4f}, Model Vol: {atm_vol_model:.4f}")
    
    plt.show()

if __name__ == "__main__":
    main()
