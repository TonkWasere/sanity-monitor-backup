#!/usr/bin/env python3
# analyze45.py — Task 45: перехват фулл-поста PatronOfSanity в 196411 + дельты vs TS 1122 (Task 44).
import json, glob, re, html, hashlib, os

os.chdir('/home/z/my-project/output/evidence_post')
NEW, OLD = '20261014_1144', '20261014_1122'
SANITY_UID = '1717344'

def norm_data(d):
    dd = d.get('data')
    if isinstance(dd, dict):
        return [dd]
    if isinstance(dd, list):
        return dd
    return []

def load_disc(path):
    with open(path) as f:
        d = json.load(f)
    if not isinstance(d, dict):
        return {}, [], {}
    attrs = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
    posts, users = [], {}
    for inc in (d.get('included', []) or []) + norm_data(d):
        if isinstance(inc, dict) and inc.get('type') == 'posts':
            a = inc['attributes']
            posts.append({
                'id': inc.get('id'), 'number': a.get('number'),
                'createdAt': a.get('createdAt'), 'ct': a.get('contentType'),
                'html': a.get('contentHtml') or '', 'hiddenAt': a.get('hiddenAt'),
                'isApproved': a.get('isApproved'), 'editCount': a.get('editCount') if 'editCount' in a else a.get('editedAt'),
                'rx': a.get('reactionCounts') or {}, 'likes': a.get('likesCount'),
                'replyTo': (inc.get('relationships', {}).get('replyTo', {}) or {}).get('data', {}).get('id'),
                'uid': (inc.get('relationships', {}).get('user', {}) or {}).get('data', {}).get('id'),
            })
        elif inc.get('type') == 'users':
            users[inc.get('id')] = (inc.get('attributes', {}) or {}).get('username', '?')
    return attrs, posts, users

def strip_h(h):
    t = re.sub(r'<br\s*/?>', '\n', h)
    t = re.sub(r'<[^>]+>', '', t)
    return html.unescape(t).strip()

def card_from_index(prefix, ts):
    nums, meta = set(), {}
    for p in sorted(glob.glob(f'{prefix}_off*_{ts}.json')):
        d = json.load(open(p))
        for inc in (d.get('included', []) or []) + norm_data(d):
            if isinstance(inc, dict) and inc.get('type') == 'posts':
                a = inc['attributes']
                n = a.get('number')
                if n:
                    nums.add(n)
                    meta[n] = {'ct': a.get('contentType'), 'createdAt': a.get('createdAt'), 'id': inc.get('id'),
                               'hiddenAt': a.get('hiddenAt'), 'isApproved': a.get('isApproved')}
    return nums, meta

print('=' * 76)
print('A) 196411 STATE: 1122 -> 1144')
na, nposts, nu = load_disc(f'discussion_196411_near999999_{NEW}.json')
oa, oposts, ou = load_disc(f'discussion_196411_near999999_{OLD}.json')
ou = {**ou, **nu}
print(f"  cc {oa.get('commentCount')} -> {na.get('commentCount')}; lastPostedAt {oa.get('lastPostedAt')} -> {na.get('lastPostedAt')}")
print(f"  sticky {oa.get('isSticky')} -> {na.get('isSticky')}; locked {oa.get('isLocked')} -> {na.get('isLocked')}; lastPostNumber {oa.get('lastPostNumber')} -> {na.get('lastPostNumber')}")
op_html = next((p['html'] for p in oposts if p['number'] == 1), None)
np1 = next((p for p in nposts if p['number'] == 1), None)
if op_html is not None and np1:
    oh = hashlib.sha256(op_html.encode()).hexdigest()[:16]
    nh = hashlib.sha256(np1['html'].encode()).hexdigest()[:16]
    print(f"  OP sha256: {oh} -> {nh} {'OK (не менялся)' if oh == nh else '!! ИЗМЕНИЛСЯ'}")

print('=' * 76)
print('B) ПОСТ САНИТИ (uid 1717344 / PatronOfSanity) в окне 1144:')
found = False
for p in sorted(nposts, key=lambda x: x['number'] or 0):
    if p['uid'] == SANITY_UID:
        found = True
        h_sha = hashlib.sha256(p['html'].encode()).hexdigest()
        print(f"  POST id={p['id']} #{p['number']} [{p['ct']}] createdAt={p['createdAt']}")
        print(f"  hiddenAt={p['hiddenAt']} isApproved={p['isApproved']} edits={p['editCount']} likes={p['likes']} rx={p['rx']} replyTo_id={p['replyTo']}")
        print(f"  contentHtml len={len(p['html'])} sha256={h_sha}")
        txt = strip_h(p['html'])
        print(f"  TEXT ({len(txt)} зн):\n  ---\n{txt}\n  ---")
if not found:
    print('  !!! ПОСТ САНИТИ В ГОСТЕВОМ ОКНЕ НЕ НАЙДЕН — проверяю по postsindex...')
    for off in (0, 20, 40, 60):
        d = json.load(open(f'postsindex_196411_off{off}_{NEW}.json'))
        for inc in (d.get('included', []) or []) + norm_data(d):
            if isinstance(inc, dict) and inc.get('type') == 'posts':
                uid = (inc.get('relationships', {}).get('user', {}) or {}).get('data', {}).get('id')
                a = inc.get('attributes', {})
                if uid == SANITY_UID:
                    print(f"  postsindex off{off}: id={inc.get('id')} #{a.get('number')} createdAt={a.get('createdAt')} hiddenAt={a.get('hiddenAt')} isApproved={a.get('isApproved')}")
                    print(f"  (contentHtml в postsindex отсутствует — снапим через near-окно!)")

print('=' * 76)
print('C) НОВЫЕ ПОСТЫ ОКНА (1144 vs 1122):')
oldnums = {p['number'] for p in oposts if p['number']}
for p in sorted(nposts, key=lambda x: x['number'] or 0):
    n = p['number']
    if n and n not in oldnums:
        who = ou.get(p['uid'], f"uid{p['uid']}")
        hid = f" hiddenAt={p['hiddenAt']}" if p['hiddenAt'] else ''
        appr = f" isApproved={p['isApproved']}" if p['isApproved'] is False else ''
        print(f"  NEW #{n} [{p['ct']}] {p['createdAt']} {who}{hid}{appr}: {strip_h(p['html'])[:150]}")
gone = sorted(n for n in oldnums if n not in {p['number'] for p in nposts})
print(f"  ИСЧЕЗЛИ ИЗ ОКНА (кандидаты на снос, проверка по union): {gone if gone else '—'}")

print('=' * 76)
print('D) UNION-КАРТА 196411 (off0/20/40/60, pageSize=20):')
nn, nmeta = card_from_index('postsindex_196411', NEW)
onums, ometa = card_from_index('postsindex_196411', OLD)
mx = max(nn) if nn else 0
gaps = sorted(set(range(1, mx + 1)) - nn)
cmt = sum(1 for n in nn if nmeta[n]['ct'] == 'comment')
print(f"  карта NEW: {len(nn)} постов, max #{mx}, гэпы: {gaps if gaps else 'нет'} (comment={cmt}, events={len(nn)-cmt})")
lost = sorted(onums - nn)
gained = sorted(nn - onums)
print(f"  vs OLD: ИСЧЕЗЛИ {lost if lost else '—'}; ПОЯВИЛИСЬ {gained if gained else '—'}")
for n in lost:
    m = ometa.get(n, {})
    print(f"    !! #{n} ИСЧЕЗ: ct={m.get('ct')} createdAt={m.get('createdAt')} id={m.get('id')} — кандидат на снос")
for n in sorted(n for n in gained if nmeta.get(n, {}).get('ct') == 'comment'):
    m = nmeta.get(n, {})
    print(f"    +#{n}: ct={m.get('ct')} createdAt={m.get('createdAt')} hiddenAt={m.get('hiddenAt')}")
# адресат #28
n28 = next((p for p in nposts if p['number'] == 28), None)
print(f"  #28 Naut_Bro: {'ЖИВ' if n28 and not n28['hiddenAt'] else 'ПРОВЕРКА'} (hiddenAt={n28['hiddenAt'] if n28 else '—'}, rx={n28['rx'] if n28 else '—'})")
# контроль тела #33 (снесён в 44) — не должен вернуться
print(f"  #33 (снесён в Task 44): {'ВЕРНУЛСЯ?!' if 33 in nn else 'отсутствует (снос подтверждён union)'}")

print('=' * 76)
print('E) КОНТРОЛЫ тихих запретов:')
for tid in (196315, 196415):
    a, ps, u = load_disc(f'discussion_{tid}_near999999_{NEW}.json')
    nums = sorted(p['number'] for p in ps if p['number'])
    last = max((p for p in ps if p['ct'] == 'comment'), key=lambda x: x['createdAt'], default=None)
    print(f"  d/{tid} [{a.get('title','?')[:40]}] cc={a.get('commentCount')} locked={a.get('isLocked')} last={a.get('lastPostedAt')} window={nums[0] if nums else '-'}..{nums[-1] if nums else '-'}")
    if last:
        print(f"    последний comment #{last['number']} {last['createdAt']} {u.get(last['uid'], last['uid'])}: {strip_h(last['html'])[:110]}")

print('=' * 76)
print('F) FRONTINDEX:')
fi = json.load(open(f'frontindex_off0_{NEW}.json'))
items = []
for x in norm_data(fi):
    a = x['attributes']
    items.append({'id': x.get('id'), 't': a.get('title', ''), 'created': a.get('createdAt'),
                  'last': a.get('lastPostedAt'), 'sticky': a.get('isSticky'), 'cc': a.get('commentCount')})
print('  sticky:')
for it in items:
    if it['sticky']:
        print(f"    d/{it['id']} [{it['t'][:46]}] cc={it['cc']} last={it['last']}")
print('  юзер-волна (createdAt >= 2026-10-12T12:00):')
for it in sorted([i for i in items if (i['created'] or '') >= '2026-10-12T12:00'], key=lambda x: x['created'] or ''):
    print(f"    d/{it['id']} [{it['t'][:46]}] created={it['created']} cc={it['cc']} last={it['last']}")
sanity_on_front = [i for i in items if i['id'] == '196411']
if sanity_on_front:
    print(f"  196411 на page0: есть, cc={sanity_on_front[0]['cc']}")
else:
    print('  196411 на page0: НЕТ (выпадение)')

print('=' * 76)
print('G) SEARCH «патч» (×5 верификация):')
sf = json.load(open(f'search_patch_{NEW}.json'))
data = norm_data(sf)
pn = [x for x in data if (x.get('attributes', {}).get('title') or '').lower().startswith('патчноут')]
for x in sorted(pn, key=lambda y: (y.get('attributes', {}).get('createdAt') or ''), reverse=True)[:4]:
    a = x['attributes']
    print(f"  [{a.get('title')}] created={a.get('createdAt')} cc={a.get('commentCount')}")
print(f"  всего выдач: {len(data)}; «Патчноут [14.10.2026]» {'ОТСУТСТВУЕТ' if not any('14.10' in (x.get('attributes', {}).get('title') or '') for x in pn) else '!!! ПОЯВИЛСЯ'}")

print('=' * 76)
print('H) HTML-ПРЕЙЛОАД 196411 (гостевой вид):')
hs = open(f'html_preload_196411-igrovye-izmeneniya-vstupili-v-silu_{NEW}.html', encoding='utf-8').read()
for marker in ('PatronOfSanity', 'PatronSaintOfFuckYourSanity', 'locked', 'Заблокировано', 'нельзя ответить'):
    cnt = hs.count(marker)
    if cnt:
        print(f"  маркер {marker!r}: ×{cnt}")
print('  (пусто = маркеров нет — пост в гостевом HTML не прелоадится, что норма №33)')
print('\nANALYZE45_DONE')
