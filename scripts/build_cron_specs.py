#!/usr/bin/env python3
# build_cron_specs.py — строит output/08_monitoring/cron_specs/jobs.json (эталон 3 cron-задач)
# Спека v1 = живое состояние на 24.10 08:4x UTC (cron list, все 3 succeeded).
# job_id в спеке — «последний известный», НЕ авторитетный: авторитетны name+schedule+payload.
# Запуск: python3 scripts/build_cron_specs.py (перезапись после ЛЮБОГО изменения промптов кронов).
import json, hashlib, os

HOURLY_MSG = "Часовой раунд мониторинга forum.exbo.net (режим «пока автор не скажет Остановить автоматизацию»). Сначала прочитай /home/z/my-project/output/08_monitoring/GIT_AUTOMATION.md (плейбук: «Линии отказоустойчивости» + раздел «Внешние источники — часовая линия EXT») и последние 2-3 задачи /home/z/my-project/worklog.md. Затем: (0) ЗДОРОВЬЕ-ПРОВЕРКА ПЕРВЫМ ШАГОМ: python3 tools/state_healthcheck.py — если файлы/репо мертвы (worklog/ledger/плейбук/tools отсутствуют, git fsck fail, ветка не sanity-monitor): python3 tools/state_healthcheck.py --recover (автоматическая вытяжка с GitHub: clone -b sanity-monitor → rsync в /home/z/my-project) и продолжить раунд; если гэп последнего коммита >3 ч — работать дальше, дельты за гэп покрыть одним резюме с пометкой «гэп N ч»; если ~/.git-credentials пропал — работать локально «push pending» и попросить автора новый токен; (1) гостевой обход форума (UA Chrome, sleep 1с, JSON-валидация, скрипты-образцы tools/rescan54_22_fetch.py / rescan54_22b_phase2.py, TS в имена файлов): news-витрина, фронт-индекс, ключевые треды 196452 (Талоны/Доставки ПВЭ), 196488+196480 (Кейс/шансы/компенсация — обещана 16.10), 196511 (Хотфикс 15.10), 196424 (ОТС 16-18.10, старт 18:00 МСК 16.10), 196411 (union-карта postsindex off0/20/40 + канон #48 sha256 e352e6a1d81de147d8c330f6e5eeb46b0aeb276ea51d6ba67fe34aa57a7e5b0e; волна сносов: #63-70, ритм ~1/час), 196461 (Раздутый ттк), 196435 (Колизей-калибровка, Crios-фидбек), 196428, 196283, 196078, 196062, контролы 196315/196415; новые OP (near=1) для тредов, которых не было в прошлом раунде; снапы в output/evidence_post/; (1b) ВНЕШНИЕ ИСТОЧНИКИ (решение автора 23.10: «раз в час обязательно, на предмет Новостей или потенциально ценной информации, а также сравнения»): python3 tools/ext_sources.py — ТГК t.me/s/stalzone (офф) + t.me/s/spectrum_zone (фан, датамайны/сливы), Steam-новости RU+EN app/1818450, VK-статьи группы -2677092; скрипт сам печатает события '>>> EXT ...' (новые посты ТГК с просмотрами, новые Steam-новости RU/EN, новые/изменённые VK-статьи) — включи их в ledger-резюме шага (2) с коротким сравнением (RU↔EN посты разработчиков, ТГК↔форум, скорость реакции); state output/08_monitoring/ext_sources_state.json руками не трогать; (2) резюме дельт: append в output/08_monitoring/ledger.md (очередной №) и append в worklog.md (Task ID: 54-<номер часа UTC>, Work Log + Stage Summary); (3) git-фиксация: cd /home/z/my-project && git add -A && git commit -m 'hourly round <UTC timestamp>: <дельта>' && git push origin sanity-monitor 2>&1 | tail -2 && git push backup sanity-monitor 2>&1 | tail -2 && git bundle create /home/z/backups/sanity-monitor-$(date -u +%Y%m%d_%H%M).bundle sanity-monitor (двойной push: origin=github.com/TonkWasere/test + backup=github.com/TonkWasere/sanity-monitor-backup; зеркало-ветка origin sanity-monitor-mirror обновляется раз в сутки или при сомнениях; bundle старше 3 шт чистить из /home/z/backups: ls -t | tail -n +4 | xargs rm -f; если push упал 403/401 — push pending: токен без прав или отозван, коммит остаётся локальным, пометь в worklog; если прошёл — пометь 'pushed'); НИКОГДА не записывай строку токена в файлы/логи/коммиты; (4) НЕ публиковать на форуме (read-only), НЕ собирать ZIP-версии, НЕ трогать /tmp-стейджи чужих процессов. Lite-линии (SNAP15 cron :10/:25/:40/:55, SNAP35 cron :35) НЕ трогать и их cron-задачи не удалять. Если автор сказал «Остановить автоматизацию» — удалить эту cron-задачу (и только её) и отчитаться. Если сеть/форум недоступны — записать в worklog 'round skipped: сеть недоступна' и завершиться без ошибок."

SNAP15_MSG = "Lite-линия SNAP15 мониторинга forum.exbo.net (молодые треды раз в 15 мин — решение автора «в первые 1-2ч нового Треда проверка раз в 15мин»; регламент: /home/z/my-project/output/08_monitoring/GIT_AUTOMATION.md, раздел «Линия молодых тредов»). Действия СТРОГО минимальные: (0) если /home/z/my-project/worklog.md или репо мертвы — сначала python3 tools/state_healthcheck.py --recover; если после этого tools/snap15_young.py отсутствует — завершиться без ошибок (lite skipped, часовой раунд разберётся). (1) cd /home/z/my-project && python3 tools/snap15_young.py — скрипт сам: дельты LPN/cc молодых тредов (ВЫРЕЗЫ = рост гэпа), VANISH (404 x2), isHidden, reconcile свежих createdAt в очередь, выпуск >2h в graduated. (2) Если вывод содержит события (строки '>>> ...' с NEW RECONCILE-ADD / ВЫРЕЗ / VANISH / GRADUATED) — append ОДНУ строку в /home/z/my-project/worklog.md в формате 'Task ID: 54-<час UTC>-s15' + одна строка сути; тихий прогон — НИЧЕГО не писать в worklog. (3) ЗАПРЕЩЕНО: любые git-команды (add/commit/push/bundle — фиксация только в часовых раундах), записи в ledger.md, полный обход форума, ЛЮБЫЕ записи на форум (read-only), трогать /tmp-стейджи, публиковать токены. Если сеть/форум недоступны — завершиться без ошибок, ничего не писать. Если автор сказал «Остановить автоматизацию» — удалить эту cron-задачу и отчитаться."

SNAP35_MSG = "Lite-линия SNAP35 мониторинга forum.exbo.net (снап в :35 UTC = 5 мин после часового обхода ~:28, чисто на предмет новых тредов, рождённых «очень близко» к окну обхода — решение автора; регламент: /home/z/my-project/output/08_monitoring/GIT_AUTOMATION.md, раздел «Линия молодых тредов»). Действия СТРОГО минимальные: (0) если репо мёртв — сначала python3 tools/state_healthcheck.py --recover; если после этого tools/snapnew35.py отсутствует — завершиться без ошибок. (1) cd /home/z/my-project && python3 tools/snapnew35.py — скрипт сам: newlist sort=-createdAt, NEW = createdAt ≤3h вне KNOWN (union prev_lpn + rescan-KNOWN + young), верификация near=1, stm-твинк-детект (username 'stm:*'), постановка в young-очередь (TTL 2h — дальше их сопровождает SNAP15 каждые 15 мин). (2) Если скрипт напечатал строки '>>> NEW <id> ...' — append ОДНУ строку в /home/z/my-project/worklog.md в формате 'Task ID: 54-<час UTC>-s35: NEW <id> «title» OP <user> [STM] lpn/cc X/Y → young 2h'; если new=0 — НИЧЕГО не писать в worklog. (3) ЗАПРЕЩЕНО: любые git-команды (add/commit/push/bundle), записи в ledger.md, полный обход форума, ЛЮБЫЕ записи на форум (read-only), трогать /tmp-стейджи, публиковать токены. Если сеть/форум недоступны — завершиться без ошибок. Если автор сказал «Остановить автоматизацию» — удалить эту cron-задачу и отчитаться."

JOBS = [
    {
        "key": "hourly",
        "last_known_job_id": 472526,
        "name": "forum.exbo.net hourly sanity-monitor round (multi-repo redundancy)",
        "schedule": {"kind": "fixed_rate", "expr": "3600", "tz": ""},
        "payload": {"kind": "agentTurn", "message": HOURLY_MSG},
        "priority": 10,
        "notes": "priority 10 (пересоздавать с params.priority=10); fixed_rate=дрейфует от длительности прогона",
    },
    {
        "key": "snap15",
        "last_known_job_id": 472472,
        "name": "forum.exbo.net SNAP15: young threads every 15min (first 1-2h)",
        "schedule": {"kind": "cron", "expr": "0 10,25,40,55 * * * ?", "tz": "UTC"},
        "payload": {"kind": "agentTurn", "message": SNAP15_MSG},
        "priority": None,
        "notes": "создана 24.10 00:26 UTC; priority не задавалась",
    },
    {
        "key": "snap35",
        "last_known_job_id": 472471,
        "name": "forum.exbo.net SNAP35: new-thread snap 5min after hourly round",
        "schedule": {"kind": "cron", "expr": "0 35 * * * ?", "tz": "UTC"},
        "payload": {"kind": "agentTurn", "message": SNAP35_MSG},
        "priority": None,
        "notes": "создана 24.10 00:26 UTC; priority не задавалась",
    },
]

OUT = '/home/z/my-project/output/08_monitoring/cron_specs/jobs.json'
os.makedirs(os.path.dirname(OUT), exist_ok=True)
spec = {
    "_meta": {
        "purpose": "Эталон cron-задач мониторинга forum.exbo.net (решение автора 24.10: хранить настройки кронов на гите; при несовпадении живых кронов со спекой — самовосстановление из неё, шаг 0c часового раунда, см. GIT_AUTOMATION.md)",
        "spec_version": 1,
        "captured_utc": "2026-10-24T08:45",
        "verified_by": "cron list 2026-10-24 08:4x UTC: 3/3 задач, все execution=succeeded",
        "authority": "АВТОРИТЕТНЫ name+schedule+payload.message; job_id и run_count — справочные (меняются при пересоздании)",
        "secret_check": "промпты не содержат токенов (только пути/команды); гит публичный",
        "update_rule": "после ЛЮБОГО изменения промпта/расписания крона — перегенерировать: python3 scripts/build_cron_specs.py",
    },
    "jobs": [],
}
for j in JOBS:
    e = dict(j)
    e["message_sha256"] = hashlib.sha256(j["payload"]["message"].encode('utf-8')).hexdigest()
    e["message_len"] = len(j["payload"]["message"])
    spec["jobs"].append(e)

json.dump(spec, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"OK: {OUT}")
for j in spec["jobs"]:
    print(f"  {j['key']}: id={j['last_known_job_id']} sha256={j['message_sha256'][:12]}… len={j['message_len']}")
