import pandas as pd

INPUT = 'authors_clean.csv'
CACHE = 'gender_cache.csv'
OUTPUT = 'authors_gender.csv'

authors = pd.read_csv(INPUT)         
gender  = pd.read_csv(CACHE)        

merged = authors.merge(
    gender.rename(columns={'name': 'name_key'}),
    on='name_key', how='left'
)

merged['gender_final'] = merged['gender'].fillna('unknown')

out = merged[['hashed_author', 'first_name', 'name_key',
              'gender', 'probability', 'count', 'gender_final']]
out.to_csv(OUTPUT, index=False)

