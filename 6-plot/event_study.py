import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_coefs(path):
    c = pd.read_stata(path)
    rows = []
    for _, r in c.iterrows():
        name = str(r['coef'])
        if 'rel_month_pre_' in name:
            k = int(name.split('pre_')[1][:2])
            rows.append((-k, r['estimate'], r['se']))
        elif 'rel_month_post_' in name:
            k = int(name.split('post_')[1][:2])
            rows.append((k, r['estimate'], r['se']))
    df = pd.DataFrame(rows, columns=['rel_month','beta','se'])
    df = pd.concat([df, pd.DataFrame([{'rel_month': -1, 'beta': 0.0, 'se': 0.0}])])
    df = df.sort_values('rel_month').reset_index(drop=True)
    df['pct']    = (np.exp(df['beta']) - 1) * 100
    df['pct_lo'] = (np.exp(df['beta'] - 1.96*df['se']) - 1) * 100
    df['pct_hi'] = (np.exp(df['beta'] + 1.96*df['se']) - 1) * 100
    return df

def plot_es(df, title, outfile, color, marker):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.yaxis.grid(True, color='#CCCCCC', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.axhline(0, color='black', linewidth=1.8, zorder=2)
    ax.axvline(0, color='black', linestyle='--', linewidth=1.2, zorder=2)
    ax.errorbar(df['rel_month'], df['pct'],
                yerr=[df['pct']-df['pct_lo'], df['pct_hi']-df['pct']],
                fmt=marker, color=color, ecolor=color,
                markersize=7, capsize=0, elinewidth=1.5, zorder=3)
    ax.set_xlabel('Months relative to first adoption', fontsize=12, fontweight='bold')
    ax.set_ylabel('Change in productivity (%)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xticks([-12, -6, 0, 6, 12, 18])
    ax.set_xlim(-13, 18.8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(outfile, dpi=300, bbox_inches='tight')
    plt.show()

dm = load_coefs('coefs_male.dta')
plot_es(dm, 'Male: LLM adopters vs non-adopters', 'fig_es_male.png', '#4878A8', 'o')
df_ = load_coefs('coefs_female.dta')
plot_es(df_, 'Female: LLM adopters vs non-adopters', 'fig_es_female.png', '#C86464', 's')
