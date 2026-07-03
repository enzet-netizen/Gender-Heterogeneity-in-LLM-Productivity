import pandas as pd
orig = pd.read_csv('authors_gender.csv')[['hashed_author','gender_final']]
rec  = pd.read_csv('recovered_gender.csv')[['hashed_author','gender_final']]
combined = pd.concat([orig, rec], ignore_index=True)
combined['is_known'] = combined['gender_final'].isin(['male','female'])
combined = combined.sort_values('is_known', ascending=False)
combined = combined.drop_duplicates(subset='hashed_author', keep='first')
combined[['hashed_author','gender_final']].to_csv('authors_gender_full.csv', index=False)
