#!/usr/bin/env python3
# analyze_167.py — точечные проверки Task 54-167:
# (1) Crios #68 в 193924 — почему Crios-скан пуст (username-mapping?);
# (2) 196852 #11 — isHidden/type (софт-скрытие при cc=9/LPN=10?);
# (3) ТГК stalzone 3227 / spectrum 7955 — есть ли новые посты;
# (4) OP-реквизиты NEW 196879/196877 (автор, createdAt, title).
import json, os, re

OUT = '/home/z/my-project/output/evidence_post'
TS = '20261023_0130'

def load(fn):
    return json.load(open(os.path.join(OUT, fn)))

print('=== 1) CRIOS #68 в 193924 (username-map) ===')
d = load(f'discussion_193924_near999999_{TS}.json')
inc = d.get('included', [])
users = {u['id']: u['attributes'].get('username') for u in inc if u.get('type') == 'users'}
print('users in included:', {k: v for k, v in users.items()})
for p in inc:
    if p.get('type') == 'posts':
        a = p.get('attributes', {})
        uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id')
        if a.get('number') in (67, 68):
            print(f"  #{a['number']} user_id={uid} username={users.get(uid)!r} createdAt={a.get('createdAt')}")

print('\n=== 2) 196852 пост #11 (isHidden?) ===')
for fn in (f'discussion_196852_near1_{TS}.json', f'discussion_196852_near999999_{TS}.json'):
    d = load(fn)
    aa = d.get('data', {}).get('attributes', {})
    print(f'  [{fn[30:45]}] cc={aa.get("commentCount")} LPN={aa.get("lastPostNumber")}')
    for p in d.get('included', []):
        if p.get('type') == 'posts' and p.get('attributes', {}).get('number') in (9, 10, 11):
            a = p.get('attributes', {})
            print(f"    #{a['number']} hidden={a.get('isHidden')} deletedAt={a.get('deletedAt')} type={p.get('type')} createdAt={a.get('createdAt')} :: {(a.get('contentPlain') or '')[:60]!r}")

print('\n=== 3) ТГК ===')
for fn, label, want in ((f'tg_stalzone_page0_{TS}.html', 'stalzone', 3227),
                        (f'tg_spectrum_page0_{TS}.html', 'spectrum', 7955)):
    html = open(os.path.join(OUT, fn), encoding='utf-8', errors='replace').read()
    ids = sorted({int(m) for m in re.findall(r'data-post="[^/]+/(\d+)"', html)})
    print(f'  {label}: посты на стр.0 = {ids[:6]}...{ids[-4:] if len(ids) > 6 else ""}; '
          f'{"★ НЕТ " + str(want) if want not in ids else "ЕСТЬ " + str(want)} (max={max(ids) if ids else "?"})')

print('\n=== 4) NEW OP 196879 / 196877 ===')
for tid in (196879, 196877):
    d = load(f'discussion_{tid}_near1_{TS}.json')
    aa = d.get('data', {}).get('attributes', {})
    inc = d.get('included', [])
    users = {u['id']: u['attributes'].get('username') for u in inc if u.get('type') == 'users'}
    print(f'  [{tid}] {aa.get("title")!r} createdAt={aa.get("createdAt")} cc={aa.get("commentCount")} tag={aa.get("tags")}')
    posts = sorted((p for p in inc if p.get('type') == 'posts'),
                   key=lambda p: p.get('attributes', {}).get('number') or 0)
    for p in posts[:4]:
        a = p.get('attributes', {})
        uid = p.get('relationships', {}).get('user', {}).get('data', {}).get('id')
        print(f"    #{a['number']} {a.get('createdAt')} @{users.get(uid)} :: {(a.get('contentPlain') or '')[:130]!r}")
