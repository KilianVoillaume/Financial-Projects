"""
This code visualizes how interest rate shifts affect the present value of fixed and floating legs
in an interest rate swap. It demonstrates the concept of mark-to-market valuation by showing how
swap values evolve over different time horizons and in different interest rate environments.
The visualization illustrates why a swap that is initially at-market (zero value) can gain or
lose value as interest rates change, with the fixed leg and floating leg responding differently
to these changes. This sensitivity analysis is crucial for understanding swap pricing dynamics
and interest rate risk management.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def present_value_factor(rate, time):
    return 1 / ((1 + rate) ** time)

def pv_fixed_leg(notional, fixed_rate, payment_frequency, maturity, discount_curve):
    payments_per_period = notional * fixed_rate / payment_frequency
    payment_times = np.arange(payment_frequency, maturity + 0.01, payment_frequency)
    payment_indices = [int(round(t * payment_frequency)) - 1 for t in payment_times]
    
    discount_factors = [discount_curve[idx] for idx in payment_indices]
    present_values = payments_per_period * np.array(discount_factors)
    
    return np.sum(present_values)

def pv_floating_leg(notional, forward_curve, payment_frequency, maturity, discount_curve):
    payment_times = np.arange(payment_frequency, maturity + 0.01, payment_frequency)
    payment_indices = [int(round(t * payment_frequency)) - 1 for t in payment_times]
    
    pv = 0
    for i, idx in enumerate(payment_indices):
        rate = forward_curve[idx]
        payment = notional * rate / payment_frequency
        pv += payment * discount_curve[idx]
    
    return pv

def generate_yield_curve(base_rate, max_maturity, frequency, scenario="flat"):
    times = np.arange(1/frequency, max_maturity + 1/frequency, 1/frequency)
    
    if scenario == "flat":
        rates = np.ones_like(times) * base_rate
    elif scenario == "normal":
        # Normal upward sloping yield curve
        rates = base_rate + 0.005 * np.sqrt(times)
    elif scenario == "inverted":
        # Inverted yield curve
        rates = base_rate + 0.01 - 0.002 * times
    elif scenario == "steep":
        # Steep yield curve
        rates = base_rate + 0.015 * np.sqrt(times)
    else:
        rates = np.ones_like(times) * base_rate
    
    return times, rates

def generate_discount_curve(yield_curve, times, frequency):
    discount_factors = np.array([present_value_factor(rate, time) for rate, time in zip(yield_curve, times)])
    return discount_factors

def generate_forward_curve(discount_factors, frequency):
    forward_rates = []
    
    for i in range(len(discount_factors) - 1):
        if i == 0:
            rate = (1/discount_factors[0] - 1) * frequency
        else:
            rate = (discount_factors[i-1]/discount_factors[i] - 1) * frequency
        
        forward_rates.append(rate)
    
    last_rate = forward_rates[-1]
    forward_rates.append(last_rate)
    
    return np.array(forward_rates)

def plot_swap_valuation_sensitivity():
    notional = 1000000  # $1 million notional
    fixed_rate = 0.03  
    payment_frequency = 2  # Semi-annual payments
    max_maturity = 10   # Years
    
    # Time points to calculate PVs (every year)
    maturities = np.arange(1, max_maturity + 1)
    
    scenarios = {
        "Base Case": {"base_rate": 0.03, "curve": "normal"},
        "Rates +100bps": {"base_rate": 0.04, "curve": "normal"},
        "Rates -50bps": {"base_rate": 0.025, "curve": "normal"}
    }
    
    plt.figure(figsize=(12, 8))
    
    lines = []
    labels = []
    
    colors = {
        "Base Case": "#3366cc",
        "Rates +100bps": "#dc3912",
        "Rates -50bps": "#109618"
    }
    
    linestyles = {
        "Fixed": "-",
        "Floating": "--"
    }
    
    for scenario_name, scenario_params in scenarios.items():
        base_rate = scenario_params["base_rate"]
        curve_type = scenario_params["curve"]
        
        fixed_pvs = []
        floating_pvs = []
        
        for maturity in maturities:
            # Generate full yield curve for calculations
            times, rates = generate_yield_curve(base_rate, maturity, payment_frequency, curve_type)
            discount_factors = generate_discount_curve(rates, times, payment_frequency)
            forward_rates = generate_forward_curve(discount_factors, payment_frequency)
            
            fixed_pv = pv_fixed_leg(notional, fixed_rate, payment_frequency, maturity, discount_factors)
            floating_pv = pv_floating_leg(notional, forward_rates, payment_frequency, maturity, discount_factors)
            
            fixed_pvs.append(fixed_pv)
            floating_pvs.append(floating_pv)
        
        fixed_line, = plt.plot(maturities, fixed_pvs, 
                               color=colors[scenario_name], 
                               linestyle=linestyles["Fixed"],
                               linewidth=2.5)
        
        floating_line, = plt.plot(maturities, floating_pvs, 
                                  color=colors[scenario_name], 
                                  linestyle=linestyles["Floating"],
                                  linewidth=2.5)
        
        if scenario_name == "Base Case":
            lines.extend([fixed_line, floating_line])
            labels.extend([f"{scenario_name} - Fixed", f"{scenario_name} - Floating"])
        else:
            lines.append(fixed_line)
            labels.append(f"{scenario_name} - Fixed")
            lines.append(floating_line)
            labels.append(f"{scenario_name} - Floating")
    
    def currency_formatter(x, pos):
        return f"${x/1000:.0f}k"
    
    plt.gca().yaxis.set_major_formatter(FuncFormatter(currency_formatter))
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.title('Swap Valuation Sensitivity: Fixed vs Floating Leg', fontsize=16)
    plt.xlabel('Time to Maturity (Years)', fontsize=14)
    plt.ylabel('Present Value ($)', fontsize=14)
    
    plt.axhline(y=0, color='gray', linestyle='-', alpha=0.5)
    
    plt.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.13), 
               ncol=3, fontsize=12, frameon=True)
    
    for scenario_name, scenario_params in scenarios.items():
        swap_values = np.array(fixed_pvs) - np.array(floating_pvs)
        
        final_swap_value = swap_values[-1]
        plt.annotate(f"Swap Value: ${final_swap_value/1000:.1f}k",
                    xy=(max_maturity, final_swap_value), 
                    xytext=(max_maturity-2.5, final_swap_value + 5000),
                    arrowprops=dict(arrowstyle="->", color=colors[scenario_name]),
                    color=colors[scenario_name], fontsize=10)
    
    explanation = """Chart shows present value of fixed and floating legs under different rate scenarios:
- Base Case: Normal yield curve starting at 3%
- Rates +100bps: Yield curve shifted up by 1%
- Rates -50bps: Yield curve shifted down by 0.5%
Swap value = Fixed leg PV - Floating leg PV"""
    
    plt.figtext(0.5, -0.25, explanation, ha="center", fontsize=12, 
                bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)
    plt.show()

plot_swap_valuation_sensitivity()
