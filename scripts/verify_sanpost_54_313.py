#!/usr/bin/env python3
# Task 54-313: верификация публикации 3 санити-постов автора в треде патчноута d/197149
# + фиксация лайка от игрока со статусом «Легенда». read-only, гостевой API.
import json, os, urllib.request, datetime
BASE = 'https://forum.exbo.net'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
OUT = '/home/z/my-project/output/evidence_post'
os.makedirs(OUT, exist_ok=True)
TS = '20261028_1130'
AUTHOR = 'PatronOfSanity'
TID = '197149'

name = f'discussion_{TID}_near999999_sanpost_verify_{TS}.json'
path = os.path.join(OUT, name)
req = urllib.request.Request(f'{BASE}/api/discussions/{TID}?page[near]=999999', headers=UA)
with urllib.request.urlopen(req, timeout=30) as r:
    body = r.read()
open(path, 'wb').write(body)
d = json.loads(body)

a = d['data']['attributes']
print(f"ТРЕД: {a.get('title')} | cc={a.get('commentCount')} lpn={a.get('lastPostNumber')} last={a.get('lastPostedAt')}")

included = d.get('included', [])
posts = [i for i in included if i.get('type') == 'posts']
users = {i['id']: i for i in included if i.get('type') == 'users'}
groups = {i['id']: i['attributes'] for i in included if i.get('type') == 'groups'}

def uinfo(uid):
    u = users.get(uid)
    if not u:
        return uid, [], None
    gids = u.get('relationships', {}).get('groups', {}).get('data', [])
    gnames = [groups[str(g['id'])]['nameSingular'] for g in gids if str(g['id']) in groups]
    return u['attributes'].get('username'), gnames, u['attributes'].get('commentCount')

def post_user(p):
    rel = p.get('relationships', {}).get('user', {}).get('data')
    return uinfo(str(rel['id'])) if rel else ('?', [], None)

def post_likes(p):
    rel = p.get('relationships', {}).get('likes', {}).get('data', [])
    return [uinfo(str(x['id'])) for x in rel]

def text(p, n=90):
    html = p['attributes'].get('contentHtml') or ''
    t = html.replace('<br>', ' ').replace('</p>', ' ').replace('</blockquote>', ' ')
    t = ' '.join(__import__('re').sub('<[^>]+>', '', t).split())
    return t[:n]

print(f"постов в выдаче: {len(posts)} | диапазон номеров: {min((p['attributes']['number'] for p in posts), default=0)}–{max((p['attributes']['number'] for p in posts), default=0)}")
found = []
for p in sorted(posts, key=lambda x: x['attributes']['number']):
    un, gr, _ = post_user(p)
    if un == AUTHOR:
        pa = p['attributes']
        lk = post_likes(p)
        found.append(p)
        print(f"--- ПОСТ #{pa['number']} | {pa['createdAt']} | alive={not pa.get('isHidden', False)} | likes={pa.get('likesCount')} | reactions={pa.get('reactionCounts')}")
        print(f"    текст: {text(p)}")
        for ln, lg, lc in lk:
            print(f"    ЛАЙК: {ln} | группы: {lg} | комментов у юзера: {lc}")
# что было после последнего поста автора (ответы?)
if found:
    lastnum = found[-1]['attributes']['number']
    after = [p for p in posts if p['attributes']['number'] > lastnum]
    print(f"после поста автора #{lastnum}: {len(after)} постов в выдаче")
    for p in after[:5]:
        un, gr, _ = post_user(p)
        print(f"    #{p['attributes']['number']} {p['attributes']['createdAt']} [{un}{'/'.join(gr) if gr else ''}]: {text(p, 70)}")
    # метаданные автора-поста для кэша
    meta = {'ts': TS, 'thread': TID, 'author': AUTHOR,
            'posts': [{'number': p['attributes']['number'], 'createdAt': p['attributes']['createdAt'],
                       'likesCount': p['attributes'].get('likesCount'), 'reactions': p['attributes'].get('reactionCounts'),
                       'likes': [{'user': ln, 'groups': lg} for ln, lg, _ in post_likes(p)]} for p in found],
            'thread_lp': a.get('lastPostNumber'), 'thread_cc': a.get('commentCount')}
    open(os.path.join(OUT, f'sanpost_verify_meta_{TS}.json'), 'w').write(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"META сохранена: sanpost_verify_meta_{TS}.json | постов автора: {len(found)}")
