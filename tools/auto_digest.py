#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# auto_digest.py — 54-689: периодическая «Аналитика» (каждые 4ч по слоту :02, вызов из auto_tick).
# Источники: output/08_monitoring/timeline.jsonl (машинные события 24ч) + young_threads.json
# (stm-твинки) + scheduler_state.json (инциденты/недопуши) + ledger-хвост (WIPE-метки).
# Выход: output/01_analysis/monitoring_digest_YYYYMMDD_HHMM.md → коммитится обычным тиком.
# Правило тона: только наблюдаемые факты и цифры; никаких интерпретаций за автора кампании.
import json, os, re, glob, time
from collections import defaultdict

REPO = '/home/z/my-project'
MON = os.path.join(REPO, 'output', '08_monitoring')
TIMELINE = os.path.join(MON, 'timeline.jsonl')
ANALYSIS = os.path.join(REPO, 'output', '01_analysis')
SCHED = os.path.join(MON, 'scheduler_state.json')
YOUNG = os.path.join(MON, 'young_threads.json')


def parse_ts(s):
    try:
        return time.mktime(time.strptime(s, '%Y-%m-%dT%H:%M:%SZ'))
    except Exception:
        return 0


def load_24h():
    now = time.time()
    cut = now - 24 * 3600
    recs = []
    try:
        with open(TIMELINE, encoding='utf-8') as f:
            for ln in f:
                try:
                    r = json.loads(ln)
                except Exception:
                    continue
                if parse_ts(r.get('ts', '')) >= cut:
                    recs.append(r)
    except FileNotFoundError:
        pass
    return recs


def iso_hm(s):
    return (s or '')[11:16]


def main():
    recs = load_24h()
    longs = [r for r in recs if r.get('line') == 'long30']
    now = time.gmtime()
    stamp = time.strftime('%Y%m%d_%H%M', now)
    date_h = time.strftime('%d.%m.%Y %H:%M', now)

    # --- агрегация движения: первый cc_old → последний cc_new по каждому tid ---
    first_old, last_new, titles, last_gap = {}, {}, {}, {}
    sig_total = newthreads = 0
    special, vanish_seen, oww_seen = [], [], set()
    ext_total = 0
    blocks = defaultdict(int)  # 2h-блоки: hour → Δcc сумма
    wipes = 0
    for r in longs:
        for ns in r.get('newsigs', []):
            tid = str(ns.get('tid'))
            try:
                co = int(ns.get('cc_old'))
                cn = int(ns.get('cc_new'))
            except (TypeError, ValueError):
                continue
            if tid not in first_old:
                first_old[tid] = co
            last_new[tid] = cn
            titles[tid] = ns.get('title') or '?'
            if ns.get('gap'):
                last_gap[tid] = ns['gap']
            blocks[int(r['ts'][11:13]) // 2 * 2] += cn - co
        sig_total += r.get('sig', 0) or 0
        newthreads += len(r.get('newthreads', []))
        for sp in r.get('spec', []):
            special.append((r['ts'], sp))
        for v in r.get('vanish', []):
            vanish_seen.add(v['tid'])
        for t in r.get('oww_fail', []):
            oww_seen.add(t)
        ext_total += r.get('ext', 0) or 0
        if r.get('healed'):
            wipes += 1

    movers = []
    for tid in last_new:
        if tid in first_old and last_new[tid] > first_old[tid]:
            movers.append((last_new[tid] - first_old[tid], tid))
    movers.sort(reverse=True)

    # вспышки: Δcc ≥ 30 за скользящие 6ч (упрощённо: по записи одного прохода или сумме соседних)
    flashes = []
    per_tid_series = defaultdict(list)
    for r in longs:
        t = parse_ts(r.get('ts', ''))
        for ns in r.get('newsigs', []):
            try:
                d = int(ns['cc_new']) - int(ns['cc_old'])
            except (TypeError, ValueError):
                continue
            per_tid_series[str(ns['tid'])].append((t, d, r['ts']))
    for tid, series in per_tid_series.items():
        series.sort()
        for i in range(len(series)):
            w = [x for x in series if series[i][0] <= x[0] <= series[i][0] + 6 * 3600]
            s6 = sum(x[1] for x in w)
            if s6 >= 30:
                flashes.append((s6, tid, series[i][2]))
    flashes = sorted(set(flashes), reverse=True)[:6]

    # stm-твинки из young
    stm_n = 0
    try:
        y = json.load(open(YOUNG, encoding='utf-8'))
        pool = list(y.get('threads', {}).values()) + list(y.get('graduated', {}).values())
        stm_n = sum(1 for e in pool if isinstance(e, dict) and e.get('stm'))
    except Exception:
        pass

    sched = {}
    try:
        sched = json.load(open(SCHED, encoding='utf-8'))
    except Exception:
        pass

    # ledger-хвост: свежие WIPE-номера
    wipe_marks = []
    try:
        tail = open(os.path.join(MON, 'ledger.md'), encoding='utf-8', errors='ignore').read()[-60000:]
        wipe_marks = sorted(set(re.findall(r'WIPE-#(\d+)', tail)), key=int)[-3:]
    except Exception:
        pass

    # --- рендер ---
    L = []
    L.append(f'# Мониторинг-дайджест {date_h} UTC (auto 54-689, окно 24ч)')
    L.append('')
    L.append('## Активность')
    L.append(f'- проходов long30 за окно: {len(longs)}, дельт-сигнатур всего: {sig_total}, новых тредов: {newthreads}')
    if blocks:
        bar = ' '.join(f'{h:02d}h:{blocks[h]:+d}' for h in sorted(blocks))
        L.append(f'- активность (Δcc по 2-часовым блокам): {bar}')
    if stm_n:
        L.append(f'- stm-твинков в young-пуле (активные+graduated): {stm_n}')
    L.append('')
    L.append('## Топ-движение 24ч (по Δcc)')
    if movers:
        for d, tid in movers[:15]:
            gap = f' гэп {last_gap[tid]}' if tid in last_gap else ''
            L.append(f'1. [{tid}] «{titles[tid]}» +{d} → {last_new[tid]}{gap}')
    else:
        L.append('- данных за окно нет (пустой timeline?)')
    L.append('')
    L.append('## Вспышки (Δcc ≥ 30 за 6ч)')
    if flashes:
        for s6, tid, ts in flashes:
            L.append(f'- [{tid}] «{titles.get(tid, "?")}» +{s6}/6ч (окно от {iso_hm(ts)} UTC)')
    else:
        L.append('- вспышек порога не достигли')
    L.append('')
    L.append('## Сносы / спец-сигнатуры (DEL/MIX/UNHIDE/ROLLBACK)')
    if special:
        for ts, sp in special[:10]:
            L.append(f'- {iso_hm(ts)} [{sp.get("tid")}] {sp.get("label")} cc {sp.get("cc_old")}→{sp.get("cc_new")}'
                     + (f' гэп {sp.get("gap")}' if sp.get('gap') else ''))
    else:
        L.append(f'- чисто: спец-сигнатур за окно 0 (подряд без DEL: {sched.get("zero_del_streak", "?")} проходов)')
    L.append('')
    L.append('## VANISH / 404')
    if vanish_seen or oww_seen:
        ids = sorted(vanish_seen | oww_seen)
        L.append(f'- в 404/недоступе: {", ".join(str(i) for i in ids)}')
    else:
        L.append('- VANISH-событий за окно не зафиксировано')
    L.append('')
    L.append('## Внешние источники (TG/Steam/VK/YouTube)')
    L.append(f'- событий за окно: {ext_total}')
    L.append('')
    L.append('## Инциденты / система')
    if wipes:
        L.append(f'- авто-восстановлений (R2/R1) за окно: {wipes}')
    if sched.get('push_pending', 0):
        L.append(f'- НЕДОПУШ: {sched["push_pending"]} тиков ждут creds (R1 при следующем тике/чат-агенте)')
    if wipe_marks:
        L.append(f'- последние WIPE в леджере: #{"#, #".join(wipe_marks)}')
    if sched.get('ticks'):
        for ln, t in sorted(sched['ticks'].items()):
            L.append(f'- шедулер {ln}: последний тик {iso_hm(t.get("ts", ""))} UTC rc={t.get("rc")} '
                     f'({t.get("note", "ok")})')
    L.append('')
    L.append(f'*Авто-дайджест 54-689; машинные данные — timeline.jsonl ({len(recs)} записей за окно); '
             f'человеко-аудит — ledger.md.*')

    os.makedirs(ANALYSIS, exist_ok=True)
    dst = os.path.join(ANALYSIS, f'monitoring_digest_{stamp}.md')
    with open(dst, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    # keep-6 ротация дайджестов
    digs = sorted(glob.glob(os.path.join(ANALYSIS, 'monitoring_digest_*.md')), key=os.path.getmtime)
    for old in digs[:-6]:
        try:
            os.remove(old)
        except Exception:
            pass
    print(f'[auto_digest] выпущен {dst} ({len(L)} строк)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
