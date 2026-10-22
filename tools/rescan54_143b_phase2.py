# rescan54_143b_phase2.py — фаза-2 раунда 54-143 (TS 0030): авторство ключевых постов
# 196810 #65 (12-й час), 196821 #8-16 (+9 вспух), 196824 #8-9, 196823 #4-5, 196817 #25-26
# (разморозка), 196770 #125 (Crios vs AlexMrz2), 196820 #11, 196819 #3, 196813 #27
import json, os, urllib.request, time, re, datetime

TS = '20261022_0030'
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
        print(f"[{tag}] cc={da.get('commentCount')} LPN={da.get('lastPostNumber')} createdAt={da.get('createdAt')} locked={da.get('locked')}")
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

# все хвосты уже снапнуты фазой-1 (near999999) — доп. GET не нужен, кроме 196821 (проверка
# полного хвоста #8-16 одним near=999999 уже есть) — читаем локально
checks = [
    ('discussion_196810_near999999_%s.json' % TS, '196810', {65}),
    ('discussion_196821_near999999_%s.json' % TS, '196821', {8, 9, 10, 11, 12, 13, 14, 15, 16}),
    ('discussion_196824_near999999_%s.json' % TS, '196824', {8, 9}),
    ('discussion_196823_near999999_%s.json' % TS, '196823', {4, 5}),
    ('discussion_196817_near999999_%s.json' % TS, '196817', {25, 26}),
    ('discussion_196770_near999999_%s.json' % TS, '196770', {125}),
    ('discussion_196820_near999999_%s.json' % TS, '196820', {11}),
    ('discussion_196819_near999999_%s.json' % TS, '196819', {3}),
    ('discussion_196813_near999999_%s.json' % TS, '196813', {27}),
]
print('===== АВТОРСТВО ПО RELATIONSHIPS (урок 54-137) =====')
for fname, tag, nums in checks:
    if os.path.exists(os.path.join(OUT, fname)):
        show(fname, tag, only_nums=nums)
    else:
        tid = fname.split('_')[1]
        get(f'{BASE}/api/discussions/{tid}?page%5Bnear%5D=999999', fname); time.sleep(1)
        show(fname, tag, only_nums=nums)

summary = {
    'round': '54-143', 'ts': TS, 'utc': datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d %H:%M'),
    'front_cutoff': '2026-10-21T23:31',
    'front_new': [], 'phase2_authorship': ['196810#65', '196821#8-16', '196824#8-9', '196823#4-5',
                                           '196817#25-26', '196770#125', '196820#11', '196819#3', '196813#27'],
}
json.dump(summary, open(f'{OUT}/check54_143b_summary_{TS}.json', 'w'), indent=1)
print('\nSUMMARY SAVED')
