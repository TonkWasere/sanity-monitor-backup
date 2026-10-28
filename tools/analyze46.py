#!/usr/bin/env python3
# analyze46.py — Task 46: разбор официального ТГК-поста про краши + дельты 196411/#48.
import json, glob, re, html, hashlib, os

os.chdir('/home/z/my-project/output/evidence_post')
NEW, OLD = '20261014_1148', '20261014_1144'

def norm_data(d):
    dd = d.get('data')
    return [dd] if isinstance(dd, dict) else (dd if isinstance(dd, list) else [])

def load_disc(path):
    d = json.load(open(path))
    attrs = d.get('data', {}).get('attributes', {}) if isinstance(d.get('data'), dict) else {}
    posts, users = [], {}
    for inc in (d.get('included', []) or []) + norm_data(d):
        if isinstance(inc, dict) and inc.get('type') == 'posts':
            a = inc['attributes']
            posts.append({'id': inc.get('id'), 'number': a.get('number'), 'createdAt': a.get('createdAt'),
                          'ct': a.get('contentType'), 'html': a.get('contentHtml') or '',
                          'hiddenAt': a.get('hiddenAt'), 'isApproved': a.get('isApproved'),
                          'rx': a.get('reactionCounts') or {}, 'likes': a.get('likesCount'),
                          'uid': (inc.get('relationships', {}).get('user', {}) or {}).get('data', {}).get('id')})
        elif inc.get('type') == 'users':
            users[inc.get('id')] = (inc.get('attributes', {}) or {}).get('username', '?')
    return attrs, posts, users

def strip_h(h):
    t = re.sub(r'<br\s*/?>', '\n', h)
    t = re.sub(r'<[^>]+>', '', t)
    return html.unescape(t).strip()

def parse_tg(path):
    s = open(path, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'data-post="([^"]+)"(.*?)(?=data-post="|class="tgme_widget_message_divider|$)', s, re.S):
        pid, blk = m.group(1), m.group(2)
        t = re.search(r'<time datetime="([^"]+)"', blk)
        v = re.search(r'tgme_widget_message_views[^>]*>\s*([^<]+?)\s*<', blk)
        txt = ''
        tm = re.search(r'tgme_widget_message_text[^>]*>(.*?)</div>', blk, re.S)
        if tm:
            x = re.sub(r'<br\s*/?>', '\n', tm.group(1))
            x = re.sub(r'<[^>]+>', '', x)
            txt = html.unescape(x).strip()
        rx = {}
        for r in re.finditer(r'<span class="tgme_reaction"><i class="emoji"[^>]*><b>(.*?)</b></i>([\d.,]+[KM]?)</span>', blk, re.S):
            rx[html.unescape(r.group(1)).strip()] = r.group(2)
        media = re.findall(r'https://cdn\d*\.telesco\.pe/file/[^\'"\s)]+', blk)
        out[pid] = {'time': t.group(1) if t else '', 'views': v.group(1) if v else '',
                    'text': txt, 'rx': rx, 'media': media[:6]}
    return out

def rxsum(rx):
    tot = 0
    for v in rx.values():
        vv, mult = str(v).replace(',', '.'), 1
        if vv.endswith('K'):
            mult, vv = 1000, vv[:-1]
        try:
            tot += int(float(vv) * mult)
        except Exception:
            pass
    return tot

print('=' * 76)
print('A) ТГК stalzone: НОВЫЕ/ИЗМЕНЁННЫЕ посты (1148 vs 1144):')
newp = parse_tg('tg_stalzone_page0_20261014_1148.html')
oldp = parse_tg('tg_stalzone_page0_20261014_1144.html')
for pid in sorted(newp, key=lambda x: int(x.split('/')[1])):
    p, o = newp[pid], oldp.get(pid)
    if o is None:
        print(f'\n  ### НОВЫЙ {pid} {p["time"]} views={p["views"]} Σ={rxsum(p["rx"])} {p["rx"]}')
        print(f'  TEXT:\n  ---\n{p["text"]}\n  ---')
        if p['media']:
            print(f'  MEDIA: {p["media"]}')
    else:
        ds = rxsum(p['rx']) - rxsum(o['rx'])
        if ds or p['text'] != o['text'] or p['views'] != o['views']:
            drx = {k: (o['rx'].get(k), p['rx'].get(k)) for k in set(o['rx']) | set(p['rx']) if o['rx'].get(k) != p['rx'].get(k)}
            print(f'  {pid} ДЕЛЬТА Σ={ds:+d} views {o["views"]}->{p["views"]} {drx}')
            if p['text'] != o['text']:
                print(f'    !! ТЕКСТ ИЗМЕНЁН: new={p["text"][:120]!r}')

print('=' * 76)
print('B) ТГК spectrum: новые/изменённые (1148 vs предыдущий):')
cands = sorted(glob.glob('tg_spectrum_zone_page0_*.html'))
olds = [c for c in cands if not c.endswith('1148.html')]
newsp = parse_tg('tg_spectrum_zone_page0_20261014_1148.html')
oldsp = parse_tg(olds[-1]) if olds else {}
for pid in sorted(newsp, key=lambda x: int(x.split('/')[1])):
    p, o = newsp[pid], oldsp.get(pid)
    if o is None:
        print(f'\n  ### НОВЫЙ {pid} {p["time"]} views={p["views"]} Σ={rxsum(p["rx"])} {p["rx"]}')
        print(f'  TEXT: {p["text"][:400]}')
    else:
        ds = rxsum(p['rx']) - rxsum(o['rx'])
        if ds:
            drx = {k: (o['rx'].get(k), p['rx'].get(k)) for k in set(o['rx']) | set(p['rx']) if o['rx'].get(k) != p['rx'].get(k)}
            print(f'  {pid} ДЕЛЬТА Σ={ds:+d} {drx}')

print('=' * 76)
print('C) 196411: судьба #48 + новые посты (1148 vs 1144):')
na, nposts, nu = load_disc(f'discussion_196411_near999999_{NEW}.json')
oa, oposts, ou = load_disc(f'discussion_196411_near999999_{OLD}.json')
ou = {**ou, **nu}
print(f"  cc {oa.get('commentCount')} -> {na.get('commentCount')}; last {oa.get('lastPostedAt')} -> {na.get('lastPostedAt')}; sticky={na.get('isSticky')} locked={na.get('isLocked')}")
p48n = next((p for p in nposts if p['number'] == 48), None)
p48o = next((p for p in oposts if p['number'] == 48), None)
if p48n:
    sha = hashlib.sha256(p48n['html'].encode()).hexdigest()
    print(f"  #48: hiddenAt={p48n['hiddenAt']} isApproved={p48n['isApproved']} rx_sum={sum(p48n['rx'].values())} likes={p48n['likes']} edits? sha256 {'OK e352e6a1' if sha == 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e' else '!! ИЗМЕНИЛСЯ: ' + sha}")
    print(f"  #48 rx nonzero: { {k: v for k, v in p48n['rx'].items() if v} }")
else:
    print('  !!! #48 ИСЧЕЗ ИЗ ОКНА — проверка по postsindex off40')
oldnums = {p['number'] for p in oposts if p['number']}
for p in sorted(nposts, key=lambda x: x['number'] or 0):
    n = p['number']
    if n and n not in oldnums:
        who = ou.get(p['uid'], f"uid{p['uid']}")
        hid = f" hiddenAt={p['hiddenAt']}" if p['hiddenAt'] else ''
        print(f"  NEW #{n} [{p['ct']}] {p['createdAt']} {who}{hid}: {strip_h(p['html'])[:160]}")

print('=' * 76)
print('D) postsindex off40_1148: карта хвоста + #48 alive:')
d = json.load(open('postsindex_196411_off40_20261014_1148.json'))
nums = []
for inc in (d.get('included', []) or []) + norm_data(d):
    if isinstance(inc, dict) and inc.get('type') == 'posts':
        a = inc.get('attributes', {})
        if a.get('number'):
            nums.append((a['number'], a.get('hiddenAt')))
nums.sort()
print(f'  номера off40: {[n for n, _ in nums]}')
print(f'  hidden в off40: {[n for n, h in nums if h] or "—"}')

print('=' * 76)
print('E) FRONTINDEX (1148): sticky + волна:')
fi = json.load(open(f'frontindex_off0_{NEW}.json'))
items = []
for x in norm_data(fi):
    a = x['attributes']
    items.append({'id': x.get('id'), 't': a.get('title', ''), 'created': a.get('createdAt'),
                  'last': a.get('lastPostedAt'), 'sticky': a.get('isSticky'), 'cc': a.get('commentCount')})
for it in items:
    if it['sticky']:
        print(f"  STICKY d/{it['id']} [{it['t'][:44]}] cc={it['cc']} last={it['last']}")
print('  волна (created >= 2026-10-14T10:00):')
for it in sorted([i for i in items if (i['created'] or '') >= '2026-10-14T10:00'], key=lambda x: x['created'] or ''):
    print(f"    d/{it['id']} [{it['t'][:44]}] created={it['created']} cc={it['cc']}")

print('=' * 76)
print('F) SEARCH «краш»/«вылетает»: топ по createdAt:')
for pat in ('search_krash', 'search_vyletaet'):
    sf = json.load(open(f'{pat}_{NEW}.json'))
    data = norm_data(sf)
    print(f'  {pat}: {len(data)} выдач')
    for x in sorted(data, key=lambda y: (y.get('attributes', {}).get('lastPostedAt') or ''), reverse=True)[:5]:
        a = x['attributes']
        print(f"    d/{x.get('id')} [{(a.get('title') or '')[:44]}] created={a.get('createdAt')} last={a.get('lastPostedAt')} cc={a.get('commentCount')}")
print('\nANALYZE46_DONE')
