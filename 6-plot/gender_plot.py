import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

coefs = pd.read_csv('gender_coefficients.csv')

coefs['pct']  = (np.exp(coefs['coef']) - 1) * 100
coefs['low']  = (np.exp(coefs['coef'] - 1.96*coefs['se']) - 1) * 100
coefs['high'] = (np.exp(coefs['coef'] + 1.96*coefs['se']) - 1) * 100

overall = coefs[coefs['group'] == 'Overall']['pct'].values[0]
bars    = coefs[coefs['group'] != 'Overall'].reset_index(drop=True)

COLORS = {'Male': '#4878A8', 'Female': '#C86464'}

fig, ax = plt.subplots(figsize=(5, 5))
for i, row in bars.iterrows():
    ax.bar(i, row['pct'], color=COLORS[row['group']], width=0.5)
    ax.errorbar(i, row['pct'],
                yerr=[[row['pct']-row['low']], [row['high']-row['pct']]],
                fmt='none', ecolor='black', capsize=5, lw=1.5)

ax.axhline(overall, ls='--', color='gray', lw=1.5, label=f'Overall ({overall:.1f}%)')
ax.set_xticks(range(len(bars)))
ax.set_xticklabels(bars['group'], size=13)
ax.set_ylabel('Changes in productivity', size=13)
ax.set_title('arXiv', size=14, fontweight='bold')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))
ax.set_ylim(0, 100)
ax.legend(fontsize=10, frameon=False)
plt.tight_layout()
plt.savefig('fig_gender_productivity.pdf')
plt.show()
