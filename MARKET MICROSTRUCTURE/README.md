# Market Microstructure Analysis – Depth, Impact & Liquidity

A suite of Python tools for visualising and understanding core concepts in market microstructure, including **order book depth**, **market impact**, and **multi-dimensional liquidity assessment** across asset classes.

---

## 📘 Related Article

This toolkit is developed in connection with:  
👉 **[Financial_Market_Uncovered_Article10_Market_Microstructure](https://github.com/KilianVoillaume/Financial_Market_Uncovered_Articles)**

---

## 🔍 Overview

This toolkit is designed to help students, traders, and researchers explore how market structure affects trading dynamics, price formation, and liquidity risk. It combines realistic visualisations with theoretical models to demonstrate:

- The relationship between **visible and hidden liquidity**
- The non-linear **market impact** of large orders
- The role of **liquidity dimensions** in comparing asset classes like equities, credit, and crypto

---

## 📘 Scripts Included

- **order_book_depth.py**  
  Simulates and visualises the cumulative visible and hidden depth on both sides of a limit order book. Demonstrates how shallow depth and iceberg orders influence execution and market impact for large trades.

- **market_impact_vs_trade_size.py**  
  Plots how market impact grows with trade size under varying liquidity regimes. Introduces liquidity-adjusted VaR (L-VaR) and compares it to standard VaR across position sizes.

- **liquidity_dimension_radar_plot.py**  
  Compares four key liquidity dimensions — tightness, depth, immediacy, and resilience — across asset classes using radar plots. Ideal for intuitive cross-asset market comparison.

---

## 🎯 Educational Goals

- Understand the mechanics of **order book construction**  
- Quantify how **market impact increases convexly** with trade size  
- Learn why **liquidity-adjusted risk models** are essential for large trades  
- Compare market quality across **equities, credit, and crypto**

---

*This toolkit is built for educational and analytical purposes only. It does not constitute trading advice or live execution infrastructure.* ⚠️
