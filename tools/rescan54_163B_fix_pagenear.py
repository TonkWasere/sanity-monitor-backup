# rescan54_163B_fix_pagenear.py — исправление: Flarum игнорирует ?near=N, нужен ?page[near]=N.
# 54-163-B: хвост d/195660 391..424 (никогда не покрывался) + переподтверждение #387/#381/#389.
import json, os, urllib.request, time, hashlib, re
TS = '20261022_2110'
OUT = '/home/z/my-project/output/evidence_post'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
def get(url, name):
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        print('SKIP', name); return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body); json.loads(body.decode('utf-8'))
        print('OK  ', name, len(body), 'bytes sha', hashlib.sha256(body).hexdigest()[:16]); time.sleep(1.0)
        return True
    except Exception as e:
        print('FAIL', name, repr(e)[:120])
        if os.path.exists(path): os.remove(path)
        return False
def parse(name):
    d = json.load(open(os.path.join(OUT, name)))
    inc = d.get('included', [])
    users = {u['id']: u['attributes'].get('username') for u in inc if u.get('type') == 'users'}
    posts = []
    for p in inc:
        if p.get('type') == 'posts':
            a = p['attributes']; uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id')
            posts.append({'n': a.get('number'), 'ct': a.get('createdAt'), 'u': users.get(uid),
                          'hidden': a.get('isHidden'), 'text': re.sub('<[^>]+>', '', a.get('contentHtml') or '')})
    dd = d.get('data', {}).get('attributes', {})
    return posts, dd
jobs = [
    (f'{BASE}/api/discussions/195660?page[near]=430', f'discussion_195660_pagenear430_{TS}.json'),
    (f'{BASE}/api/discussions/195660?page[near]=381', f'discussion_195660_pagenear381_{TS}.json'),
    (f'{BASE}/api/discussions/195192?page[near]=389', f'discussion_195192_pagenear389_{TS}.json'),
    (f'{BASE}/api/discussions/195192?page[near]=381', f'discussion_195192_pagenear381_{TS}.json'),
    (f'{BASE}/api/discussions/195660?page[near]=350', f'discussion_195660_pagenear350_{TS}.json'),
]
for u, n in jobs: get(u, n)
print('\n=== ANALYSIS (page[near] FIX) ===')
for name in [j[1] for j in jobs]:
    try:
        posts, dd = parse(name)
        nums = sorted(p['n'] for p in posts if p['n'] is not None)
        print(f"\n{name}: cc={dd.get('commentCount')} LPN={dd.get('lastPostNumber')} | captured {len(nums)}: {min(nums)}..{max(nums)}")
        for p in posts:
            mark = ' <<< SANITY' if p['u'] == 'PatronOfSanity' else ''
            if p['u'] == 'PatronOfSanity' or (p['n'] and 'near430' in name):
                print(f"  #{p['n']} {str(p['ct'])[:16]} {p['u']} hidden={p['hidden']}: {p['text'][:95]}{mark}")
    except Exception as e:
        print(name, 'parse fail:', repr(e)[:100])
