import pandas as pd

PANEL  = 'panel.csv'
GENDER = 'authors_gender.csv'
OUTPUT = 'panel_gender.csv'

panel  = pd.read_csv(PANEL)
gender = pd.read_csv(GENDER)[['hashed_author', 'gender_final']]

panel = panel.merge(gender, on='hashed_author', how='left')
panel = panel[panel['gender_final'].isin(['male', 'female'])].copy()

panel['post'] = (panel['rel_month'] >= 1).astype(int)
panel['post_treated'] = panel['post'] * panel['treated']

panel = panel[panel['rel_month'] != 0].copy()

panel.to_csv(OUTPUT, index=False)

