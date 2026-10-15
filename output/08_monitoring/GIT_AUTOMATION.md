# GIT_AUTOMATION.md — регламент часовой автоматизации (Task 53, режим «пока не скажу Остановить»)

## Цель
Полная независимость состояния мониторинга от ВМ: после каждого раунда всё содержимое
(worklog, ledger, снапы, инструменты, документы) уходит в GitHub-репо автора.
Рекавери = git clone. Работает до команды автора «Остановить автоматизацию».

## Линии отказоустойчивости (Task 54-hc, 15.10 22:25 UTC)
1. **origin** https://github.com/TonkWasere/test.git → ветка **sanity-monitor** (основная)
2. **backup** https://github.com/TonkWasere/sanity-monitor-backup.git → ветка **sanity-monitor**
   (второй репо, создан 15.10 22:23 тем же PAT; защита от удаления/порчи основного репо)
3. **origin** ветка **sanity-monitor-mirror** (зеркало основной ветки; защита от кривого push/force в основную)
4. **Локальный bundle** /home/z/backups/sanity-monitor-*.bundle (вне репо; защита от порчи GitHub-репозиториев;
   обновлять каждый раунд; восстановление: git clone sanity-monitor-*.bundle recovered)
Каждый раунд пушит В ОБА remote: `git push origin sanity-monitor && git push backup sanity-monitor`.
Health-check каждый раунд (шаг 0): `python3 tools/state_healthcheck.py` (12 проверок: файлы/директории,
fsck, ветка, creds, синхронизация origin+backup, гэп коммитов >3 ч, свежесть bundle).
При провале файлов/репо: `python3 tools/state_healthcheck.py --recover` — вытяжка с Гита (clone → rsync).
Если credentials пропали — коммить локально («push pending»), токен восстановить может только автор.

## Репозиторий
- remote: https://github.com/TonkWasere/test.git
- ВЕТКА: **sanity-monitor** (локальная ветка master переименована в sanity-monitor 15.10;
  default-ветка master на GitHub НЕ трогаем — по просьбе автора «в отд ветку»)
- push: `git push origin sanity-monitor`
- PAT аккаунта TonkWasere хранится локально в ~/.git-credentials (ВНЕ репо, chmod 600,
  credential.helper = store). Строка токена НИКОГДА не попадает в worklog/ledger/коммиты
  (публичный репо!) и в выводы логов.
- СТАТУС (15.10 19:15 UTC): **PUSH РАБОТАЕТ.** Первый токен (fine-grained) дал push 403
  (не хватало Contents:write); автор выдал классический токен — ls-remote OK, пуш прошёл:
  ветка sanity-monitor создана на GitHub, первые 4 коммита (b87396c…f58c8d1) уехали, master не тронут.
- ЕСЛИ ТОКЕН ОТОВРАН/ПРОСРОЧЕН: раунды идут, коммиты копятся ЛОКАЛЬНО в /home/z/my-project (git),
  push отложенный — как только рабочий токен появится в ~/.git-credentials, часовой раунд запушит всё накопленное.

## Часовой раунд (executed by cron agentTurn, fixed_rate 3600s)
0. **Health-check состояния** (ПЕРВЫМ ШАГОМ, до обхода): `python3 tools/state_healthcheck.py`.
   Если файлы/репо мертвы → `python3 tools/state_healthcheck.py --recover` (вытяжка с Гита) и продолжить раунд.
   Если гэп коммитов >3 ч (ВМ/cron ушёл погулять) → продолжить раунд, дельты за гэп покрыть одним резюме
   с пометкой «гэп N ч». Если credentials пропали → работать локально, «push pending», просить токен.
1. Прочитать хвост /home/z/my-project/worklog.md (последние 2-3 задачи) — не повторять уже сделанное.
2. Обход forum.exbo.net (гостевые GET, UA Chrome, sleep 1с, JSON-валидация):
   - news-витрина: /api/discussions?filter[tag]=news&sort=-lastPostedAt&page[size]=50&page[offset]=0
   - фронт: /api/discussions?page[offset]=0
   - ключевые линии (near=1 и/или near=999999): 196452 (Талоны/Доставки ПВЭ), 196488+196480 (Кейс),
     196411 (union-карта postsindex off0/20/40 + #48-канон sha256 e352e6a1…), 196424 (ОТС 16-18.10),
     196461 (Раздутый ттк), 196435 (Колизей-калибровка), 196428, 196283, 196078 (магпулы), 196062,
     контролы 196315/196415
   - ТГК: https://t.me/s/stalzone (новые посты после 3203, реакции)
   - новые OP (near=1) для тредов, которых не было в предыдущем раунде
   Снапы: /home/z/my-project/output/evidence_post/*_TS.json (+html)
   Скрипты-образцы: /home/z/my-project/tools/rescan53_fetch.py, rescan53b_fetch.py
3. Резюме раунда: append в /home/z/my-project/output/08_monitoring/ledger.md (№ очередная запись)
   + append в /home/z/my-project/worklog.md (шаблон Task ID: 54-<час>, секции Work Log / Stage Summary).
4. Git-фиксация:
   - cd /home/z/my-project
   - git add -A (gitignore отсекает zip/tar/png-баннеры/node_modules)
   - git commit -m "hourly round <UTC timestamp>: <краткое дельта-описание>"
   - ДВОЙНОЙ PUSH: `git push origin sanity-monitor` + `git push backup sanity-monitor`
     (если origin прошёл, backup упал — пометить «pushed origin, backup FAILED»; 401/403 —
     «push pending: токен отозван/без прав», коммит остаётся локальным)
   - Обновить bundle: `git bundle create /home/z/backups/sanity-monitor-$(date -u +%Y%m%d_%H%M).bundle sanity-monitor`
     (старые bundle >3 шт можно чистить: ls -t | tail -n +4 | xargs rm -f)
5. НЕ публиковать ничего на форуме (read-only), НЕ создавать ZIP-версии (это отдельная линия,
   только по чек-пойнтам/команде автора), НЕ трогать /tmp-стейджи.

## Рекавери-процедура (если ВМ откатилась/отвалилась/стейт ушёл погулять)
0. АВТОМАТИЧЕСКИ: `python3 tools/state_healthcheck.py --recover` — сам найдёт мёртвое, склонирует
   с origin, перенесёт контент и .git в /home/z/my-project. Ручной вариант:
1. git clone -b sanity-monitor https://github.com/TonkWasere/test.git → вернуть worklog.md, tools/, output/ тексты.
   (ветка по умолчанию на GitHub = master «Hello world» — мониторинг живёт в sanity-monitor).
2. Если origin-репо повреждён/удалён: `git clone -b sanity-monitor https://github.com/TonkWasere/sanity-monitor-backup.git`
3. Если оба GitHub-репо мертвы: локальный bundle `git clone /home/z/backups/sanity-monitor-<свежий>.bundle recovered`
4. Тяжёлое (ZIP vNN, png-баннеры) — из MEGA-оттяжки автора (свежая версия у автора всегда).
5. Продолжить раунды с нового HEAD. Если credentials пропали — работать локально (push pending),
   автор выдаёт новый токен (GitHub → Settings → Developer settings → Tokens, scope repo).

## Ограничения
- GitHub: файл ≤100 МБ, репо мягкий лимит ~5 ГБ. Баннеры png исключены из git (в ZIP-линии).
- Токен в чате = риск; хранится только в credential store ВМ. Отзыв: GitHub → Settings → Tokens.
- Остановка: команда автора «Остановить автоматизацию» → удалить cron-задачу, отчитаться.
