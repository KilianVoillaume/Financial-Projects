import autograd.numpy as np  
from autograd.scipy.stats import norm  
from autograd import grad 

def N(x):
    return norm.cdf(x)

def black_scholes(S0, K, T, r, sigma, Q, option_type='call'):
    d1 = (np.log(S0 / K) + (r - Q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        return S0 * np.exp(-Q * T) * N(d1) - K * np.exp(-r * T) * N(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * N(-d2) - S0 * np.exp(-Q * T) * N(-d1)
    else:
        raise ValueError("Invalid option type. Choose 'call' or 'put'.")

def value_loss(S0, K, T, r, sigma_guess, Q, market_price, option_type='call'):
    return black_scholes(S0, K, T, r, sigma_guess, Q, option_type) - market_price

loss_grad = grad(value_loss, argnum=4)  

def implied_volatility(S0, K, T, r, market_price, Q, sigma_guess=1.2, tol=1e-6, max_iter=50, verbose=True):
    IV = sigma_guess  
    for i in range(max_iter):
        loss = value_loss(S0, K, T, r, IV, Q, market_price, option_type='call')
        
        if verbose:
            print(f"Iteration {i+1}: Sigma = {IV:.8f}, Loss = {loss:.8f}")
        if abs(loss) < tol:  # If the loss is small enough, we have converged
            break
        grad_loss = loss_grad(S0, K, T, r, IV, Q, market_price)
        if grad_loss == 0:  
            raise ValueError("Gradient is zero, Newton's method failed to converge.")

        IV = IV - loss / grad_loss  # Newton's update step

    return IV


S0 = 110  
K = 100  
T = 2  
r = 0.2 
sigma_guess = 0.15  
Q = 0  

# Compute the market price using Black-Scholes
market_price = black_scholes(S0, K, T, r, sigma_guess, Q, option_type='call')
print(f"\nTheoretical market price: {market_price:.3f}\n")

# Compute implied volatility
calculated_IV = implied_volatility(S0, K, T, r, market_price, Q, sigma_guess=1.8)
print(f"\nEstimated Implied Volatility: {calculated_IV:.5f}\n")


