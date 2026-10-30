# rescan54_142b_phase2.py — фаза-2 раунда 54-142 (TS 2331 слой): NEW ×2 (196822/196824)
# + авторство ключевых постов: 196820 #10 (22:55 «берлога 6у»), 196807 #22, 196761 #31-35
# + verify createdAt (урок 54-69: lastPostedAt обманывает — 4 раунда подряд)
import json, os, urllib.request, time, re, datetime

TS = '20261021_2331'
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'

def get(url, name, validate_json=True):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print(f'SKIP {name}'); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        if validate_json:
            json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        return True
    except Exception as e:
        print(f'FAIL {name}: {e}')
        return False

def posts_of(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
    except Exception as e:
        print(f'PARSE FAIL {fname}: {e}'); return [], d
    data = d.get('data')
    items = data if isinstance(data, list) else [data] if data else []
    pp = [i for i in items if isinstance(i, dict) and i.get('type') == 'posts']
    inc = [i for i in (d.get('included') or []) if isinstance(i, dict) and i.get('type') == 'posts']
    return pp + inc, d

def head_text(p, n=150):
    a = p.get('attributes', {})
    c = a.get('contentHtml') or a.get('content') or ''
    c = re.sub('<[^>]+>', ' ', c)
    return re.sub(r'\s+', ' ', c).strip()[:n]

def show(fname, tag, only_nums=None, authors=False):
    pp, d = posts_of(fname)
    disc = d.get('data', {}) if isinstance(d, dict) else {}
    if isinstance(disc, dict) and disc.get('type') == 'discussions':
        da = disc.get('attributes', {})
        print(f"[{tag}] cc={da.get('commentCount')} LPN={da.get('lastPostNumber')} createdAt={da.get('createdAt')} "
              f"lastPostedAt={da.get('lastPostedAt')} sticky={da.get('sticky')} locked={da.get('locked')}")
    users = {}
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'users':
            users[i.get('id')] = (i.get('attributes') or {}).get('username', '?')
    for p in pp:
        a = p.get('attributes', {})
        num = a.get('number')
        if only_nums and num not in only_nums:
            continue
        uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id')
        who = users.get(uid, f'id{uid}')
        print(f"  #{num} {a.get('createdAt')} :: [{who}] {head_text(p)}")

time.sleep(1)
# --- NEW ×2: OP near=1 + near999999 оба (урок 54-131/136) ---
for tid in (196822, 196824):
    get(f'{BASE}/api/discussions/{tid}?page%5Bnear%5D=1',
        f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    get(f'{BASE}/api/discussions/{tid}?page%5Bnear%5D=999999',
        f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)

print('\n===== NEW 196822 «новый ивент» =====')
show(f'discussion_196822_near1_{TS}.json', '196822 OP')
show(f'discussion_196822_near999999_{TS}.json', '196822 tail')

print('\n===== NEW 196824 «Двужушности хочется» =====')
show(f'discussion_196824_near1_{TS}.json', '196824 OP')
show(f'discussion_196824_near999999_{TS}.json', '196824 tail')

# --- авторство ключевых постов по relationships.user (урок 54-137) ---
print('\n===== АВТОРСТВО: 196820 #10 / 196807 #22 / 196761 #31-35 =====')
show(f'discussion_196820_near999999_{TS}.json', '196820', only_nums={10})
show(f'discussion_196807_near999999_{TS}.json', '196807', only_nums={22})
show(f'discussion_196761_near999999_{TS}.json', '196761', only_nums={31, 32, 33, 34, 35})

# --- сводка ---
summary = {
    'round': '54-142', 'ts': TS, 'utc': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
    'front_cutoff': '2026-10-21T22:33',
    'phase2': ['196822', '196824'],
    'authorship_checks': ['196820#10', '196807#22', '196761#31-35'],
}
json.dump(summary, open(f'{OUT}/check54_142b_summary_{TS}.json', 'w'), indent=1)
print('\nSUMMARY SAVED')
