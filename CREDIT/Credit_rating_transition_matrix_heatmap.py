import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for the visualization
sns.set(style="white")

"""
Credit Rating Transition Matrix Visualization

This script generates a synthetic 1-year transition matrix for credit ratings
from AAA to Default. The matrix shows the probability of a company transitioning 
from one credit rating to another over a one-year period. Key characteristics of
this matrix include diagonal dominance (ratings tend to persist), higher stability
for better ratings, higher default probabilities for lower ratings, and a slight
bias toward downgrades versus upgrades.

Credit rating transition matrices are essential tools for risk management and 
credit portfolio analysis. They represent the likelihood of credit migration 
between different rating categories over a specified time horizon. Financial 
institutions use these matrices for various applications including economic 
capital calculations, credit value-at-risk models, and pricing of credit 
derivatives. The visualization below helps analysts quickly identify patterns 
and potential areas of concern in credit quality migration.
"""

# Define the ratings
ratings = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'Default']

# Higher probabilities on diagonal (staying in same rating)
# Lower probabilities for big jumps in ratings
# Slightly higher probabilities for downgrades than upgrades
transition_matrix = np.array([
    [0.9045, 0.0850, 0.0070, 0.0025, 0.0007, 0.0002, 0.0001, 0.0000],  # AAA
    [0.0084, 0.9120, 0.0684, 0.0075, 0.0022, 0.0010, 0.0003, 0.0002],  # AA
    [0.0007, 0.0230, 0.9140, 0.0520, 0.0070, 0.0023, 0.0007, 0.0003],  # A
    [0.0002, 0.0035, 0.0550, 0.8860, 0.0420, 0.0098, 0.0025, 0.0010],  # BBB
    [0.0001, 0.0008, 0.0055, 0.0720, 0.8330, 0.0740, 0.0110, 0.0036],  # BB
    [0.0000, 0.0003, 0.0015, 0.0068, 0.0790, 0.8370, 0.0650, 0.0104],  # B
    [0.0000, 0.0001, 0.0005, 0.0022, 0.0098, 0.0760, 0.8264, 0.0850],  # CCC
    [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.0000],  # Default (absorbing state)
])

row_sums = transition_matrix.sum(axis=1)
print("Row sums:", row_sums)

df_transition = pd.DataFrame(transition_matrix, index=ratings, columns=ratings)

plt.figure(figsize=(14, 12))

colors = ["#FFFFFF", "#EBF5FB", "#AED6F1", "#3498DB", "#1A5276"]  # White to dark blue gradient
cmap_transitions = sns.color_palette(colors, as_cmap=True)

diag_colors = ["#FF7043", "#E64A19", "#BF360C"]  # Stronger orange/red for diagonals
cmap_diagonal = sns.color_palette(diag_colors, as_cmap=True)

default_color = "#581845"  # Dark purple for 100% default

visualization_matrix = transition_matrix.copy()

ax = sns.heatmap(
    df_transition,
    annot=True,                     
    fmt='.1%',                
    cmap=cmap_transitions,           
    linewidths=0.8,                 
    cbar_kws={
        'label': 'Transition Probability',
        'shrink': 0.8
    },
    vmin=0,                         
    vmax=0.15                     
)

mask_diag = np.zeros_like(transition_matrix, dtype=bool)
np.fill_diagonal(mask_diag, True)

diag_df = pd.DataFrame(np.zeros_like(transition_matrix), index=ratings, columns=ratings)
for i in range(len(ratings)-1):  # Exclude Default state
    diag_df.iloc[i, i] = transition_matrix[i, i]

sns.heatmap(
    diag_df.iloc[:-1, :-1],  # Exclude Default state
    mask=~mask_diag[:-1, :-1],  # Apply mask (inverse)
    cmap=cmap_diagonal,
    linewidths=0.8,
    annot=True,
    fmt='.1%',
    cbar=False,
    ax=ax
)

default_df = pd.DataFrame(np.zeros_like(transition_matrix), index=ratings, columns=ratings)
default_df.iloc[-1, -1] = 1.0  # 100% for Default->Default

default_mask = np.ones_like(transition_matrix, dtype=bool)
default_mask[-1, -1] = False

sns.heatmap(
    default_df,
    mask=default_mask,
    cmap=sns.light_palette(default_color, as_cmap=True),
    linewidths=0.8,
    annot=True,
    fmt='.1%',
    cbar=False,
    ax=ax
)

plt.title('1-Year Credit Rating Transition Matrix', fontsize=18, pad=20)
plt.xlabel('Future Rating', fontsize=16, labelpad=10)
plt.ylabel('Current Rating', fontsize=16, labelpad=10)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.xticks(rotation=0)

plt.tight_layout()

plt.figtext(0.5, 0.01, 
           "Key observations: (1) Diagonal dominance shows rating stability, (2) Higher ratings show greater stability,\n" +
           "(3) Transitions typically occur to adjacent ratings, (4) Default probability increases at lower ratings.",
           ha="center", fontsize=11, bbox={"facecolor":"aliceblue", "alpha":0.5, "pad":5})

plt.savefig('credit_rating_transition_matrix.png', dpi=300, bbox_inches='tight')

plt.show()

print("\nCredit Rating Transition Matrix (probabilities):")
pd.options.display.float_format = '{:.2%}'.format
print(df_transition)
