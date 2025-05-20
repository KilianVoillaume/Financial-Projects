import numpy as np
from scipy.stats import norm
import blackscholes as bs

def N(x):
      return norm.cdf(x)

def black_scholes(S0, K, T, r, sigma, Q, type='call'):
      d1 = (np.log(S0/K) + (r - Q + 0.5 * sigma**2.0) * T) / (sigma * np.sqrt(T))
      d2 = d1 - sigma * np.sqrt(T)
      if type == 'call':
          return S0 * np.exp(-Q*T) * N(d1) - K * np.exp(-r*T) * N(d2)
      elif type == 'put':
          return K * np.exp(-r*T) * N(-d2) - S0 * np.exp(-Q*T) * N(-d1)
      else:
          raise ValueError("Option type not valid")

S0 = 100.0
K = 110.0
T = 1.0
r = 0.05
sigma = 0.2
Q = 0.50

ref_call = bs.BlackScholesCall(S0, K, T, r, sigma, Q)
ref_call_price = ref_call.price()

ref_put = bs.BlackScholesPut(S0, K, T, r, sigma, Q)
ref_put_price = ref_put.price()

our_call = black_scholes(S0, K, T, r, sigma, Q, type='call')
our_put = black_scholes(S0, K, T, r, sigma, Q, type='put')

print()
print("Our call is " + str(our_call) + "\nThe reference call is " + str(ref_call_price))
print("Our call difference is " + str(our_call - ref_call_price))
print()
print("Our put is " + str(our_put) + "\nThe reference put is " + str(ref_put_price))
print("Our put difference is " + str(our_put - ref_put_price))
print()


