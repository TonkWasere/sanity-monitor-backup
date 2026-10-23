# snap15_young.py — Task-линия «15 МИН / МОЛОДЫЕ ТРЕДЫ» (создан 54-181, 20:2x UTC 23.10,
# по решению автора: «в первые 1-2ч нового Треда — проверка раз в 15мин»).
# Лёгкий обход ТОЛЬКО молодых тредов (age < TTL 2h с момента постановки в очередь):
#   - дельты LPN/cc vs прошлый 15-мин замер (+N постов, ВЫРЕЗЫ = рост гэпа lpn-cc);
#   - VANISH (404/снос) и isHidden детект;
#   - reconcile-пасс: треды с createdAt <= 2.5h, отсутствующие в очереди/graduated
#     (включая найденные часовым раундом) → автопостановка в young-очередь.
# Принципы: ГОСТЕВОЙ read-only GET; НЕ ходит в git; НЕ пишет ledger/worklog (это делает
# lite-агент по факту событий); state = output/08_monitoring/young_threads.json;
# журнал = output/08_monitoring/YOUNG_JOURNAL.md; снапы = evidence_post/*_SNAP15_*.json.
# Расписание cron: :10/:25/:40/:55 UTC (вне часа раунда ~:28 и снапа :35).
import json, os, re, time, glob, urllib.request, sys
from datetime import datetime, timezone, timedelta

TS = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
OUT = '/home/z/my-project/output/evidence_post'
MON = '/home/z/my-project/output/08_monitoring'
YOUNG = os.path.join(MON, 'young_threads.json')
JOURNAL = os.path.join(MON, 'YOUNG_JOURNAL.md')
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36',
      'Accept': 'application/json'}
BASE = 'https://forum.exbo.net'
TTL_H = 2.0            # часы жизни в young-очереди (автор: «первые 1-2ч»)
RECON_WINDOW_H = 2.5   # глубина reconcile по createdAt
MAX_THREADS = 12       # потолок тредов за один проход (безопасность)

def now_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def journal(line):
    try:
        os.makedirs(MON, exist_ok=True)
        stamp = now_iso()
        if not os.path.exists(JOURNAL) or os.path.getsize(JOURNAL) == 0:
            with open(JOURNAL, 'a', encoding='utf-8') as f:
                f.write('# YOUNG_JOURNAL — lite-линия 15м/35м (54-181): молодые треды + снап новых\n\n')
        with open(JOURNAL, 'a', encoding='utf-8') as f:
            f.write(f'- {stamp} snap15 {line}\n')
    except Exception as e:
        print(f'journal fail: {e}')

def get_json(url, name):
    path = os.path.join(OUT, name)
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        d = json.loads(body)
        print(f'OK {name} ({len(body)}B)')
        return d
    except Exception as e:
        code = getattr(e, 'code', None)
        print(f'FAIL {name}: {e}' + (f' [HTTP {code}]' if code else ''))
        if os.path.exists(path):
            os.remove(path)
        return None, (code or str(e)) if code else str(e)

def discs(d):
    out = []
    if not isinstance(d, dict):
        return out
    data = d.get('data')
    for i in (data if isinstance(data, list) else [data] if data else []):
        if isinstance(i, dict) and i.get('type') == 'discussions':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'discussions':
            out.append(i)
    return out

def posts_of(d):
    out = []
    if not isinstance(d, dict):
        return out
    data = d.get('data')
    for i in (data if isinstance(data, list) else [data] if data else []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    for i in (d.get('included') or []):
        if isinstance(i, dict) and i.get('type') == 'posts':
            out.append(i)
    return out

def load_young():
    if os.path.exists(YOUNG):
        try:
            return json.load(open(YOUNG, encoding='utf-8'))
        except Exception as e:
            print(f'young load fail: {e}')
    return {'_meta': {'version': 1, 'note': 'young-thread queue (54-181)'},
            'threads': {}, 'graduated': {}}

def save_young(y):
    tmp = YOUNG + '.tmp'
    os.makedirs(MON, exist_ok=True)
    json.dump(y, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(tmp, YOUNG)

def parse_ts(s):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

def main():
    y = load_young()
    threads = y.setdefault('threads', {})
    graduated = y.setdefault('graduated', {})
    now = datetime.now(timezone.utc)

    # 1) выпуск отслуживших (> TTL) — дальше их накрывает часовой раунд (WATCH/prev_lpn)
    for tid in sorted(list(threads.keys())):
        until = parse_ts(threads[tid].get('until_ts') or '')
        if until and until < now:
            e = threads.pop(tid)
            e['graduated_at'] = now_iso()
            e['checks_done'] = e.get('checks', 0)
            graduated[tid] = e
            journal(f'{tid} GRADUATED (2h отслужил, checks={e.get("checks_done")}) — накрывает часовой раунд')
    print(f'young активных: {len(threads)}, graduated всего: {len(graduated)}')

    # 2) проверка молодых (near=999999: cc/lpn + хвост постов)
    events = []
    ordered = sorted(threads.keys(), key=lambda t: threads[t].get('discovered_at') or '')
    for tid in ordered[:MAX_THREADS]:
        e = threads[tid]
        r = get_json(f'{BASE}/api/discussions/{tid}?page[near]=999999',
                     f'discussion_{tid}_near999999_SNAP15_{TS}.json')
        time.sleep(1)
        if isinstance(r, tuple) or r is None:
            _, err = (r if isinstance(r, tuple) else (None, 'no response'))
            e['fails'] = e.get('fails', 0) + 1
            e['last_error'] = str(err)[:80]
            line = f'{tid} CHECK FAIL x{e["fails"]} ({e["last_error"]})'
            if e['fails'] >= 2:
                line += ' — VANISH? (2+ подряд; title: ' + (e.get('title') or '?')[:40] + ')'
            print(f'>>> {line}')
            journal(line)
            events.append(line)
            continue
        e['fails'] = 0
        da = (r.get('data') or {}).get('attributes', {}) if isinstance(r.get('data'), dict) else {}
        lpn = da.get('lastPostNumber') or 0
        cc = da.get('commentCount') or 0
        hidden = da.get('isHidden')
        old_l, old_c = e.get('last_lpn', 0), e.get('last_cc', 0)
        d_lpn, d_cc = lpn - old_l, cc - old_c
        gap_now, gap_old = lpn - cc, old_l - old_c
        parts = []
        if d_lpn > 0:
            parts.append(f'+{d_lpn}')
        if d_lpn < 0:
            parts.append(f'LPN ОТКАТ {d_lpn}')
        if gap_now > gap_old:
            parts.append(f'ВЫРЕЗ +{gap_now - gap_old} (гэп {gap_old}→{gap_now})')
        elif gap_now < gap_old:
            parts.append(f'гэп смягчился {gap_old}→{gap_now}')
        if hidden:
            parts.append('isHidden=True')
        # номера пропавших постов (best-effort по хвосту)
        if gap_now > gap_old and d_lpn >= 0:
            nums = {p.get('attributes', {}).get('number') for p in posts_of(r)}
            missing = sorted(set(range(old_l + 1, lpn + 1)) - nums)
            if missing:
                parts.append(f'битые номера: {missing}')
        e['last_lpn'], e['last_cc'] = lpn, cc
        e['checks'] = e.get('checks', 0) + 1
        e['last_checked'] = now_iso()
        if parts:
            line = f'{tid} «{(e.get("title") or "?")[:40]}» lpn/cc {old_l}/{old_c}→{lpn}/{cc}: ' + '; '.join(parts)
            print(f'>>> {line}')
            journal(line)
            events.append(line)
        else:
            print(f'  {tid}: без дельт ({lpn}/{cc}, check #{e["checks"]})')

    # 3) reconcile: свежие createdAt вне очереди/graduated → автопостановка
    d = get_json(f'{BASE}/api/discussions?sort=-createdAt&page[size]=30&page[offset]=0',
                 f'newlist_created30_SNAP15_{TS}.json')
    recon_added = 0
    if isinstance(d, dict):
        time.sleep(1)
        cut = now - timedelta(hours=RECON_WINDOW_H)
        for i in discs(d):
            a = i.get('attributes') or {}
            try:
                ct = datetime.fromisoformat(a.get('createdAt') or '')
            except Exception:
                continue
            tid = str(i.get('id'))
            if ct >= cut and tid not in threads and tid not in graduated:
                threads[tid] = {
                    'title': a.get('title') or '?', 'slug': a.get('slug') or '',
                    'createdAt': a.get('createdAt'), 'op_user': '?',
                    'stm': False, 'discovered_at': now_iso(), 'source': 'snap15-reconcile',
                    'until_ts': (now + timedelta(hours=TTL_H)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'last_lpn': a.get('lastPostNumber') or 0, 'last_cc': a.get('commentCount') or 0,
                    'checks': 0,
                }
                recon_added += 1
                line = (f'{tid} RECONCILE-ADD «{(a.get("title") or "?")[:44]}» '
                        f'createdAt {a.get("createdAt")} lpn/cc {a.get("lastPostNumber")}/{a.get("commentCount")} → young({TTL_H:.0f}h)')
                print(f'>>> {line}')
                journal(line)
                events.append(line)
    save_young(y)
    print(f'>>> итог: active={len(threads)} graduated={len(graduated)} recon_add={recon_added}')
    print(f'DONE SNAP15: events={len(events)}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
