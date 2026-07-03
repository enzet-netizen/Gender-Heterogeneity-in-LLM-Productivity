import pandas as pd
import requests, time, os, unicodedata

DOI_FILE  = 'removed_with_doi.csv'
OA_RESULT = 'recovered_names.csv'
OUTPUT    = 'recovered_crossref.csv'
EMAIL     = ''

def norm(s):
    if not s: return ''
    s = unicodedata.normalize('NFKD', str(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return ''.join(c for c in s.lower() if c.isalnum())

def crossref_fullname(doi, target_last, email):
    url = f"https://api.crossref.org/works/{doi}"
    try:
        r = requests.get(url, params={'mailto': email}, timeout=20)
        if r.status_code == 429:
            time.sleep(2)
            r = requests.get(url, params={'mailto': email}, timeout=20)
        if r.status_code != 200:
            return None
        authors = r.json().get('message', {}).get('author', [])
        tgt = norm(target_last)
        for a in authors:
            fam = a.get('family', '')
            if fam and norm(fam) == tgt:
                given = (a.get('given','') or '').strip()
                if given and '.' not in given and len(given) > 1:
                    return given
        return None
    except Exception:
        return None

df = pd.read_csv(DOI_FILE)
df['doi'] = df['doi'].astype(str)
oa = pd.read_csv(OA_RESULT)
already = set(oa[oa['recovered_first'].notna() & (oa['recovered_first']!='')]['hashed_author'])
todo_df = df[~df['hashed_author'].isin(already)]
if os.path.exists(OUTPUT):
    prev = pd.read_csv(OUTPUT); done_keys = set(prev['hashed_author']); rows = prev.to_dict('records')
else:
    rows, done_keys = [], set()
todo = todo_df[~todo_df['hashed_author'].isin(done_keys)]
cnt = 0
for row in todo.itertuples():
    first = crossref_fullname(str(row.doi), row.last, EMAIL)
    rows.append({'hashed_author': row.hashed_author, 'recovered_first': first if first else '', 'method': 'crossref'})
    cnt += 1
    if cnt % 100 == 0:
        pd.DataFrame(rows).to_csv(OUTPUT, index=False)
    time.sleep(0.05)
pd.DataFrame(rows).to_csv(OUTPUT, index=False)
