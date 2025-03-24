# Option Payoff Visualization

This repository contains a Python script to visualize the payoffs of different option strategies, including long and short calls and puts. The script calculates and plots the payoff diagrams to help understand option pricing and risk.

## Features
- Computes payoffs for:
  - Long Call
  - Short Call
  - Long Put
  - Short Put
- Displays breakeven points on the payoff graphs
- Uses Matplotlib for visualization

## Requirements
Make sure you have the following dependencies installed:

```bash
pip install numpy matplotlib
```

## Code overview
The script performs the following tasks:
- Defines an opayoff function to compute the payoff of an option contract.
- Sets parameters for option pricing, including:
  - **Strike price**
  - **Option premium**
  - **Range of underlying stock prices**
- Computes payoffs for different positions (long/short call and put).
- Uses Matplotlib to plot the payoff diagrams.

# AUTHOR
Kilian Voillaume 
