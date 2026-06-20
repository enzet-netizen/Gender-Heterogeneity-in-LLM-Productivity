import pandas as pd
import time

INPUT   = 'authors_clean.csv'
OUTPUT   = 'gender_cache.csv'        
API_KEY = ''      
BATCH   = 10

authors = pd.read_csv(INPUT)
all_names = sorted(authors['name_key'].dropna().unique())

if os.path.exists(OUTPUT):
    done = pd.read_csv(OUTPUT)
    done_names = set(done['name'])
else:
    done = pd.DataFrame(columns=['name', 'gender', 'probability', 'count'])
    done_names = set()

todo = [n for n in all_names if n not in done_names]

results = []
for i in range(0, len(todo), BATCH):
    batch = todo[i:i+BATCH]
    params = [('name[]', n) for n in batch] + [('apikey', API_KEY)]
    try:
        r = requests.get('https://api.genderize.io', params=params, timeout=20)
        r.raise_for_status()
        for item in r.json():
            results.append({
                'name': item.get('name'),
                'gender': item.get('gender'),
                'probability': item.get('probability'),
                'count': item.get('count'),
            })
    except Exception as e:
        break

    if len(results) >= 500:
        done = pd.concat([done, pd.DataFrame(results)], ignore_index=True)
        done.to_csv(OUTPUT, index=False)
        results = []
    time.sleep(0.1)

if results:
    done = pd.concat([done, pd.DataFrame(results)], ignore_index=True)
    done.to_csv(OUTPUT, index=False)
print(f"Done.")
