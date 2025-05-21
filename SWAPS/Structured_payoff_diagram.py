import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import matplotlib.ticker as mtick

def reverse_convertible_payoff(spot_prices, initial_price, coupon, barrier):
    payoffs = np.ones_like(spot_prices) * (1 + coupon)  # Principal + Coupon
    
    # If final price is below barrier, investor receives asset instead of full principal
    barrier_value = initial_price * barrier
    below_barrier = spot_prices < barrier_value
    
    # When below barrier, payoff becomes: (spot_price/initial_price) + coupon
    payoffs[below_barrier] = (spot_prices[below_barrier] / initial_price) + coupon
    
    return payoffs

def autocallable_payoff(spot_prices, initial_price, coupons, trigger_levels, observation_periods, final_barrier):
    final_period_coupon = coupons[-1]
    final_trigger = trigger_levels[-1]
    max_coupon = sum(coupons)  
    
    payoffs = np.zeros_like(spot_prices)
    
    # Above final trigger level - full principal plus all coupons
    above_trigger = spot_prices >= initial_price * final_trigger
    payoffs[above_trigger] = 1 + max_coupon
    
    # Between barrier and trigger - principal returned plus only final coupon
    between_barrier_and_trigger = (spot_prices >= initial_price * final_barrier) & (spot_prices < initial_price * final_trigger)
    payoffs[between_barrier_and_trigger] = 1 + final_period_coupon
    
    # Below barrier - principal at risk, proportional to underlying performance
    below_barrier = spot_prices < initial_price * final_barrier
    payoffs[below_barrier] = spot_prices[below_barrier] / initial_price
    
    return payoffs

def capital_protected_note_payoff(spot_prices, initial_price, participation_rate, capital_protection):
    performance = spot_prices / initial_price - 1
    payoffs = np.ones_like(spot_prices) * capital_protection
    positive_perf = performance > 0
    payoffs[positive_perf] = capital_protection + (performance[positive_perf] * participation_rate)
    
    return payoffs

def plot_structured_products():
    initial_price = 100
    price_range = np.linspace(initial_price * 0.5, initial_price * 1.5, 1000)
    price_percent = price_range / initial_price
    
    fig, axs = plt.subplots(3, 1, figsize=(12, 26))
    
    # 1. Reverse Convertible
    coupon = 0.12  # 12% coupon
    barrier = 0.75  # 75% barrier
    
    rc_payoffs = reverse_convertible_payoff(price_range, initial_price, coupon, barrier)
    
    axs[0].plot(price_percent, rc_payoffs, 'b-', linewidth=3)
    axs[0].plot(price_percent, price_percent, 'k--', alpha=0.5, label='Underlying Asset')
    axs[0].plot([0, 2], [1, 1], 'k:', alpha=0.5, label='Principal')
    
    axs[0].axvline(x=barrier, color='r', linestyle='--', alpha=0.7, 
                 label=f'Barrier ({barrier*100:.0f}%)')
    axs[0].fill_between(price_percent, 1, 1+coupon, 
                      where=(price_percent >= barrier),
                      alpha=0.2, color='green', label=f'Coupon ({coupon*100:.0f}%)')
    axs[0].fill_between(price_percent, price_percent, 1,
                      where=(price_percent < barrier),
                      alpha=0.2, color='red', label='Capital at Risk')
    axs[0].set_title('Reverse Convertible Payoff Diagram', fontsize=16, fontweight='bold')
    axs[0].grid(True, alpha=0.3)
    axs[0].legend(loc='upper right', fontsize=8, framealpha=0.9)
    axs[0].set_xlim(0.5, 1.5)
    axs[0].set_ylim(0.5, 1.25)
    axs[0].xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axs[0].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    axs[0].annotate('Fixed coupon regardless\nof underlying performance\nif above barrier', 
                   xy=(1, 1.12), xytext=(1.03, 0.85),
                   fontsize=9, ha='center',  
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    axs[0].annotate('Below barrier:\nReceive depreciated\nshares/value + coupon', 
                   xy=(0.65, 0.75), xytext=(0.6, 0.9),
                   fontsize=9, ha='center',  
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
                   arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
    
    # 2. Autocallable
    coupons = [0.035, 0.07, 0.105, 0.14] 
    trigger_levels = [1.0, 0.95, 0.9, 0.85]  # Autocall triggers
    observation_periods = 4
    final_barrier = 0.6  # 60% final barrier
    
    auto_payoffs = autocallable_payoff(price_range, initial_price, coupons, trigger_levels, 
                                     observation_periods, final_barrier)
    
    axs[1].plot(price_percent, auto_payoffs, 'g-', linewidth=3)
    axs[1].plot(price_percent, price_percent, 'k--', alpha=0.5, label='Underlying Asset')
    axs[1].plot([0, 2], [1, 1], 'k:', alpha=0.5, label='Principal')
    axs[1].axvline(x=final_barrier, color='r', linestyle='--', alpha=0.7, 
                 label=f'Barrier ({final_barrier*100:.0f}%)')
    axs[1].axvline(x=trigger_levels[-1], color='b', linestyle='--', alpha=0.7,
                 label=f'Final Trigger ({trigger_levels[-1]*100:.0f}%)') 
    axs[1].fill_between(price_percent, 1, 1+sum(coupons),
                      where=(price_percent >= trigger_levels[-1]),
                      alpha=0.2, color='green', label=f'Max Coupon ({sum(coupons)*100:.0f}%)')
    axs[1].fill_between(price_percent, 1, 1+coupons[-1],
                      where=(price_percent >= final_barrier) & (price_percent < trigger_levels[-1]),
                      alpha=0.2, color='yellow', label=f'Final Coupon ({coupons[-1]*100:.0f}%)')
    axs[1].fill_between(price_percent, price_percent, 1,
                      where=(price_percent < final_barrier),
                      alpha=0.2, color='red', label='Capital at Risk')
    axs[1].set_title('Autocallable Product Payoff Diagram (Final Observation)', fontsize=16, fontweight='bold')
    axs[1].grid(True, alpha=0.3)
    axs[1].legend(loc='upper right', fontsize=8, framealpha=0.9)
    axs[1].set_xlim(0.5, 1.5)
    axs[1].set_ylim(0.5, 1.25)
    axs[1].xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axs[1].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    axs[1].annotate('Above trigger:\nFull principal + all coupons', 
                   xy=(1.07, 1.16), xytext=(1.07, 1.06),
                   fontsize=9, ha='center', 
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    axs[1].annotate('Between barrier and trigger:\nPrincipal + final coupon', 
                   xy=(0.75, 1.12), xytext=(0.72, 0.97),
                   fontsize=9, ha='center',  
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
                   arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.2"))
    
    axs[1].annotate('Below barrier:\nCapital at risk', 
                   xy=(0.55, 0.55), xytext=(0.54, 0.65),
                   fontsize=9, ha='center',  
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
                   arrowprops=dict(arrowstyle='->'))
    
    # 3. Capital Protected Note
    participation_rate = 0.7  # 70% participation
    capital_protection = 0.9  # 90% capital protection
    
    cpn_payoffs = capital_protected_note_payoff(price_range, initial_price, 
                                             participation_rate, capital_protection)
    
    axs[2].plot(price_percent, cpn_payoffs, 'purple', linewidth=3)
    axs[2].plot(price_percent, price_percent, 'k--', alpha=0.5, label='Underlying Asset')
    axs[2].plot([0, 2], [1, 1], 'k:', alpha=0.5, label='Principal') 
    axs[2].axhline(y=capital_protection, color='g', linestyle='--', alpha=0.7,
                 label=f'Capital Protection ({capital_protection*100:.0f}%)')
    axs[2].axvline(x=1.0, color='b', linestyle='--', alpha=0.7, label='Initial Price')
    axs[2].fill_between(price_percent, 0, capital_protection, 
                      alpha=0.2, color='green', label='Protected Capital')
    axs[2].fill_between(price_percent, capital_protection, cpn_payoffs,
                      where=(price_percent > 1),
                      alpha=0.2, color='blue', 
                      label=f'Participation ({participation_rate*100:.0f}%)')
    axs[2].set_title('Capital Protected Note Payoff Diagram', fontsize=16, fontweight='bold')
    axs[2].grid(True, alpha=0.3)
    axs[2].legend(loc='upper right', fontsize=8, framealpha=0.9)
    axs[2].set_xlim(0.5, 1.5)
    axs[2].set_ylim(0.5, 1.3)
    axs[2].xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axs[2].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    axs[2].annotate('Capital protection floor', 
                   xy=(0.7, capital_protection), xytext=(0.8, capital_protection - 0.15),
                   fontsize=9, ha='center', 
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
                   arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.1"))
    
    axs[2].annotate(f'Participation: {participation_rate*100:.0f}% of\nunderlying appreciation', 
                   xy=(1.3, 1.15), xytext=(1.1, 1.1),
                   fontsize=9, ha='center', 
                   bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
                   arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-.1"))
    
    for ax in axs:
        ax.set_xlabel('Underlying Asset Price at Maturity (% of Initial)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Payoff (% of Principal)', fontsize=12, fontweight='bold')
        
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.set_facecolor('#f8f9fa')
    
    fig.suptitle('Structured Product Payoff Diagrams', fontsize=20, y=0.995)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2, hspace=0.6, top=0.9)
    plt.show()

plot_structured_products()
