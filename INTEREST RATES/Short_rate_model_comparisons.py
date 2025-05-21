import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.stats import norm
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("talk")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['lines.linewidth'] = 2.5

# Set random seed for reproducibility
np.random.seed(42)

T = 10.0         # Tears
N = 1000        
dt = T / N       
paths = 5      

r0 = 0.03        # Initial short rate 
kappa = 0.5      # Mean reversion speed
theta = 0.05     # Long-term mean rate 
sigma = 0.02     # Volatility

time_grid = np.linspace(0, T, N+1)

# Sample paths for the Vasicek model
def vasicek_model(r0, kappa, theta, sigma, T, N, paths):
    dt = T / N
    r = np.zeros((paths, N+1))
    r[:, 0] = r0
    for i in range(paths):
        dW = np.random.normal(0, np.sqrt(dt), N)
        for t in range(N):
            dr = kappa * (theta - r[i, t]) * dt + sigma * dW[t]
            r[i, t+1] = r[i, t] + dr
    return r

# Sample paths for the CIR model
def cir_model(r0, kappa, theta, sigma, T, N, paths):
    dt = T / N
    r = np.zeros((paths, N+1))
    r[:, 0] = r0
    for i in range(paths):
        dW = np.random.normal(0, np.sqrt(dt), N)
        for t in range(N):
            dr = kappa * (theta - r[i, t]) * dt + sigma * np.sqrt(max(r[i, t], 0)) * dW[t]
            r[i, t+1] = max(r[i, t] + dr, 0)  # Ensure rates don't go negative
    return r

# Function for Hull-White with time-dependent drift
def hull_white_model(r0, kappa, sigma, T, N, paths):
    dt = T / N
    r = np.zeros((paths, N+1))
    r[:, 0] = r0

    def theta_t(t):
        if t < T/2:
            return 0.04  # 4% initially
        else:
            return 0.06  # 6% later
    
    theta_values = np.array([theta_t(t) for t in time_grid])
    for i in range(paths):
        dW = np.random.normal(0, np.sqrt(dt), N)
        for t in range(N):
            theta_current = theta_values[t]
            dr = kappa * (theta_current - r[i, t]) * dt + sigma * dW[t]
            r[i, t+1] = r[i, t] + dr
    return r, theta_values

# Sample paths
vasicek_paths = vasicek_model(r0, kappa, theta, sigma, T, N, paths)
cir_paths = cir_model(r0, kappa, theta, sigma, T, N, paths)
hull_white_paths, hw_theta = hull_white_model(r0, kappa, sigma, T, N, paths)


# Vasicek Model
fig_vasicek = plt.figure(figsize=(12, 8))
ax_vasicek = fig_vasicek.add_subplot(111)
for i in range(paths):
    ax_vasicek.plot(time_grid, vasicek_paths[i], alpha=0.8)
ax_vasicek.axhline(y=theta, color='r', linestyle='--', label=f'Long-term mean rate ({theta:.1%})')
ax_vasicek.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax_vasicek.set_title('Vasicek Model Sample Paths')
ax_vasicek.set_ylabel('Short Rate (r)')
ax_vasicek.set_xlabel('Time (years)')
ax_vasicek.yaxis.set_major_formatter(PercentFormatter(1.0))
ax_vasicek.grid(True)
ax_vasicek.legend()
ax_vasicek.annotate('Can go negative', xy=(8, -0.01), xytext=(6, -0.03),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))

props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
ax_vasicek.text(0.02, 0.95, r'$dr(t) = \kappa(\theta - r(t))dt + \sigma dW(t)$', 
                transform=ax_vasicek.transAxes, fontsize=12,
                verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('vasicek_model.png', dpi=300, bbox_inches='tight')
plt.show()


# CIR Model
fig_cir = plt.figure(figsize=(12, 8))
ax_cir = fig_cir.add_subplot(111)
for i in range(paths):
    ax_cir.plot(time_grid, cir_paths[i], alpha=0.8)
ax_cir.axhline(y=theta, color='r', linestyle='--', label=f'Long-term mean rate ({theta:.1%})')
ax_cir.set_title('CIR Model Sample Paths')
ax_cir.set_ylabel('Short Rate (r)')
ax_cir.set_xlabel('Time (years)')
ax_cir.yaxis.set_major_formatter(PercentFormatter(1.0))
ax_cir.grid(True)
ax_cir.legend()
ax_cir.annotate('Non-negative', xy=(8, 0.01), xytext=(6, 0.03),
               arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))

ax_cir.text(0.02, 0.95, r'$dr(t) = \kappa(\theta - r(t))dt + \sigma\sqrt{r(t)} dW(t)$', 
            transform=ax_cir.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('cir_model.png', dpi=300, bbox_inches='tight')
plt.show()


# Hull-White Model
fig_hw = plt.figure(figsize=(12, 8))
ax_hw = fig_hw.add_subplot(111)

for i in range(paths):
    ax_hw.plot(time_grid, hull_white_paths[i], alpha=0.8)
ax_hw.plot(time_grid, hw_theta, 'r--', label='Time-varying mean')
ax_hw.axhline(y=0, color='black', linestyle='-', alpha=0.3)
ax_hw.set_title('Hull-White Model Sample Paths')
ax_hw.set_xlabel('Time (years)')
ax_hw.set_ylabel('Short Rate (r)')
ax_hw.yaxis.set_major_formatter(PercentFormatter(1.0))
ax_hw.grid(True)
ax_hw.legend()
ax_hw.annotate('Time-dependent\nlong-term mean', xy=(5, hw_theta[500]+0.01), xytext=(3, hw_theta[500]+0.03),
               arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
ax_hw.text(0.02, 0.95, r'$dr(t) = \kappa(\theta(t) - r(t))dt + \sigma dW(t)$', 
           transform=ax_hw.transAxes, fontsize=12,
           verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('hull_white_model.png', dpi=300, bbox_inches='tight')
plt.show()

plt.figure(figsize=(14, 8))

many_paths = 1000
vasicek_many = vasicek_model(r0, kappa, theta, sigma, T, N, many_paths)
cir_many = cir_model(r0, kappa, theta, sigma, T, N, many_paths)
hull_white_many, _ = hull_white_model(r0, kappa, sigma, T, N, many_paths)

# Terminal distributions
sns.kdeplot(vasicek_many[:, -1], label='Vasicek', fill=True, alpha=0.3)
sns.kdeplot(cir_many[:, -1], label='CIR', fill=True, alpha=0.3)
sns.kdeplot(hull_white_many[:, -1], label='Hull-White', fill=True, alpha=0.3)

plt.axvline(x=theta, color='r', linestyle='--', label=f'Long-term mean rate ({theta:.1%})')
plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
plt.title(f'Terminal Distribution of Short Rates at T={T}')
plt.xlabel('Short Rate (r)')
plt.ylabel('Density')
plt.gca().xaxis.set_major_formatter(PercentFormatter(1.0))
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('short_rate_terminal_distributions.png', dpi=300, bbox_inches='tight')
plt.show()

plt.figure(figsize=(14, 8))

# Rolling volatility to show different volatility behaviors
window = 50  # Rolling window size
v_vol = np.zeros((paths, N-window+1))
c_vol = np.zeros((paths, N-window+1))
hw_vol = np.zeros((paths, N-window+1))

for i in range(paths):
    for t in range(N-window+1):
        v_vol[i, t] = np.std(np.diff(vasicek_paths[i, t:t+window]))
        c_vol[i, t] = np.std(np.diff(cir_paths[i, t:t+window]))
        hw_vol[i, t] = np.std(np.diff(hull_white_paths[i, t:t+window]))

plt.plot(time_grid[window:], np.mean(v_vol, axis=0), label='Vasicek')
plt.plot(time_grid[window:], np.mean(c_vol, axis=0), label='CIR')
plt.plot(time_grid[window:], np.mean(hw_vol, axis=0), label='Hull-White')

plt.title('Rolling Volatility Comparison')
plt.xlabel('Time (years)')
plt.ylabel('Rolling Volatility')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('short_rate_volatility_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

print("Model Parameters:")
print(f"Initial rate (r0): {r0:.2%}")
print(f"Mean reversion speed (kappa): {kappa:.2f}")
print(f"Long-term mean rate (theta): {theta:.2%}")
print(f"Volatility (sigma): {sigma:.2%}")
print("\nKey Model Characteristics:")
print("1. Vasicek: Constant volatility, can have negative rates")
print("2. CIR: Square-root diffusion process, non-negative rates")
print("3. Hull-White: Time-varying drift, extension of Vasicek")
