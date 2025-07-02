import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.lines as mlines

strike_price = 100
option_premium_vanilla = 5 
option_premium_digital = 0.4 * option_premium_vanilla 
digital_payoff = option_premium_vanilla * 2 

vanilla_breakeven = strike_price + option_premium_vanilla
digital_breakeven = strike_price + option_premium_digital/digital_payoff * (strike_price - 70)

underlying_prices = np.linspace(70, 130, 1000)

vanilla_payoffs = np.maximum(underlying_prices - strike_price, 0) - option_premium_vanilla
digital_payoffs = np.where(underlying_prices > strike_price, digital_payoff, 0) - option_premium_digital

fig, ax = plt.subplots(figsize=(12, 7))
fig.suptitle('Digital Call vs Vanilla Call Option: Net Payoff Comparison', fontsize=16)

colors = {'vanilla': '#1f77b4', 'digital': '#ff7f0e', 'zero': '#7f7f7f'}
line_width = 2.5

ax.plot(underlying_prices, vanilla_payoffs, 
        label=f'Vanilla Call (Premium: ${option_premium_vanilla})', 
        color=colors['vanilla'], linewidth=line_width)
ax.plot(underlying_prices, digital_payoffs, 
        label=f'Digital Call (Premium: ${option_premium_digital:.2f})', 
        color=colors['digital'], linewidth=line_width)

ax.axhline(y=0, color=colors['zero'], linestyle='-', alpha=0.3)
ax.axvline(x=strike_price, color='red', linestyle='--', alpha=0.5, label=f'Strike Price (K = ${strike_price})')

ax.axhline(y=-option_premium_vanilla, color=colors['vanilla'], linestyle=':', alpha=0.7)
ax.axhline(y=-option_premium_digital, color=colors['digital'], linestyle=':', alpha=0.7)

ax.annotate(f'Vanilla Premium: ${option_premium_vanilla}', 
            xy=(70, -option_premium_vanilla), 
            xytext=(72, -option_premium_vanilla - 1),
            arrowprops=dict(arrowstyle='->', color=colors['vanilla'], alpha=0.7))

ax.annotate(f'Digital Premium: ${option_premium_digital:.2f}', 
            xy=(70, -option_premium_digital), 
            xytext=(72, -option_premium_digital + 1),
            arrowprops=dict(arrowstyle='->', color=colors['digital'], alpha=0.7))

ax.annotate(f'Digital Fixed Payoff: ${digital_payoff}', 
           xy=(110, digital_payoff - option_premium_digital), 
           xytext=(105, digital_payoff - option_premium_digital + 3),
           arrowprops=dict(arrowstyle='->', color=colors['digital']))

ax.scatter(vanilla_breakeven, 0, color=colors['vanilla'], s=80, zorder=5)
ax.scatter(digital_breakeven, 0, color=colors['digital'], s=80, zorder=5)

ax.set_xlabel('Underlying Price at Expiration')
ax.set_ylabel('Profit/Loss')
ax.grid(True, alpha=0.3)

vanilla_breakeven_point = mlines.Line2D([], [], color=colors['vanilla'], marker='o', 
                                      linestyle='None', markersize=8, 
                                      label=f'Vanilla Break-even Point (${vanilla_breakeven:.2f})')

digital_breakeven_point = mlines.Line2D([], [], color=colors['digital'], marker='o', 
                                      linestyle='None', markersize=8, 
                                      label=f'Digital Break-even Point (${digital_breakeven:.2f})')

handles, labels = ax.get_legend_handles_labels()
handles.extend([vanilla_breakeven_point, digital_breakeven_point])
ax.legend(handles=handles, loc='upper left')

ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('$%.1f'))
plt.tight_layout()
plt.subplots_adjust(top=0.93)
plt.show()

print(f"Strike Price (K): ${strike_price}")
print(f"Vanilla Call Premium: ${option_premium_vanilla}")
print(f"Digital Call Premium: ${option_premium_digital:.2f}")
print(f"Digital Call Fixed Payoff: ${digital_payoff}")
print(f"Vanilla Call Break-even Price: ${vanilla_breakeven:.2f}")
print(f"Digital Call Break-even Price: ${digital_breakeven:.2f}")
