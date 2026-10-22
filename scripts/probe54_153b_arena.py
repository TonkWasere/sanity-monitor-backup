#!/usr/bin/env python3
# probe54_153b_arena.py — Task 54-153b (внераундовый, ~11:1x UTC 22.10): АД-ХОК ПРОБА
# по наводке АВТОРА: «ОФФ раздуплился на анонс Арены Митрополита (узнал с Дискорда),
# в ТГК сталзоны тоже есть пост». Гостевой read-only обход: фронт-индекс + news-витрина
# + поиск «арена»/«митрополит» + TG stalzone/спектрум; найденное — OP near=1 + хвост.
# UA Chrome, sleep 1s, JSON-валидация, TS в именах файлов. Секретов не трогает.
import json, os, time, datetime, urllib.request

BASE = 'https://forum.exbo.net'
OUT = '/home/z/my-project/output/evidence_post'
now = datetime.datetime.now(datetime.UTC)
TS = now.strftime('%Y%m%d_%H%M')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

ok_n = fail_n = 0

def get(url, name, validate_json=True):
    global ok_n, fail_n
    path = os.path.join(OUT, name)
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
        if validate_json:
            data = json.loads(raw.decode('utf-8'))
            with open(path, 'w') as f:
                json.dump(data, f, ensure_ascii=False)
        else:
            with open(path, 'wb') as f:
                f.write(raw)
        ok_n += 1
        print(f"OK  {len(raw):>7}B  {name}")
        return data if validate_json else raw
    except Exception as e:
        fail_n += 1
        print(f"FAIL       {name}: {e}")
        return None

def items(fname):
    try:
        d = json.load(open(os.path.join(OUT, fname)))
        return d.get('data', [])
    except Exception:
        return []

def title_of(it):
    return (it.get('attributes') or {}).get('title', '')

def created_of(it):
    return (it.get('attributes') or {}).get('createdAt', '')

def posts_count(it):
    a = it.get('attributes') or {}
    return a.get('commentCount') or a.get('postsCount') or 0

print(f"=== PROBE 54-153b АРЕНА-МИТРОПОЛИТА @ {TS} UTC ===")

# 1. Фронт-индекс + news-витрина
get(f'{BASE}/api/discussions?page[offset]=0', f'frontindex_off0_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions?filter[tag]=news&sort=-lastPostedAt&page[size]=50&page[offset]=0', f'tagnews_off0_{TS}.json'); time.sleep(1)

# 2. Поиски: арена / митрополит / митрополита
get(f'{BASE}/api/discussions?filter[q]=%D0%B0%D1%80%D0%B5%D0%BD%D0%B0&page[offset]=0', f'search_arena_{TS}.json'); time.sleep(1)
get(f'{BASE}/api/discussions?filter[q]=%D0%BC%D0%B8%D1%82%D1%80%D0%BE%D0%BF%D0%BE%D0%BB%D0%B8%D1%82&page[offset]=0', f'search_mitropolit_{TS}.json'); time.sleep(1)

# 3. TG-каналы
get('https://t.me/s/stalzone', f'tg_stalzone_page0_{TS}.html', validate_json=False); time.sleep(1)
get('https://t.me/s/spectrum_zone', f'tg_spectrum_page0_{TS}.html', validate_json=False); time.sleep(1)

# 4. Разбор: кандидаты про Арену Митрополита
cands = {}
for fname in (f'frontindex_off0_{TS}.json', f'tagnews_off0_{TS}.json',
              f'search_arena_{TS}.json', f'search_mitropolit_{TS}.json'):
    for it in items(fname):
        tid = it.get('id')
        t = title_of(it)
        if not tid:
            continue
        low = t.lower()
        if 'арен' in low or 'митрополит' in low:
            cands[tid] = {'title': t, 'createdAt': created_of(it), 'cc': posts_count(it), 'src': fname.split('_' + TS)[0]}

print(f"\n--- КАНДИДАТЫ АРЕНА/МИТРОПОЛИТ: {len(cands)} ---")
for tid, c in sorted(cands.items(), key=lambda kv: -int(kv[0] or 0)):
    print(f"  {tid}  cc={c['cc']}  created={c['createdAt']}  [{c['src']}]  «{c['title'][:90]}»")

# 5. Новые треды (createdAt после 09:30 UTC 22.10 — база 54-153)
fresh = []
for it in items(f'frontindex_off0_{TS}.json'):
    c = created_of(it)
    if c >= '2026-10-22T09:30':
        fresh.append((it.get('id'), title_of(it), c, posts_count(it)))
print(f"\n--- ФРЕШ (created >= 09:30 UTC): {len(fresh)} ---")
for tid, t, c, cc in fresh:
    print(f"  {tid}  cc={cc}  {c}  «{t[:80]}»")

# 6. OP-слепки кандидатов (near=1) + хвосты (near=999999, только для мелких)
for tid in cands:
    try:
        if int(tid) < 195000:
            continue  # старые треды серии не слепим целиком — фронт дал суть
    except ValueError:
        continue
    get(f'{BASE}/api/discussions/{tid}?page[near]=1', f'discussion_{tid}_near1_{TS}.json'); time.sleep(1)
    get(f'{BASE}/api/discussions/{tid}?page[near]=999999', f'discussion_{tid}_near999999_{TS}.json'); time.sleep(1)

print(f"\n=== PROBE DONE: OK={ok_n} FAIL={fail_n} ===")
