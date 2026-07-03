import pandas as pd
import requests, time, os, unicodedata
from collections import defaultdict

INPUT   = 'removed_with_doi.csv'
CACHE   = 'recovered_cache.csv'
OUTPUT  = 'recovered_names.csv'
API_KEY = ''
BATCH   = 100

def norm(s):
    if not s: return ''
    s = unicodedata.normalize('NFKD', str(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return ''.join(c for c in s.lower() if c.isalnum())

def find_first_name(authorships, target_last):
    tgt = norm(target_last)
    for a in authorships:
        auth = a.get('author', {})
        fam = auth.get('family_name')
        given = auth.get('given_name')
        if fam and norm(fam) == tgt:
            if given and '.' not in given and len(given) > 1:
                return given
            continue
        if not fam:
            full = auth.get('display_name', '')
            parts = [p for p in full.split() if p.lower().strip('.') not in ('jr','sr','ii','iii','iv')]
            if len(parts) >= 2 and norm(parts[-1]) == tgt:
                first = parts[0]
                if '.' not in first and len(first) > 1:
                    return first
    return None

df = pd.read_csv(INPUT)
df['doi'] = df['doi'].astype(str)
if os.path.exists(CACHE):
    done = pd.read_csv(CACHE); done_keys = set(done['hashed_author'])
else:
    done = pd.DataFrame(columns=['hashed_author','recovered_first']); done_keys = set()
todo = df[~df['hashed_author'].isin(done_keys)]
doi_map = defaultdict(list)
for row in todo.itertuples():
    doi_map[row.doi.lower()].append((row.hashed_author, row.last))
unique_dois = list(doi_map.keys())
results = []
for i in range(0, len(unique_dois), BATCH):
    batch = unique_dois[i:i+BATCH]
    params = {'filter': 'doi:' + '|'.join(batch), 'per-page': BATCH, 'api_key': API_KEY}
    try:
        r = requests.get("https://api.openalex.org/works", params=params, timeout=40)
        if r.status_code != 200:
            time.sleep(1); continue
        for w in r.json().get('results', []):
            w_doi = (w.get('doi') or '').lower().replace('https://doi.org/','')
            auths = w.get('authorships', [])
            for (hashed, last) in doi_map.get(w_doi, []):
                first = find_first_name(auths, last)
                results.append({'hashed_author': hashed, 'recovered_first': first if first else ''})
    except Exception:
        time.sleep(1); continue
    if len(results) >= 500:
        done = pd.concat([done, pd.DataFrame(results)], ignore_index=True)
        done.to_csv(CACHE, index=False); results = []
    time.sleep(0.1)
if results:
    done = pd.concat([done, pd.DataFrame(results)], ignore_index=True)
    done.to_csv(CACHE, index=False)
done.to_csv(OUTPUT, index=False)
