# rescan54_145b_phase2.py — фаза-2 раунда 54-145 (TS 0230): NEW ×2 (196828 «Просто FMG-9»,
# 196814 «Вопрос для гретых на запаски») OP near=1 + near999999 ОБА + перепроверка createdAt
# (урок 54-136) + авторство дельт: 196827 #3, 196826 #2, 196813 #28, 196805 #32-33, 196816 #17
import json, os, urllib.request, time, re, datetime

TS = '20261022_0230'
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

def head_text(p, n=160):
    a = p.get('attributes', {})
    c = a.get('contentHtml') or a.get('content') or ''
    c = re.sub('<[^>]+>', ' ', c)
    return re.sub(r'\s+', ' ', c).strip()[:n]

def show(fname, tag, only_nums=None):
    pp, d = posts_of(fname)
    disc = d.get('data', {}) if isinstance(d, dict) else {}
    if isinstance(disc, dict) and disc.get('type') == 'discussions':
        da = disc.get('attributes', {})
        print(f"[{tag}] cc={da.get('commentCount')} LPN={da.get('lastPostNumber')} createdAt={da.get('createdAt')} title={da.get('title','?')} locked={da.get('locked')}")
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

print('===== ФАЗА-2: NEW ×2 OP near=1 + near999999 ОБА (перепроверка createdAt, урок 54-136) =====')
new_threads = [196828, 196814]
for tid in new_threads:
    f1 = f'discussion_{tid}_near1_{TS}.json'
    f2 = f'discussion_{tid}_near999999_{TS}.json'
    if not os.path.exists(os.path.join(OUT, f1)):
        get(f'{BASE}/api/discussions/{tid}?page%5Bnear%5D=1', f1); time.sleep(1)
    if not os.path.exists(os.path.join(OUT, f2)):
        get(f'{BASE}/api/discussions/{tid}?page%5Bnear%5D=999999', f2); time.sleep(1)
    show(f1, f'{tid} OP', only_nums={1})
    show(f2, f'{tid} TAIL', only_nums=None)

print('===== АВТОРСТВО ПО RELATIONSHIPS (урок 54-137) =====')
checks = [
    ('discussion_196827_near999999_%s.json' % TS, '196827', {3}),
    ('discussion_196826_near999999_%s.json' % TS, '196826', {2}),
    ('discussion_196813_near999999_%s.json' % TS, '196813', {28}),
    ('discussion_196805_near999999_%s.json' % TS, '196805', {32, 33}),
    ('discussion_196816_near999999_%s.json' % TS, '196816', {17}),
]
for fname, tag, nums in checks:
    if os.path.exists(os.path.join(OUT, fname)):
        show(fname, tag, only_nums=nums)
    else:
        tid = fname.split('_')[1]
        get(f'{BASE}/api/discussions/{tid}?page%5Bnear%5D=999999', fname); time.sleep(1)
        show(fname, tag, only_nums=nums)

summary = {
    'round': '54-145', 'ts': TS, 'utc': datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M'),
    'front_cutoff': '2026-10-22T01:30',
    'front_new': ['196828', '196814'],
    'phase2_authorship': ['196827#3', '196826#2', '196813#28', '196805#32-33', '196816#17'],
}
json.dump(summary, open(f'{OUT}/check54_145b_summary_{TS}.json', 'w'), indent=1)
print('\nSUMMARY SAVED')
