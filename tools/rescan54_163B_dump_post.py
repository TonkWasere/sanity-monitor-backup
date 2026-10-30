# rescan54_163B_dump_post.py — Task 54-163-B (межраунд ~20:55-21:15 UTC 22.10):
# АВТОР прислал 2 скриншота ПРОФИЛЯ PatronOfSanity (Discord CDN, скачаны 20:55):
#   img1 = скрытый пост «Нейро»-методологии из d/195192 (наш #389, текст совпадает со снапом 19.09)
#   img2 = ВТОРОЙ скрытый пост — «Обещал исходники — держите» MEGA-дамп доказательств
#          (aw8VlLTQ..., 8 MB, 146 файлов, SHA256 cccd6734..., папки 01-07 + README)
#          из d/195660 «Патчноут [30.09.2026]» — ЭТО НЕ #387! №203-B поправка: #387 жив.
# Дамп-маркеры (aw8VlLTQ|MANIFEST|Обещал) НЕ встречаются ни в одном из 249 снапов 195660
# => скрыт ДО первого снапа. near381-окно 371..390, LPN=424 => хвост 391..424 НИКОГДА не покрывался.
# Задача: живой гостевая-фетч хвоста (near=430), переподтверждение #387 (near=381) и #389 (near=389);
# по отсутствующим номерам в 391..424 локализовать номер скрытого дампа.
import json, os, urllib.request, time, hashlib, re

TS = '20261022_2100'
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
        open(path, 'wb').write(body)
        json.loads(body.decode('utf-8'))  # validate
        print('OK  ', name, len(body), 'bytes, sha256', hashlib.sha256(body).hexdigest()[:16])
        time.sleep(1.0)
        return True
    except Exception as e:
        print('FAIL', name, repr(e)[:120])
        if os.path.exists(path): os.remove(path)
        return False

targets = [
    (f'{BASE}/api/discussions/195660?sort=-createdAt&near=430&page[scale]=2', f'discussion_195660_near430_{TS}.json'),
    (f'{BASE}/api/discussions/195660?near=381',                              f'discussion_195660_near381_{TS}.json'),
    (f'{BASE}/api/discussions/195192?near=389',                              f'discussion_195192_near389_{TS}.json'),
    (f'{BASE}/api/discussions/195192?near=381',                              f'discussion_195192_near381_{TS}.json'),
]
for u, n in targets:
    get(u, n)

print('\n=== ANALYSIS ===')
def parse(name):
    d = json.load(open(os.path.join(OUT, name)))
    inc = d.get('included', [])
    users = {u['id']: u['attributes'].get('username') for u in inc if u.get('type') == 'users'}
    posts = []
    for p in inc:
        if p.get('type') == 'posts':
            a = p['attributes']
            uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id')
            posts.append({'n': a.get('number'), 'ct': a.get('createdAt'),
                          'u': users.get(uid), 'hidden': a.get('isHidden'),
                          'text': re.sub('<[^>]+>', '', a.get('contentHtml') or '')})
    dd = d.get('data', {}).get('attributes', {})
    return posts, dd

for name in [f'discussion_195660_near430_{TS}.json', f'discussion_195660_near381_{TS}.json']:
    try:
        posts, dd = parse(name)
        nums = sorted(p['n'] for p in posts if p['n'] is not None)
        print(f"\n{name}: cc={dd.get('commentCount')} LPN={dd.get('lastPostNumber')}")
        print('  captured:', len(nums), '| range:', min(nums), '..', max(nums))
        for p in posts:
            if p['u'] == 'PatronOfSanity':
                print(f"  SANITY #{p['n']} {p['ct']} hidden={p['hidden']}: {p['text'][:110]}")
        if 'near430' in name and nums:
            missing = [i for i in range(391, max(nums)+1) if i not in nums]
            print('  MISSING numbers in 391..max (кандидаты на скрытые/удалённые):', missing)
            for p in posts:
                if p['n'] and p['n'] >= 391:
                    print(f"    #{p['n']} {p['ct']} {p['u']} hidden={p['hidden']}: {p['text'][:80]}")
    except Exception as e:
        print(name, 'parse fail:', repr(e)[:100])

# 195192: 389 hidden reconfirm + 381 alive reconfirm
for name, want in [(f'discussion_195192_near389_{TS}.json', 389), (f'discussion_195192_near381_{TS}.json', 381)]:
    try:
        posts, dd = parse(name)
        nums = sorted(p['n'] for p in posts if p['n'] is not None)
        print(f"\n{name}: cc={dd.get('commentCount')} LPN={dd.get('lastPostNumber')} | 381 alive: {381 in nums} | 389 visible: {389 in nums}")
        for p in posts:
            if p['u'] == 'PatronOfSanity':
                print(f"  SANITY #{p['n']} {p['ct']}: {p['text'][:90]}")
    except Exception as e:
        print(name, 'parse fail:', repr(e)[:100])
