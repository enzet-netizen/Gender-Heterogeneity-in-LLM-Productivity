import pandas as pd
oa = pd.read_csv('recovered_names.csv')
oa = oa[oa['recovered_first'].notna() & (oa['recovered_first'] != '')]
cr = pd.read_csv('recovered_crossref.csv')
cr = cr[cr['recovered_first'].notna() & (cr['recovered_first'] != '')]
rec = pd.concat([oa[['hashed_author','recovered_first']], cr[['hashed_author','recovered_first']]], ignore_index=True)
rec = rec.drop_duplicates(subset='hashed_author', keep='first')
rec['name_key'] = rec['recovered_first'].str.strip().str.lower()
rec.to_csv('recovered_all.csv', index=False)
