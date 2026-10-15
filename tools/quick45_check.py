#!/usr/bin/env python3
# quick45_check.py — доп-чек: OP sha256 (near1), скрытость адресатов (#28/#30/#31), ТГК-дельты.
import json, glob, re, html, hashlib, os

os.chdir('/home/z/my-project/output/evidence_post')

def norm_data(d):
    dd = d.get('data')
    if isinstance(dd, dict):
        return [dd]
    if isinstance(dd, list):
        return dd
    return []

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

print('1) OP #1 196411 sha256-чек (near1):')
h1 = hashlib.sha256(load_disc('discussion_196411_near1_20261014_1144.json')[1][0]['html'].encode()).hexdigest()[:16]
for ts in ('20261014_1500', '20261014_1042', '20261014_0940'):
    f = f'discussion_196411_near1_{ts}.json'
    if os.path.exists(f):
        _, ps, _ = load_disc(f)
        p1 = next((p for p in ps if p['number'] == 1), None)
        if p1:
            hh = hashlib.sha256(p1['html'].encode()).hexdigest()[:16]
            print(f'   vs {ts}: {hh} {"OK" if hh == h1 else "!! ИЗМЕНИЛСЯ"} (len={len(p1["html"])})')
print(f'   current: {h1}')

print('2) postsindex off0_1144: contentHtml у #1?')
d = json.load(open('postsindex_196411_off0_20261014_1144.json'))
for inc in (d.get('included', []) or []) + norm_data(d):
    if isinstance(inc, dict) and inc.get('type') == 'posts':
        a = inc.get('attributes', {})
        if a.get('number') == 1:
            print(f'   #1: contentHtml len={len(a.get("contentHtml") or "")} hiddenAt={a.get("hiddenAt")} isApproved={a.get("isApproved")}')

print('3) Адресаты и хвост: скрытость #28/#30/#31 + authors окна 39..48:')
users = {}
d2 = json.load(open('discussion_196411_near999999_20261014_1144.json'))
users_all = {}
for src in (d2, json.load(open('discussion_196411_near1_20261014_1144.json')), json.load(open('postsindex_196411_off20_20261014_1144.json'))):
    for inc in (src.get('included', []) or []):
        if isinstance(inc, dict) and inc.get('type') == 'users':
            users_all[inc.get('id')] = (inc.get('attributes', {}) or {}).get('username', '?')
for off in (0, 20, 40):
    d = json.load(open(f'postsindex_196411_off{off}_20261014_1144.json'))
    for inc in (d.get('included', []) or []) + norm_data(d):
        if isinstance(inc, dict) and inc.get('type') == 'posts':
            a = inc.get('attributes', {})
            n = a.get('number')
            if n in (28, 30, 31, 34):
                uid = (inc.get('relationships', {}).get('user', {}) or {}).get('data', {}).get('id')
                print(f"   #{n}: hiddenAt={a.get('hiddenAt')} isApproved={a.get('isApproved')} rx={a.get('reactionCounts') or {}} author={users_all.get(uid, uid)} createdAt={a.get('createdAt')}")
# хвост окна 39..48 с авторами
_, ps, _ = load_disc('discussion_196411_near999999_20261014_1144.json')
print('   окно near999999 (post -> автор):')
for p in sorted(ps, key=lambda x: x['number'] or 0):
    print(f"     #{p['number']} [{p['ct']}] {p['createdAt']} {users_all.get(p['uid'], p['uid'])} rx_total={sum(p['rx'].values())} likes={p['likes']}")

print('4) ТГК stalzone дельты (1144 vs 1122):')
def parse_tg(path):
    s = open(path, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'data-post="([^"]+)"(.*?)(?=data-post="|class="tgme_widget_message_divider|$)', s, re.S):
        pid, blk = m.group(1), m.group(2)
        t = re.search(r'<time datetime="([^"]+)"', blk)
        v = re.search(r'tgme_widget_message_views[^>]*>\s*([^<]+?)\s*<', blk)
        rx = {}
        for r in re.finditer(r'<span class="tgme_reaction"><i class="emoji"[^>]*><b>(.*?)</b></i>([\d.,]+[KM]?)</span>', blk, re.S):
            rx[html.unescape(r.group(1)).strip()] = r.group(2)
        out[pid] = {'time': t.group(1) if t else '', 'views': v.group(1) if v else '', 'rx': rx}
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
newp = parse_tg('tg_stalzone_page0_20261014_1144.html')
oldp = parse_tg('tg_stalzone_page0_20261014_1122.html')
for pid in sorted(newp, key=lambda x: int(x.split('/')[1])):
    p, o = newp[pid], oldp.get(pid)
    ds = rxsum(p['rx']) - rxsum(o['rx']) if o else None
    line = f"   {pid} views={p['views']} Σ={rxsum(p['rx'])} {p['rx']}"
    if o and ds:
        drx = {k: (o['rx'].get(k), p['rx'].get(k)) for k in set(o['rx']) | set(p['rx']) if o['rx'].get(k) != p['rx'].get(k)}
        print(line + f' | ДЕЛЬТА Σ={ds:+d} {drx}')
    elif o:
        print(line + ' | без изменений')
    else:
        print(line + ' | НОВЫЙ/нет в старом')
print('\nQUICK45_DONE')
