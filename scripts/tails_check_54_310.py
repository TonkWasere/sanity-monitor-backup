#!/usr/bin/env python3
# Task 54-310: целевые GET хвостовых тредов для Поста №3 «Хвосты» + статус-таблица
# read-only, гостевой API, авторская задача (не lite-тик)
import json, os, urllib.request, datetime
BASE = 'https://forum.exbo.net'
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
OUT = '/home/z/my-project/output/evidence_post'
os.makedirs(OUT, exist_ok=True)
NOW = datetime.datetime.now(datetime.timezone.utc)

TARGETS = {
    '196424': 'ОТС: тред теста (обещан «опрос на почту» по окончании)',
    '196425': 'ОТС: обсуждение теста',
    '196511': 'хотфикс 15.10 (официальное описание так и не вышло)',
    '196488': 'кейс/компенсация',
    '196480': 'компенсация (второй тред)',
    '196452': 'талонная линия',
    '196689': 'клан-жалоба',
    '196411': '«Игровые изменения вступили в силу» (канон #48)',
    '191642': 'вопросы по обвесам',
    '196062': 'что было ранее (сверка)',
}

def get(tid):
    name = f'discussion_{tid}_near999999_tailcheck_20261028_1045.json'
    path = os.path.join(OUT, name)
    if os.path.exists(path):
        with open(path, 'rb') as f: return json.loads(f.read())
    try:
        req = urllib.request.Request(f'{BASE}/api/discussions/{tid}', headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
        open(path, 'wb').write(body)
        return json.loads(body)
    except Exception as e:
        print(f'FAIL {tid}: {e}')
        return None

rows = []
for tid, note in TARGETS.items():
    d = get(tid)
    if not d:
        rows.append((tid, note, 'FAIL/404', '-', '-', '-'))
        continue
    a = d.get('data', {}).get('attributes', {})
    # последний пост: ищем в included самое свежее comment.createdAt
    last = None
    for inc in d.get('included', []):
        if inc.get('type') == 'posts':
            ca = inc.get('attributes', {}).get('createdAt')
            if ca and (last is None or ca > last):
                last = ca
    lpa = a.get('lastPostedAt', '')
    age_d = ''
    if lpa:
        dt = datetime.datetime.fromisoformat(lpa)
        age_d = f'{(NOW-dt).total_seconds()/86400:.1f}сут'
    rows.append((tid, note, f"cc={a.get('commentCount')}", f"lpn={a.get('lastPostNumber')}", f"lpa={lpa[:16].replace('T',' ')}", f"тишина={age_d}"))

print(f"{'ID':7} {'тред':48} {'счётчик':14} {'номер':10} {'последний пост':18} {'возраст':>9}")
for r in rows:
    print(f"{r[0]:7} {r[1][:48]:48} {r[2]:14} {r[3]:10} {r[4]:18} {r[5]:>9}")
