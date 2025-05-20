import numpy as np
import matplotlib.pyplot as plt

def opayoff(S0, K, premium, otype, position):
    if otype == "call":
        payoff = np.maximum(S0 - K, 0) - premium
    elif otype == "put":
        payoff = np.maximum(K - S0, 0) - premium
    else:
        raise ValueError("Option type must be a 'call' or a 'put'")
    if position == 'long':
        return payoff
    else:    #If short
        return -payoff

S0 = np.linspace(50, 150, 200)
K = 110
premium = 3  
breakeven_call = K + premium
breakeven_put = K - premium

long_call = opayoff(S0, K, premium, "call", "long")
short_call = opayoff(S0, K, premium, "call", "short")
long_put = opayoff(S0, K, premium, "put", "long")
short_put = opayoff(S0, K, premium, "put", "short")

fig, ax = plt.subplots(2, 2, figsize=(12, 8))

ax[0, 0].plot(S0, long_call, label="Long Call")
ax[0, 0].axvline(breakeven_call, linestyle="dotted", color="red", label="Breakeven")
ax[0, 0].annotate(f'{breakeven_call}', xy=(breakeven_call, ax[0, 0].get_ylim()[0]), xytext=(0, -15),
                  textcoords='offset points', color='red', ha='center')
ax[0, 0].set_title("Long Call: Payoff")
ax[0, 0].set_xlabel("Underlying Stock Price ($)")
ax[0, 0].set_ylabel("Payoff ($)")
ax[0, 0].grid()
ax[0, 0].legend()

ax[0, 1].plot(S0, short_call, label="Short Call")
ax[0, 1].axvline(breakeven_call, linestyle="dotted", color="red", label="Breakeven")
ax[0, 1].annotate(f'{breakeven_call}', xy=(breakeven_call, ax[0, 1].get_ylim()[0]), xytext=(0, -15),
                  textcoords='offset points', color='red', ha='center')
ax[0, 1].set_title("Short Call: Payoff")
ax[0, 1].set_xlabel("Underlying Stock Price ($)")
ax[0, 1].set_ylabel("Payoff ($)")
ax[0, 1].grid()
ax[0, 1].legend()

ax[1, 0].plot(S0, long_put, label="Long Put")
ax[1, 0].axvline(breakeven_put, linestyle="dotted", color="red", label="Breakeven")
ax[1, 0].annotate(f'{breakeven_put}', xy=(breakeven_put, ax[1, 0].get_ylim()[0]), xytext=(0, -15),
                  textcoords='offset points', color='red', ha='center')
ax[1, 0].set_title("Long Put: Payoff")
ax[1, 0].set_xlabel("Underlying Stock Price ($)")
ax[1, 0].set_ylabel("Payoff ($)")
ax[1, 0].grid()
ax[1, 0].legend()

ax[1, 1].plot(S0, short_put, label="Short Put")
ax[1, 1].axvline(breakeven_put, linestyle="dotted", color="red", label="Breakeven")
ax[1, 1].annotate(f'{breakeven_put}', xy=(breakeven_put, ax[1, 1].get_ylim()[0]), xytext=(0, -15),
                  textcoords='offset points', color='red', ha='center')
ax[1, 1].set_title("Short Put: Payoff")
ax[1, 1].set_xlabel("Underlying Stock Price ($)")
ax[1, 1].set_ylabel("Payoff ($)")
ax[1, 1].grid()
ax[1, 1].legend()

plt.tight_layout()
plt.show()

