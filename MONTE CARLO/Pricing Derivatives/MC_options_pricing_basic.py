import math
import pandas as pd
import numpy as np
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt
import yfinance as yf

S = 101.15              
K = 98.01         
vol = 0.0991      
r = 0.01          
N = 10            # number of time steps (increased from 1 to 100)
M = 1000           # number of simulations

market_value = 3.86     # market value of the option
T = ((datetime.date(2022,3,17)-datetime.date(2022,1,17)).days+1)/365    #time in years to maturity    
print(T)


# ++++++++++++ SLOW SOLUTION - STEPS +++++++++++++
dt = T/N
nudt = (r - 0.5*vol**2)*dt
volsdt = vol*np.sqrt(dt)
lnS = np.log(S)

# Standard Error Placeholders
sum_CT = 0
sum_CT2 = 0

# Monte Carlo Method
for i in range(M):
    lnSt = lnS
    for j in range(N):
        lnSt = lnSt + nudt + volsdt*np.random.normal()
                  # Updates the log-price (lnSt) by adding the drift  (nudt) and a random shock (volsdt*np.random.normal()).

    ST = np.exp(lnSt)
      #Convert log price no normal price
    CT = max(0, ST - K)
    sum_CT = sum_CT + CT
    sum_CT2 = sum_CT2 + CT*CT

# Compute Expectation and SE
C0 = np.exp(-r*T)*sum_CT/M
      #Risk-neutral formula
sigma = np.sqrt( (sum_CT2 - sum_CT*sum_CT/M)*np.exp(-2*r*T) / (M-1) )
      #Standard deviation of the option price
SE = sigma/np.sqrt(M)
      #Computes the Standard Error of the estimated option price. 
      #The Standard Error measures the accuracy and reliability of your Monte Carlo estimate. Larger values of 𝑀 (number of simulations) typically reduce the SE, leading to a more precise estimation.

print("Slow Solution: Call value is ${0} with SE +/- {1}".format(np.round(C0,2),np.round(SE,2)))


#+++++++++++++ FAST SOUTION VECTORIZED ++++++++++++
dt = T/N
nudt = (r - 0.5*vol**2)*dt
volsdt = vol*np.sqrt(dt)
lnS = np.log(S)

# Monte Carlo Method
Z = np.random.normal(size=(N, M))
delta_lnSt = nudt + volsdt*Z
      #Computes the incremental changes in the log asset price for each step, including drift and randomness.
lnSt = lnS + np.cumsum(delta_lnSt, axis=0)
      #Converts incremental changes into cumulative log asset prices
lnSt = np.concatenate( (np.full(shape=(1, M), fill_value=lnS), lnSt ) )
      #Adds the initial log price to the beginning of the array

# Compute Expectation and SE
ST = np.exp(lnSt)
      #Compute back to normal price
CT = np.maximum(0, ST - K)
C0 = np.exp(-r*T)*np.sum(CT[-1])/M

sigma = np.sqrt( np.sum( (CT[-1] - C0)**2) / (M-1) )
SE = sigma/np.sqrt(M)

print("Fast Solution: Call value is ${0} with SE +/- {1}".format(np.round(C0,2),np.round(SE,2)))


"""
For simple processes where the SDE does not need to be approximated like in the case of Geometric Brownian Motion used for calculating a European Option Price, we can just simulate the variables at the final Time Step as Brownian Motion scales with time and independent increments.
"""
N = 1
dt = T/N
nudt = (r - 0.5*vol**2)*dt
volsdt = vol*np.sqrt(dt)
lnS = np.log(S)

# Monte Carlo
Z = np.random.normal(size=(N, M))
delta_lnSt = nudt + volsdt*Z
lnSt = lnS + np.cumsum(delta_lnSt, axis=0)
lnSt = np.concatenate( (np.full(shape=(1, M), fill_value=lnS), lnSt ) )

# Compute Expectation and SE
ST = np.exp(lnSt)
CT = np.maximum(0, ST - K)
C0 = np.exp(-r*T)*np.sum(CT[-1])/M

sigma = np.sqrt( np.sum( (CT[-1] - C0)**2) / (M-1) )
SE = sigma/np.sqrt(M)

print("1 time step: Call value is ${0} with SE +/- {1}".format(np.round(C0,2),np.round(SE,2)))


#++++++++++ VISUALISE CONVERGENCE +++++++++++++
x1 = np.linspace(C0-3*SE, C0-1*SE, 100)
x2 = np.linspace(C0-1*SE, C0+1*SE, 100)
x3 = np.linspace(C0+1*SE, C0+3*SE, 100)

s1 = stats.norm.pdf(x1, C0, SE)
s2 = stats.norm.pdf(x2, C0, SE)
s3 = stats.norm.pdf(x3, C0, SE)

plt.fill_between(x1, s1, color='tab:blue',label='> StDev')
plt.fill_between(x2, s2, color='cornflowerblue',label='1 StDev')
plt.fill_between(x3, s3, color='tab:blue')

plt.plot([C0,C0],[0, max(s2)*1.1], 'k',
        label='Theoretical Value')
plt.plot([market_value,market_value],[0, max(s2)*1.1], 'r',
        label='Market Value')

plt.ylabel("Probability")
plt.xlabel("Option Price")
plt.legend()
plt.show()


"""
Theoretical Value (Black Line)
This line shows the estimated fair value of the option calculated by the Monte Carlo simulation under the risk-neutral measure. It's the mean (expected value) of all simulated option payoffs discounted back to today.

Market Value (Red Line)
This line indicates the current market price of the option. Its position relative to the theoretical value provides insights:
If it’s close to the theoretical value, the market might be fairly valuing the option.
If it's far from the theoretical value, the option may be mispriced by the market (suggesting a potential trading opportunity).

Standard Deviation (blue regions)
Light Blue (±1 standard deviation) shows the range where ~68% of the simulated prices fall.
Dark Blue (>1 standard deviation) shows where the less likely outcomes fall (~32% total, ~16% in each tail).
"""
