import pandas as pd
rec = pd.read_csv('recovered_all.csv')
gdone = pd.read_csv('gender_cache.csv')
rec = rec.merge(gdone[['name','gender']].rename(columns={'name':'name_key'}), on='name_key', how='left')
rec['gender_final'] = rec['gender'].fillna('unknown')
rec[['hashed_author','recovered_first','name_key','gender','gender_final']].to_csv('recovered_gender.csv', index=False)
