# snapnew35.py — Task-линия «СНАП :35» (создан 54-181, 20:2x UTC 23.10, по решению автора)
# Лёгкий снап в :35 каждого часа (5 мин после часового обхода ~:28) ЧИСТО на предмет
# новых тредов, рождённых «очень близко» к окну обхода (урок 54-69: поднятие сортировкой
# и рождение сразу после обхода иначе ждут целый час).
# Принципы: ГОСТЕВОЙ read-only GET; НЕ ходит в git; НЕ пишет ledger/worklog (это делает
# lite-агент по факту находок); state = output/08_monitoring/young_threads.json;
# журнал = output/08_monitoring/YOUNG_JOURNAL.md.
# NEW-кандидаты: createdAt >= (now - 3h) И id вне KNOWN (union: /tmp/prev_lpn_*.json +
# KNOWN-сет последнего tools/rescan54_*_fetch.py + young/graduated). Проверка near=1,
# stm-твинк-детект (username начинается с 'stm:'), затем постановка в young-очередь (TTL 2h).
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
TTL_H = 2.0          # часы в young-очереди (автор: «первые 1-2ч нового треда»)
CAND_WINDOW_H = 3.0  # свежесть createdAt для NEW-кандидата
MAX_NEW = 6          # потолок постановки за один снап

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
            f.write(f'- {stamp} snap35 {line}\n')
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
        print(f'FAIL {name}: {e}')
        if os.path.exists(path):
            os.remove(path)
        return None

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

def users_of(d):
    m = {}
    for u in (d.get('included') or [] if isinstance(d, dict) else []):
        if isinstance(u, dict) and u.get('type') == 'users':
            m[str(u.get('id'))] = (u.get('attributes') or {}).get('username') or '?'
    return m

def known_ids():
    ids = set()
    for p in sorted(glob.glob('/tmp/prev_lpn_*.json')):
        try:
            ids |= set(json.load(open(p)).keys())
        except Exception:
            pass
    try:
        srcs = sorted(glob.glob('/home/z/my-project/tools/rescan54_*_fetch.py'))
        if srcs:
            src = open(srcs[-1], encoding='utf-8').read()
            m = re.search(r'KNOWN\s*=\s*\{([^}]*)\}', src, re.S)
            if m:
                ids |= {x for x in re.findall(r'\d{5,7}', m.group(1))}
    except Exception:
        pass
    return ids

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

def main():
    y = load_young()
    known = known_ids()
    known |= set(y.get('threads', {}).keys()) | set(y.get('graduated', {}).keys())
    print(f'KNOWN: {len(known)} id (prev_lpn + rescan-KNOWN + young)')

    d = get_json(f'{BASE}/api/discussions?sort=-createdAt&page[size]=30&page[offset]=0',
                 f'newlist_created30_SNAP35_{TS}.json')
    time.sleep(1)
    if d is None:
        journal('SKIP: сеть/форум недоступны (newlist FAIL)')
        print('DONE SNAP35: skip (no net)')
        return 0

    cut = datetime.now(timezone.utc) - timedelta(hours=CAND_WINDOW_H)
    users = users_of(d)
    cands = []
    for i in discs(d):
        a = i.get('attributes') or {}
        ca = a.get('createdAt') or ''
        try:
            ct = datetime.fromisoformat(ca)
        except Exception:
            continue
        if ct >= cut and str(i.get('id')) not in known:
            cands.append((str(i.get('id')), a, ct))
    cands.sort(key=lambda x: x[2], reverse=True)
    print(f'кандидаты NEW (createdAt >= {cut.isoformat()}, вне KNOWN): {len(cands)}')

    added = 0
    for tid, a, ct in cands[:MAX_NEW]:
        fn = f'discussion_{tid}_near1_SNAP35_{TS}.json'
        dd = get_json(f'{BASE}/api/discussions/{tid}?page[near]=1', fn)
        time.sleep(1)
        if dd is None:
            journal(f'NEW? {tid} верификация FAIL (404/снос до постановки?) — в очередь НЕ добавлен')
            continue
        da = (dd.get('data') or {}).get('attributes', {}) if isinstance(dd.get('data'), dict) else {}
        op_uid = str((((dd.get('data') or {}).get('relationships') or {}).get('user') or {}).get('data', {}).get('id', ''))
        op_user = users.get(op_uid) or (users_of(dd).get(op_uid) or '?')
        stm = op_user.lower().startswith('stm:')
        entry = {
            'title': da.get('title') or a.get('title') or '?',
            'slug': da.get('slug') or a.get('slug') or '',
            'createdAt': da.get('createdAt') or ct.isoformat(),
            'op_user': op_user,
            'stm': stm,
            'discovered_at': now_iso(),
            'source': 'snap35',
            'until_ts': (datetime.now(timezone.utc) + timedelta(hours=TTL_H)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'last_lpn': da.get('lastPostNumber') or 0,
            'last_cc': da.get('commentCount') or 0,
            'checks': 0,
        }
        y.setdefault('threads', {})[tid] = entry
        added += 1
        head = f'NEW {tid} «{entry["title"]}» OP {op_user}' + (' [STM-ТВИНК]' if stm else '') + \
               f' createdAt {entry["createdAt"]} lpn/cc {entry["last_lpn"]}/{entry["last_cc"]} → young({TTL_H:.0f}h)'
        print(f'>>> {head}')
        journal(head)

    save_young(y)
    print(f'>>> young очередь: {len(y.get("threads", {}))} активных, graduated {len(y.get("graduated", {}))}')
    print(f'DONE SNAP35: candidates={len(cands)} new={added}')
    return 0

if __name__ == '__main__':
    sys.exit(main())
