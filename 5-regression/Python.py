import pandas as pd
import numpy as np
import pyfixest as pf

panel = pd.read_csv('panel_gender_full.csv')

rel_vars = []
for c in panel.columns:
    if c.startswith('rel_month_pre_') or c.startswith('rel_month_post_'):
        if c.endswith('_treated'):
            rel_vars.append(c)

rhs = ''
for v in rel_vars:
    rhs = rhs + v + ' + '
rhs = rhs[:-3]  

fml = 'monthly_productivity ~ ' + rhs + ' | author_id + cohort_id^month_id + rel_month'


def run_es(df, name, outfile):
    model = pf.fepois(fml, data=df, vcov={'CRV1': 'author_id'})
    res = model.tidy()

    rel_month = []
    est = []
    se = []
    for var in res.index:
        if 'rel_month_pre_' in var:
            num = int(var.split('pre_')[1][:2])
            rel_month.append(-num)
            est.append(res.loc[var, 'Estimate'])
            se.append(res.loc[var, 'Std. Error'])
        elif 'rel_month_post_' in var:
            num = int(var.split('post_')[1][:2])
            rel_month.append(num)
            est.append(res.loc[var, 'Estimate'])
            se.append(res.loc[var, 'Std. Error'])

    out = pd.DataFrame()
    out['rel_month'] = rel_month
    out['estimate'] = est
    out['se'] = se
    out = out.sort_values('rel_month')
    out.to_csv(outfile, index=False)
    return out

male_df = panel[panel['gender_final'] == 'male']
run_es(male_df, 'Male', 'coefs_male_py.csv')

female_df = panel[panel['gender_final'] == 'female']
run_es(female_df, 'Female', 'coefs_female_py.csv')
