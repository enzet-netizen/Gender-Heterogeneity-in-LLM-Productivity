import pandas as pd
import unicodedata

INPUT = 'panel.csv'
OUTPUT = 'authors_clean.csv'

ALLOWED_PUNCT = set("-'")

def classify(name):
    if pd.isna(name):
        return 'na', None
    name = str(name).strip()
    if not name:
        return 'na', None

    first_token = name.split()[0]
    if '.' in first_token:
        return 'initial', None

    core = first_token.replace('-', '').replace("'", '')
    if len(core) <= 1:
        return 'too_short', None

    if first_token[0] in ALLOWED_PUNCT or first_token[-1] in ALLOWED_PUNCT:
        return 'too_short', None

    for ch in first_token:
        if ch in ALLOWED_PUNCT:
            continue
        if not unicodedata.category(ch).startswith('L'):
            return 'nonalpha', None

    return 'keep', first_token.lower()

df = pd.read_csv(INPUT)
authors = df[['hashed_author']].drop_duplicates().reset_index(drop=True)
authors['first_name'] = authors['hashed_author'].str.split('|').str[-1]
ORDER = ['na', 'too_short', 'initial', 'nonalpha', 'keep']
counts = {k: 0 for k in ORDER}
tags, name_keys = [], []
for nm in authors['first_name']:
    tag, cleaned = classify(nm)
    counts[tag] += 1
    tags.append(tag)
    name_keys.append(cleaned)
authors['tag'] = tags
authors['name_key'] = name_keys

clean = authors.loc[authors['tag'] == 'keep',
                    ['hashed_author', 'first_name', 'name_key']].copy()
clean.to_csv(OUTPUT, index=False)

