import pandas as pd

PANEL  = 'panel.csv'
GENDER = 'authors_gender_full.csv'
OUTPUT = 'panel_gender_full.csv'

panel  = pd.read_csv(PANEL)
gender = pd.read_csv(GENDER)

panel = panel.merge(gender, on='hashed_author', how='left')
panel = panel[panel['gender_final'].isin(['male','female'])].copy()

panel.to_csv(OUTPUT, index=False)

