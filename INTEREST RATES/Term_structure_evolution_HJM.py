import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Set random seed for reproducibility
np.random.seed(42)

dt = 0.01  # Time step
T_max = 10.0  # Max maturity
t_max = 5.0  # Max simulation time
num_T = 100  # Points in maturity dimension
num_t = int(t_max / dt)  # Number of time steps
num_paths = 1 

t_grid = np.linspace(0, t_max, num_t)
T_grid = np.linspace(0, T_max, num_T)
t_mesh, T_mesh = np.meshgrid(t_grid, T_grid, indexing='ij')

def initial_forward_curve(T):
    # Nelson-Siegel parameterization for initial curve
    beta0 = 0.03  # Long-term level
    beta1 = -0.02  # Short-term component
    beta2 = 0.01  # Medium-term component
    lambda_param = 0.5  # Decay factor
    
    return beta0 + beta1 * np.exp(-lambda_param * T) + beta2 * ((lambda_param * T) * np.exp(-lambda_param * T))

def constant_vol(t, T):
    return 0.01 * np.ones_like(T)  # constant 1% 

def hump_vol(t, T):
    a = 0.1
    b = 0.3
    c = 2.0
    return a * np.exp(-b * (T - t)) * (1 - np.exp(-c * (T - t)))

def two_factor_vol(t, T):
    sigma1 = 0.01
    sigma2 = 0.015
    a1 = 0.5
    a2 = 0.1
    
    factor1 = sigma1 * np.exp(-a1 * (T - t))
    factor2 = sigma2 * np.exp(-a2 * (T - t))
    return np.sqrt(factor1**2 + factor2**2)

# Drift term in HJM model
def hjm_drift(f, vol_func, t, T_grid):
    drift = np.zeros_like(T_grid)
    
    for i in range(len(T_grid)):
        T = T_grid[i]
        if T > t:  # Only compute drift for future maturities
            vol_T = vol_func(t, T)
            integral = 0.0
            for j in range(i):
                T_j = T_grid[j]
                if T_j >= t and T_j < T:
                    vol_Tj = vol_func(t, T_j)
                    dT = T_grid[1] - T_grid[0]
                    integral += vol_T * vol_Tj * dT
            
            drift[i] = integral
    
    return drift

# Forward rate evolution
def simulate_hjm_model(vol_type="constant"):
    if vol_type == "constant":
        vol_func = constant_vol
    elif vol_type == "hump":
        vol_func = hump_vol
    elif vol_type == "two_factor":
        vol_func = two_factor_vol
    else:
        raise ValueError("Unknown volatility type")
    
    # Initialize forward rate surface
    f = np.zeros((num_t, num_T))
    
    # Set initial forward curve (t=0)
    f[0, :] = initial_forward_curve(T_grid)
    
    for i in range(1, num_t):
        t = t_grid[i-1]
        
        # Drift term (HJM)
        drift = hjm_drift(f[i-1, :], vol_func, t, T_grid)
        
        dW = np.sqrt(dt) * np.random.normal(0, 1)
        
        # Update forward rates using Euler discretization
        for j in range(num_T):
            T = T_grid[j]
            if T > t:  # Only update future rates
                vol = vol_func(t, T)
                f[i, j] = f[i-1, j] + drift[j] * dt + vol * dW
            else:
                # Past rates are realized
                if j > 0: 
                    f[i, j] = f[i-1, j]
    
    return f

def plot_3d_surface(f, vol_type):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(t_mesh, T_mesh, f, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Forward Rate')
    ax.set_xlabel('Time (t)')
    ax.set_ylabel('Maturity (T)')
    ax.set_zlabel('Forward Rate f(t,T)')
    ax.set_title(f'HJM Forward Rate Evolution with {vol_type.capitalize()} Volatility')
    plt.tight_layout()
    plt.show()

def create_animation(f, vol_type):
    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot(T_grid, f[0], 'b-', linewidth=2)
    
    ax.set_xlabel('Maturity (T)')
    ax.set_ylabel('Forward Rate f(t,T)')
    ax.set_title(f'Forward Rate Curve Evolution - {vol_type.capitalize()} Volatility')
    ax.set_ylim(np.min(f) - 0.005, np.max(f) + 0.005)
    ax.grid(True)
    time_text = ax.text(0.02, 0.95, 'Time t=0.00', transform=ax.transAxes)
    
    def update(frame):
        line.set_ydata(f[frame])
        time_text.set_text(f'Time t={t_grid[frame]:.2f}')
        return line, time_text
    
    ani = FuncAnimation(fig, update, frames=range(0, num_t, 10), 
                        blit=True, interval=100, repeat=True)
    plt.tight_layout()
    return ani

def compare_volatility_models():
    f_constant = simulate_hjm_model("constant")
    f_hump = simulate_hjm_model("hump")
    f_two_factor = simulate_hjm_model("two_factor")
    
    plt.figure(figsize=(10, 6))
    plt.plot(T_grid, f_constant[-1], 'b-', label='Constant Vol')
    plt.plot(T_grid, f_hump[-1], 'r-', label='Humped Vol')
    plt.plot(T_grid, f_two_factor[-1], 'g-', label='Two-Factor Vol')
    plt.plot(T_grid, initial_forward_curve(T_grid), 'k--', label='Initial Curve (t=0)')
    plt.xlabel('Maturity (T)')
    plt.ylabel('Forward Rate f(t_max,T)')
    plt.title(f'Forward Rate Curves at t={t_max} with Different Volatility Models')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    return f_constant, f_hump, f_two_factor

def show_curve_steepening_flattening(f):
    time_indices = [0, int(num_t/4), int(num_t/2), int(3*num_t/4), -1]
    
    plt.figure(figsize=(10, 6))
    for idx in time_indices:
        t = t_grid[idx]
        plt.plot(T_grid, f[idx], label=f't = {t:.2f}')
    plt.xlabel('Maturity (T)')
    plt.ylabel('Forward Rate f(t,T)')
    plt.title('Forward Rate Curve Steepening/Flattening Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Simulating HJM model with constant volatility...")
    f_constant = simulate_hjm_model("constant")
    
    plot_3d_surface(f_constant, "constant")
    
    ani = create_animation(f_constant, "constant")
    plt.show()
    
    show_curve_steepening_flattening(f_constant)
    
    f_constant, f_hump, f_two_factor = compare_volatility_models()
    
    plot_3d_surface(f_hump, "hump")
