import pandas as pd
import matplotlib.pyplot as plt

panel = pd.read_csv('panel_gender_full.csv')
panel['group'] = panel['treated'].astype(str) + '_' + panel['gender_final']
avg = panel.groupby(['group','month'])['monthly_productivity'].mean().reset_index().sort_values('month')

for treated_flag, fname, title in [('0','fig_desc_nonadopters.png','Non-adopters: Male vs Female productivity (descriptive)'),
                                    ('1','fig_desc_adopters.png','Adopters: Male vs Female productivity (descriptive)')]:
    fig, ax = plt.subplots(figsize=(10,5))
    for g, color, label in [(treated_flag+'_male', '#4878A8', 'Male'),
                             (treated_flag+'_female', '#C86464', 'Female')]:
        sub = avg[avg['group']==g]
        ax.plot(range(len(sub)), sub['monthly_productivity'], color=color, linewidth=2, label=label)
    xtick_pos = list(range(0, len(avg[avg['group']==treated_flag+'_male']), 6))
    xtick_lab = avg[avg['group']==treated_flag+'_male']['month'].iloc[xtick_pos].tolist()
    ax.set_xticks(xtick_pos); ax.set_xticklabels(xtick_lab, rotation=45, ha='right')
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Avg. monthly productivity', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.legend(frameon=False)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    plt.show()
