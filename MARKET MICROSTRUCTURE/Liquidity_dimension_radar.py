import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

# Categories: Tightness, Depth, Immediacy, Resilience
dimensions = ['Tightness', 'Depth', 'Immediacy', 'Resilience']
n_dimensions = len(dimensions)

equities = [8, 7, 9, 6]  # Equities tend to have tight spreads, good depth, high immediacy, moderate resilience
credit = [5, 6, 4, 8]    # Credit markets typically have wider spreads, decent depth, lower immediacy, high resilience
crypto = [7, 4, 8, 3]    # Crypto often has reasonably tight spreads, less depth, high immediacy, low resilience

angles = np.linspace(0, 2*np.pi, n_dimensions, endpoint=False).tolist()
angles += angles[:1]  # Close the polygon

equities += equities[:1]
credit += credit[:1]
crypto += crypto[:1]
dimensions += dimensions[:1]

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

ax.plot(angles, equities, 'b-', linewidth=2, label='Equities')
ax.fill(angles, equities, 'b', alpha=0.1)

ax.plot(angles, credit, 'r-', linewidth=2, label='Credit')
ax.fill(angles, credit, 'r', alpha=0.1)

ax.plot(angles, crypto, 'g-', linewidth=2, label='Crypto')
ax.fill(angles, crypto, 'g', alpha=0.1)

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(dimensions[:-1], fontsize=12)

ax.set_ylim(0, 10)
ax.set_yticks(np.arange(2, 11, 2))
ax.set_yticklabels(np.arange(2, 11, 2), fontsize=10)
ax.grid(True)

ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), fontsize=12)
plt.title('Liquidity Dimensions Across Asset Classes', fontsize=15, y=1.1)

footnote = """
Tightness: Bid-ask spread size (higher score = tighter spreads)
Depth: Market's ability to absorb large orders without price impact
Immediacy: Speed of transaction execution
Resilience: How quickly market returns to equilibrium after a shock
"""
plt.figtext(0.65, 0.1, footnote, wrap=True, fontsize=10)

ax.grid(True, color='gray', linestyle='--', alpha=0.7)
ax.spines['polar'].set_visible(False)

plt.tight_layout()
plt.show()
