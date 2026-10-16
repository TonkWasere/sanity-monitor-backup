#!/usr/bin/env python3
# walk_parse.py — протокольный парсер обхода (Task 39, обход №26).
# Сверка дельт: свежие снапы vs предыдущие (в evidence_post), ТГК-дельты реакций,
# индексные карты по объединению off* (метод №26.1), frontindex, поиск.
# Запуск: python3 walk_parse.py [NEW_TS] [OLD_TS]   (по умолчанию — авто-детект)
import json, glob, re, html, os, sys

os.chdir('/home/z/my-project/output/evidence_post')
files_all = glob.glob('*.json') + glob.glob('*.html')
TSS = sorted({m.group(1) for f in files_all for m in [re.search(r'_(\d{8}_\d{4})\.', f)] if m})
NEW = sys.argv[1] if len(sys.argv) > 1 else TSS[-1]
OLD = sys.argv[2] if len(sys.argv) > 2 else (TSS[-2] if len(TSS) > 1 else None)
print(f'WALK_PARSE: NEW={NEW} OLD={OLD}')

def norm_data(d):
    """№26.2/№26.6: /api/posts кладёт посты в data[] (list), /api/discussions/{id} — объект в data (dict)."""
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
    # №26.2: посты могут лежать и в included[], и в data[] (корень /api/posts) — берём оба
    for inc in (d.get('included', []) or []) + norm_data(d):
        if isinstance(inc, dict) and inc.get('type') == 'posts':
            a = inc['attributes']
            posts.append({
                'id': inc.get('id'), 'number': a.get('number'),
                'createdAt': a.get('createdAt'), 'ct': a.get('contentType'),
                'html': a.get('contentHtml') or '',
                'rx': a.get('reactionCounts') or {}, 'likes': a.get('likesCount'),
                'uid': (inc.get('relationships', {}).get('user', {}) or {}).get('data', {}).get('id'),
            })
        elif inc.get('type') == 'users':
            users[inc.get('id')] = (inc.get('attributes', {}) or {}).get('username', '?')
    return attrs, posts, users

def strip_h(h):
    t = re.sub(r'<br\s*/?>', ' / ', h)
    t = re.sub(r'<[^>]+>', '', t)
    return html.unescape(re.sub(r'\s+', ' ', t)).strip()

def card_from_index(prefix, ts):
    nums = set(); meta = {}
    for p in sorted(glob.glob(f'{prefix}_off*_{ts}.json')):
        with open(p) as f:
            d = json.load(f)
        if not isinstance(d, dict):
            continue
        # №26.2: union data[] + included[]
        for inc in (d.get('included', []) or []) + norm_data(d):
            if isinstance(inc, dict) and inc.get('type') == 'posts':
                a = inc['attributes']
                n = a.get('number')
                if n:
                    nums.add(n)
                    meta[n] = {'ct': a.get('contentType'), 'createdAt': a.get('createdAt'), 'id': inc.get('id')}
    return nums, meta

print('=' * 72)
print('SECTION 1 — ДЕЛЬТЫ ТРЕДОВ (old -> new)')
TRACKED = [195574, 195660, 196033, 195889, 196062, 196074, 196078, 194423,
           196180, 196276, 196283, 196315, 196326, 196341, 196380, 196411]
for tid in TRACKED:
    nf = sorted(glob.glob(f'discussion_{tid}_near*_{NEW}.json'))
    if not nf:
        print(f'\n### d/{tid}: НЕТ НОВОГО СНАПА'); continue
    na, nposts, nu = load_disc(nf[-1])
    line = f"\n### d/{tid} [{na.get('title','?')[:52]}]"
    of = sorted(glob.glob(f'discussion_{tid}_near*_{OLD}.json')) if OLD else []
    if of:
        oa, oposts, ou = load_disc(of[-1])
        ou = {**ou, **nu}
        occ = oa.get('commentCount'); ncc = na.get('commentCount')
        line += f"\n  cc {occ} -> {ncc} (d={None if occ is None or ncc is None else ncc-occ}); lastPostedAt {oa.get('lastPostedAt')} -> {na.get('lastPostedAt')}"
        if (oa.get('isSticky') != na.get('isSticky')) or (oa.get('isLocked') != na.get('isLocked')):
            line += f"\n  !! STATE: sticky {oa.get('isSticky')}->{na.get('isSticky')}, locked {oa.get('isLocked')}->{na.get('isLocked')}"
        oldnums = {p['number'] for p in oposts if p['number']}
        seen = []
        for p in sorted(nposts, key=lambda x: (x['number'] or 0)):
            n = p['number']
            if n and n not in oldnums:
                who = ou.get(p['uid'], f"uid{p['uid']}")
                seen.append(f"    NEW #{n} [{p['ct']}] {p['createdAt']} {who}: {strip_h(p['html'])[:170]}")
        line += ('\n  --- новые посты окна:\n' + '\n'.join(seen)) if seen else '\n  новых постов в окне нет'
    else:
        line += f"\n  (старого снапа нет) cc={na.get('commentCount')} last={na.get('lastPostedAt')}"
    print(line)

print('\n' + '=' * 72)
print('SECTION 2 — 51716 #524 и 188595 (точечные окна)')
for tid, near in ((51716, 524), (188595, 9)):
    nf = f'discussion_{tid}_near{near}_{NEW}.json'
    if not os.path.exists(nf):
        print(f'd/{tid}: нового окна нет'); continue
    na, nposts, nu = load_disc(nf)
    of = f'discussion_{tid}_near{near}_{OLD}.json' if OLD else None
    occ = load_disc(of)[0].get('commentCount') if (of and os.path.exists(of)) else '?'
    print(f"\n### d/{tid} cc {occ} -> {na.get('commentCount')}")
    if tid == 51716:
        for p in nposts:
            if p['number'] == 524:
                print(f"  #524 reactions {p['rx']} likes {p['likes']}")
                if of and os.path.exists(of):
                    for q in load_disc(of)[1]:
                        if q['number'] == 524:
                            print(f"  (old) reactions {q['rx']} likes {q['likes']}")
    else:
        nums = sorted([p['number'] for p in nposts if p['number']])
        print(f"  окно номера: {nums}")

print('\n' + '=' * 72)
print('SECTION 3 — ИНДЕКСНЫЕ КАРТЫ (объединение off*, метод №26.1)')
for tid in (195660, 196283, 196315, 196326, 196276):
    nn, nmeta = card_from_index(f'postsindex_{tid}', NEW)
    onums, ometa = (None, {})
    if OLD and glob.glob(f'postsindex_{tid}_off*_{OLD}.json'):
        onums, ometa = card_from_index(f'postsindex_{tid}', OLD)
    mx = max(nn) if nn else 0
    gaps = sorted(set(range(1, mx + 1)) - nn)
    comment_ct = sum(1 for n in nn if nmeta[n]['ct'] == 'comment')
    line = f'\n### d/{tid}: карта {len(nn)} постов, max #{mx}, гэпы: {gaps if gaps else "нет"} (comment={comment_ct}, events={len(nn)-comment_ct})'
    if onums is not None:
        lost = sorted(onums - nn)
        gained = sorted(nn - onums)
        line += f'\n  vs {OLD}: ИСЧЕЗЛИ {lost if lost else "—"}; ПОЯВИЛИСЬ {gained if gained else "—"}'
        if lost:
            for n in lost:
                m = ometa.get(n, {})
                line += f'\n    !! #{n} ИСЧЕЗ: ct={m.get("ct")} createdAt={m.get("createdAt")} id={m.get("id")} — кандидат на снос'
        for n in gained:
            m = nmeta.get(n, {})
            line += f'\n    +#{n}: ct={m.get("ct")} createdAt={m.get("createdAt")}'
    print(line)

print('\n' + '=' * 72)
print('SECTION 4 — FRONTINDEX (закрепы + новые треды)')
fi = sorted(glob.glob(f'frontindex_off0_{NEW}.json'))[-1]
d = json.load(open(fi))
items = []
for x in norm_data(d):
    a = x['attributes']
    items.append({'id': x.get('id'), 't': a.get('title', ''), 'created': a.get('createdAt'),
                  'last': a.get('lastPostedAt'), 'sticky': a.get('isSticky'),
                  'locked': a.get('isLocked'), 'cc': a.get('commentCount')})
print('ЗАКРЕПЛЕНЫ (sticky):')
for it in items:
    if it['sticky']:
        print(f"  d/{it['id']} [{it['t'][:46]}] cc={it['cc']} last={it['last']}")
print('НОВЫЕ ТРЕДЫ (createdAt >= 2026-10-12T12:00):')
for it in sorted([i for i in items if (i['created'] or '') >= '2026-10-12T12:00'], key=lambda x: x['created'] or ''):
    print(f"  d/{it['id']} [{it['t'][:46]}] created={it['created']} cc={it['cc']} last={it['last']} sticky={it['sticky']}")

print('\n' + '=' * 72)
print('SECTION 5 — ПОИСК «Неизбежность» (караул набор №2)')
sf = sorted(glob.glob(f'search_neizbezhnost_{NEW}.json'))[-1]
d = json.load(open(sf))
data = norm_data(d)
print(f'  всего выдач: {len(data)}')
for x in sorted(data, key=lambda y: (y.get('attributes', {}).get('createdAt') or ''), reverse=True)[:6]:
    a = x['attributes']
    print(f"  d/{x.get('id')} [{(a.get('title') or '')[:40]}] created={a.get('createdAt')} cc={a.get('commentCount')}")

print('\n' + '=' * 72)
print('SECTION 6 — ТГК stalzone + spectrum_zone')

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
        # №26.4 (фикс регрессии; канон №21.1): <span class="tgme_reaction"><i class="emoji"...><b>ЭМОДЗИ</b></i>COUNT</span>
        rx = {}
        for r in re.finditer(r'<span class="tgme_reaction"><i class="emoji"[^>]*><b>(.*?)</b></i>([\d.,]+[KM]?)</span>', blk, re.S):
            rx[html.unescape(r.group(1)).strip()] = r.group(2)
        media = re.findall(r'https://cdn\d*\.telesco\.pe/file/[^\'"\s)]+', blk)
        links = re.findall(r'href="(https?://(?:www\.)?(?:youtube\.com|youtu\.be|vkvideo\.ru|vk\.com|forum\.exbo\.net)[^"]+)"', blk)
        out[pid] = {'time': t.group(1) if t else '', 'views': v.group(1) if v else '',
                    'text': txt[:200], 'rx': rx, 'media': media[:4], 'links': links[:4]}
    return out

def rxsum(rx):
    tot = 0
    for v in rx.values():
        vv, mult = str(v).replace(',', '.'), 1
        if vv.endswith('K'): mult = 1000; vv = vv[:-1]
        elif vv.endswith('M'): mult = 1000000; vv = vv[:-1]
        try: tot += int(float(vv) * mult)
        except: pass
    return tot

for chan in ('stalzone', 'spectrum_zone'):
    newf = f'tg_{chan}_page0_{NEW}.html'
    cands = sorted(glob.glob(f'tg_{chan}_page0_*.html'))
    oldf = [c for c in cands if c != newf]
    oldf = oldf[-1] if oldf else None
    newp = parse_tg(newf)
    oldp = parse_tg(oldf) if oldf else {}
    nums = sorted(int(p.split('/')[1]) for p in newp)
    print(f'\n### t.me/{chan} (new={newf}, old={oldf}): видимых постов {len(newp)}, диапазон {nums[0] if nums else "-"}..{nums[-1] if nums else "-"}')
    for pid in sorted(newp, key=lambda x: int(x.split('/')[1])):
        p = newp[pid]
        o = oldp.get(pid)
        base = f'  {pid} {p["time"]} views={p["views"]} Σ={rxsum(p["rx"])} {p["rx"]}'
        if o:
            dsum = rxsum(p['rx']) - rxsum(o['rx'])
            drx = {k: (o['rx'].get(k), p['rx'].get(k)) for k in set(o['rx']) | set(p['rx']) if o['rx'].get(k) != p['rx'].get(k)}
            print(base + (f' | ДЕЛЬТА Σ={dsum:+d} {drx}' if (dsum or drx) else ' | без изменений'))
        else:
            print(base + ' | (в старом снапе нет / НОВЫЙ)')
            print(f'      text: {p["text"][:180]!r}')
            if p['media']: print(f'      media: {p["media"]}')
            if p['links']: print(f'      links: {p["links"]}')
print('\nWALK_PARSE_DONE')
