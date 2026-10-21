# diff54_135b_getgood.py — дельты по постам автора между базовыми снапами и TS 1711.

import json, os, re, glob

OUT = '/home/z/my-project/output/evidence_post'

def load(fn):
    d = json.load(open(os.path.join(OUT, fn)))
    posts = {}
    users = {}
    items = d.get('data') if isinstance(d.get('data'), list) else ([d['data']] if isinstance(d.get('data'), dict) else [])
    for i in items + list(d.get('included') or []):
        if not isinstance(i, dict): continue
        if i.get('type') == 'posts':
            a = i.get('attributes', {}) or {}
            posts[a.get('number') or 0] = (i, a)
        elif i.get('type') == 'users':
            users[i.get('id')] = (a2 := i.get('attributes', {}) or {}).get('username') or i.get('id')
    return posts, users, d

def show(tag, posts, users, nums, filter_author=None):
    print(f'--- {tag}')
    found = 0
    for n in sorted(posts):
        i, a = posts[n]
        uid = i.get('relationships', {}).get('user', {}).get('data', {})
        uid = uid.get('id') if isinstance(uid, dict) else None
        uname = users.get(uid, '?')
        if filter_author and uname != filter_author: continue
        if nums and n not in nums: continue
        found += 1
        rc = {k: v for k, v in (a.get('reactionCounts') or {}).items() if v}
        print(f"  #{n} {a.get('createdAt','?')[:19]} {uname} likes={a.get('likesCount')} rx={rc} :: {re.sub('<[^>]+>',' ',(a.get('contentPlain') or ''))[:70]}")
    if not found: print('  (нет подходящих постов в окне)')
    return found

# 1) 195574 #69: baseline 11.10 vs сейчас
p_old, u_old, _ = load('discussion_195574_near69_20261011_0251.json')
show('195574 #69 БАЗА 11.10 02:51', p_old, u_old, {69})
p_new, u_new, _ = load('discussion_195574_near69_20261021_1711.json')
show('195574 #69 СЕЙЧАС 17:11', p_new, u_new, {69})

# 2) 195660: все посты PatronOfSanity в текущем окне near381 + база 02.10
p_old, u_old, _ = load('discussion_195660_near999999_20261002_1934.json')
print('=== 195660 БАЗА 02.10: посты автора ===')
show('все PatronOfSanity (база)', p_old, u_old, None, 'PatronOfSanity')
p_new, u_new, _ = load('discussion_195660_near381_20261021_1711.json')
print('=== 195660 СЕЙЧАС near381: посты автора ===')
show('все PatronOfSanity (сейчас)', p_new, u_new, None, 'PatronOfSanity')

# 3) 196411 #48: база 1634 сегодня vs сейчас near48
p_old, u_old, _ = load('discussion_196411_near999999_20261021_1634.json')
show('196411 #48 БАЗА 16:34', p_old, u_old, {48})
p_new, u_new, _ = load('discussion_196411_near48_20261021_1711.json')
show('196411 #48 СЕЙЧАС 17:11', p_new, u_new, {48})

# 4) 159759 окно near14591: какие номера в окне, есть ли ещё посты автора
p_new, u_new, d = load('discussion_159759_near14591_20261021_1711.json')
nums = sorted(p_new)
print(f'=== 159759 окно near14591: {len(nums)} постов, диапазон {nums[0]}..{nums[-1] if nums else "-"}')
show('все PatronOfSanity в окне', p_new, u_new, None, 'PatronOfSanity')
