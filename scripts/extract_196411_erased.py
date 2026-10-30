#!/usr/bin/env python3
# extract_196411_erased.py — форензика: восстановление затёртых постов d/196411 из снапшотов.
# Сканирует ВСЕ discussion_196411_* и postsindex_196411_* в output/evidence_post/,
# строит карту «какие номера постов когда наблюдались», вычисляет текущие гэпы
# (union новейших postsindex off0/20/40 + новейший near999999) и восстанавливает
# полный текст каждого затёртого поста из последнего снапшота, где он был жив.
# Проверяет канон #48 (sha256). Результат -> output/08_monitoring/196411_erased_posts_recovery.md
import json, os, re, glob, hashlib, datetime

EV = '/home/z/my-project/output/evidence_post'
OUT_MD = '/home/z/my-project/output/08_monitoring/196411_erased_posts_recovery.md'
CANON48 = 'e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e'
UTC = datetime.timezone.utc

recs = []
for pat in ('discussion_196411_*.json', 'postsindex_196411_*.json'):
    for p in glob.glob(os.path.join(EV, pat)):
        try:
            recs.append((os.path.getmtime(p), p))
        except OSError:
            pass
recs.sort()
print(f'файлов снапшотов 196411: {len(recs)}')

def load(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return None

def items(d, typ):
    out = []
    if not isinstance(d, dict):
        return out
    data = d.get('data')
    for i in (data if isinstance(data, list) else [data] if data else []):
        if isinstance(i, dict) and i.get('type') == typ:
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == typ:
            out.append(i)
    return out

def mts(t):
    return datetime.datetime.fromtimestamp(t, UTC).strftime('%d.%m %H:%M')

seen = {}   # number -> {'meta','snaps','html'}
canon48 = []
for mt, p in recs:
    d = load(p)
    if d is None:
        continue
    fname = os.path.basename(p)
    users = {}
    for u in items(d, 'users'):
        ua = u.get('attributes', {}) or {}
        users[u.get('id')] = ua.get('username') or ua.get('displayName') or str(u.get('id'))
    for po in items(d, 'posts'):
        a = po.get('attributes', {}) or {}
        num = a.get('number')
        if num is None:
            continue
        num = int(num)
        uid = None
        try:
            ud = po['relationships']['user']['data']
            uid = (ud[0]['id'] if isinstance(ud, list) and ud else ud.get('id') if isinstance(ud, dict) else None)
        except Exception:
            pass
        author = users.get(uid, uid or '?')
        html = a.get('contentHtml') or ''
        meta = {'id': po.get('id'), 'createdAt': a.get('createdAt'), 'author': author,
                'likes': a.get('likesCount'),
                'rx': sum((a.get('reactionCounts') or {}).values()) if a.get('reactionCounts') else 0}
        r = seen.setdefault(num, {'meta': {}, 'snaps': [], 'html': ''})
        for k in ('id', 'createdAt', 'author'):
            if not r['meta'].get(k) and meta.get(k):
                r['meta'][k] = meta[k]
        r['meta']['likes'] = meta['likes'] if meta['likes'] is not None else r['meta'].get('likes')
        r['meta']['rx'] = max(r['meta'].get('rx') or 0, meta['rx'])
        if len(html) > len(r['html']):
            r['html'] = html
        r['snaps'].append((mt, fname))
        if num == 48 and html:
            canon48.append((mt, fname, hashlib.sha256(html.encode()).hexdigest()))

# --- текущий union и гэпы ---
newest_pi = [x for x in recs if 'postsindex_196411' in x[1]]
newest_disc = [x for x in recs if 'discussion_196411_near' in x[1]]
union = set()
for mt, p in (newest_pi[-3:] + newest_disc[-1:]):
    d = load(p)
    for po in items(d, 'posts'):
        n = (po.get('attributes') or {}).get('number')
        if n:
            union.add(int(n))
maxn = max(union) if union else 0
gaps = sorted(set(range(1, maxn + 1)) - union)
recovered = [g for g in gaps if g in seen]
missing = [g for g in gaps if g not in seen]
print(f'новейшие замеры: {[os.path.basename(p) for _, p in (newest_pi[-3:] + newest_disc[-1:])]}')
print(f'union 1..{maxn}, гэпы: {gaps}')
print(f'восстановимо: {recovered}')
print(f'НЕ попало ни в один снапшот: {missing}')

def strip_html(h):
    t = re.sub(r'<br\s*/?>', '\n', h)
    t = re.sub(r'</(p|div|blockquote|li)>', '\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    for a, b in (('&gt;', '>'), ('&lt;', '<'), ('&amp;', '&'), ('&quot;', '"'), ('&#039;', "'"), ('&nbsp;', ' ')):
        t = t.replace(a, b)
    return re.sub(r'\n{3,}', '\n\n', t).strip()

now = datetime.datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')
first_all = mts(recs[0][0]) if recs else '?'
last_all = mts(recs[-1][0]) if recs else '?'
L = []
L.append(f'# Восстановление затёртых постов d/196411 (форензика по снапшотам мониторинга)')
L.append('')
L.append(f'Сгенерировано: {now}. Просмотрено снапшотов: {len(recs)} (период наблюдения {first_all} — {last_all}).')
L.append('')
L.append(f'Текущий union-замер: посты 1..{maxn}; **гэпы (затёртые/скрытые номера): {gaps}**.')
L.append('')
L.append(f'Восстановлено из наших снапшотов: **{len(recovered)} из {len(gaps)}**.')
if missing:
    L.append(f'НЕ попали ни в один снапшот (созданы и стёрты между обходами, либо стёрты до старта мониторинга 14.10 ~09:40 UTC): {missing}.')
L.append('')
L.append('## Сводка по затёртым постам')
L.append('')
L.append('| № | создан | автор | в снапшотах | первый раз | последний раз |')
L.append('|---|--------|-------|-------------|------------|---------------|')
for g in gaps:
    if g in seen:
        r = seen[g]
        m = r['meta']
        L.append(f"| #{g} | {(m.get('createdAt') or '?')[:16]} | {m.get('author','?')} | {len(r['snaps'])} шт | {mts(r['snaps'][0][0])} ({os.path.basename(r['snaps'][0][1])}) | {mts(r['snaps'][-1][0])} ({os.path.basename(r['snaps'][-1][1])}) |")
    else:
        L.append(f'| #{g} | — | — | 0 | — | — |')
L.append('')
L.append('## Полные тексты восстановленных постов')
L.append('')
for g in recovered:
    r = seen[g]
    m = r['meta']
    snaps = r['snaps']
    first, last = snaps[0], snaps[-1]
    L.append(f'### Пост #{g}')
    L.append('')
    L.append(f"- id: `{m.get('id')}`; создан: **{(m.get('createdAt') or '?')}**; автор: **{m.get('author','?')}**; likes={m.get('likes')}, реакции={m.get('rx')}")
    L.append(f"- наблюдавался в {len(snaps)} снапшотах: {mts(first[0])} ({os.path.basename(first[1])}) -> {mts(last[0])} ({os.path.basename(last[1])})")
    L.append(f"- последнее наблюдение живым: {mts(last[0])} UTC; в следующем обходе уже отсутствовал (гэп)")
    L.append('')
    txt = strip_html(r['html'])
    L.append('> ' + '\n> '.join(txt.split('\n')) if txt else '> (пустой контент в снапшоте)')
    L.append('')
    L.append('<details><summary>сырой contentHtml</summary>')
    L.append('')
    L.append('```html')
    L.append(r['html'])
    L.append('```')
    L.append('')
    L.append('</details>')
    L.append('')
if missing:
    L.append('## Не восстановлено')
    L.append('')
    for g in missing:
        L.append(f"- #{g} — ни одного снапшота с этим номером (окно жизни пришлось на интервал между обходами, либо пост стёрт до 14.10 09:40 UTC)")
    L.append('')
ok48 = [c for c in canon48 if c[2] == CANON48]
bad48 = [c for c in canon48 if c[2] != CANON48]
L.append('## Канон #48')
L.append('')
if canon48:
    lastc = canon48[-1]
    L.append(f"Проверок содержимого #48: {len(canon48)}; sha256 совпадений с каноном: {len(ok48)}; расхождений: {len(bad48)}.")
    L.append(f"Последняя проверка: {mts(lastc[0])} ({lastc[1]}) — {'CANON OK' if lastc[2] == CANON48 else '!!! ИЗМЕНИЛСЯ: ' + lastc[2]}")
else:
    L.append('Пост #48 не встречен в снапшотах (вне окон off20/off40/last-page).')
L.append('')
open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(L))
print(f'отчёт: {OUT_MD} ({os.path.getsize(OUT_MD)}B)')
for mt, fn, h in canon48[-2:]:
    print(f'  #48 @ {mts(mt)} {fn}: {h[:16]}... {"OK" if h == CANON48 else "!!! CHANGED"}')
