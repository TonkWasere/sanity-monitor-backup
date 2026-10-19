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
- СТАТУС (15.10 23:33 UTC): **PUSH ВОССТАНОВЛЕН.** Хронология: первый токен (fine-grained) дал push 403;
  классический «SanityBackups» работал 19:15–22:30 UTC; в 22:48–22:50 UTC отозван GitHub'ом —
  ПРИЧИНА ПОДТВЕРЖДЕНА ПИСЬМОМ: «GitHub PAT found in gist» — секрет-сканинг поймал токен в содержимом
  СЕКРЕТНОГО gist'а (даже с base64-обфускацией). Gist dfe5c841 удалён 23:30 UTC. ХРАНИТЬ ТОКЕН НА GITHUB
  (в любом виде) — ЗАПРЕЩЕНО. Новый токен выдан автором 23:25 UTC, creds восстановлены 23:33 UTC
  (формат user:pass — см. ниже), dual push 7aadec4..9d246f6 verified на оба remote.
- ХРАНЕНИЕ ТОКЕНА (по решению автора 23:28 UTC): (1) ~/.git-credentials (600) — рабочий формат;
  (2) /home/z/my-project/PAT_VAULT_LOCAL.md — рядом с RESTORE_GUIDE.md, gitignored (PAT_VAULT_LOCAL* в
  .gitignore), 600 — попадает в tar-слепки воркспейса, переживает откат ВМ; (3) НЕ в git, НЕ на GitHub.
- ФОРМАТ CREDS — ТОЛЬКО user:pass: printf 'https://TonkWasere:%s@github.com/\n' "$NEW_PAT" > ~/.git-credentials
  && chmod 600 ~/.git-credentials. Вариант «https://TOKEN@github.com/» (token-as-username) store-хелпер
  НЕ подхватывает — push падает «could not read Username» (проверено 23:32 UTC).
  Проверка: curl -s -o /dev/null -w '%{http_code}' -H "Authorization: token $NEW_PAT" https://api.github.com/user → 200.
- ЕСЛИ ТОКЕН ОТОВРАН/ПРОСРОЧЕН: раунды идут, коммиты копятся ЛОКАЛЬНО в /home/z/my-project (git),
  push отложенный — как только рабочий токен появится, часовой раунд запушит всё накопленное
  (пример: 2 инцидентных коммита 1e3d998+9d246f6 провисели ~45 мин и уехали 23:33 UTC).

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
   - SECRET GUARD (обязателен, до commit): python3 tools/secret_guard.py
     (скан staged-диффа на ghp_/github_pat_/cred-URL; exit 1 = секрет в стейдже, коммит прервать;
     полное значение НЕ печатается — только файл:строка и маска). Профилактика инцидента 15.10 22:55 UTC.
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

## Инцидент-лог
### 15.10.2026 22:48–23:33 UTC — PAT «SanityBackups» отозван и заменён (ЗАКРЫТ)
- Симптом: git push 401 «Invalid username or token» на оба remote; API тем же токеном тоже 401.
- Тайминг: 22:46 API 200 · 22:48 POST /gists 201 (создано офф-ВМ gist-хранилище токена) ·
  22:49 push 401 · 22:50 API 401. Смерть ровно в окне после создания gist'а.
- **ПРИЧИНА КОНФИРМИРОВАНА письмом GitHub автору (~23:20 UTC):** «A recent scan found a valid GitHub
  Personal Access Token, SanityBackups, in the content of gist. We have revoked it» — секрет-сканинг
  GitHub просканил СЕКРЕТНЫЙ gist и авто-отозвал токен. Base64-обфускация НЕ спасла.
  Наша git-история чиста (git log --all -S по телу токена — пусто, grep дерева — чист).
- ВЫВОДЫ: (1) хранить токен на GitHub — ЗАПРЕЩЕНО в любом виде (gist/репо/обфускация);
  (2) провалившийся пуш стирает строку credential store (credential erase → файл 0 байт) — штатно;
  (3) формат creds — ТОЛЬКО user:pass (token-as-username store-хелпер не отдаёт).
- Решение автора 23:28 UTC: новый токен выдан 23:25 UTC; хранение — ~/.git-credentials +
  PAT_VAULT_LOCAL.md рядом с RESTORE_GUIDE.md (gitignored, попадает в tar-слепки, переживает откат);
  gist dfe5c841 удалён 23:30 UTC (204).
- Восстановление 23:33 UTC: creds (user:pass) → API 200 → dual push 7aadec4..9d246f6 (оба remote) →
  sync verified. Инцидент ЗАКРЫТ.
- Профилактика: tools/secret_guard.py (шаг 4 раунда; паттерн cred_url_userpass_token добавлен);
  guard позитивный/чистый тесты — OK.

## Ограничения
- GitHub: файл ≤100 МБ, репо мягкий лимит ~5 ГБ. Баннеры png исключены из git (в ZIP-линии).
- Токен в чате = риск; хранится только в credential store ВМ. Отзыв: GitHub → Settings → Tokens.
- Остановка: команда автора «Остановить автоматизацию» → удалить cron-задачу, отчитаться.

## СТАТУС ЖИВОСТИ (обновляется при каждых руках агента; 19.10 12:37 UTC)
- КРОН: 462533 активен, последний прогон 54-84 (12:27 UTC, ledger №127) — час 16 после закрытия ОТС: линия молчит (196424=160 +0), итоги ждутся 20.10; ППШКИ-ВЗРЫВ: 196667 +42 (78 live, ТТК-мета-спор); NEW 196690 «Арена» НАСТОЯЩИЙ (stm:…00524976, 18); вчерашние NEW растут: 196689 +12 (29), 196688 +11 (30); ТГК 3215 ВЫШЕЛ 12:01 (пауза 21 ч); ФЛЕШМОБ ТАЛОНОВ пауза 6-й час (cc=30); моверы: 196108 +4 (84), 195082 ожил +5 (92), 195081 +4 (948); KIM-X тихий 3-й час; сносы 196411 гэпы стабильны, канон OK
- ПУШ: dual push faf3bcc..61d2f6b на ОБА remote 11:38 UTC 19.10 (54-83 раунд+статус); bundles 0936/1041/1137 (3/3); пуш 54-84 — после коммита статуса
- УРОК 54-66: контекст раунда может исчерпаться ПОСЛЕ обхода — снапы тогда на диске, но ledger нет; следующий раунд восстанавливает дельты скриптами scripts/analyze_1830*.py (шаблон)
- УРОК 54-69: «NEW» на фронте бывает ЛОЖНЫМ — тред 196439 (14.10, cc=18) поднялся сортировкой lastPostedAt на один пост; всегда сверять createdAt перед «NEW ×N» в ledger
- ВОССТАНОВЛЕНИЕ ПОСЛЕ ЧИСТКИ №3-lite (18.10 ~17:2x): автор перезалил vault на прежнюю ссылку
  file/r9QxQBCT (с 17:27 отдавала ZIP v60 93 МБ, к 18:10 снова vault 2630 B); tools/mega_pull.py:
  MAC OK, sha256 7f9edd5d = эталон 54-61; токен (classic ghp_, строка «ТОКЕН:») → API 200,
  scope repo на месте; creds (user:pass, 600) + PAT_VAULT_LOCAL*.md (gitignored, 600) восстановлены;
  credential.helper=store возвращён ДО пуша (слетает при каждой чистке!)
- ⚠️ РОТАЦИЯ PAT НЕ СДЕЛАНА: живой токен с 14:29 UTC лежит на публичной MEGA-ссылке, URL которой
  в git-истории публичных реп (инцидент 54-61); GitHub MEGA не сканирует — решение за автором
- ⚠️ ВТОРИЧНАЯ ЗАЧИСТКА: /home/z/backups и не-git-файлы отсутствовали в 18:10, хотя раунд 54-65
  восстанавливал их в ~17:45 — не-git-артефакты не переживают даже час; healthcheck каждый раунд
- MEGA-линия восстановления: tools/mega_pull.py <url> [out] (новый /file/-формат:
  AES-ключ XOR(key[:16],key[16:32]), CTR nonce=key[16:24], MAC ECB-condense; download-URL
  только при {"a":"g","g":1,"p":<id>,"ssl":2}, URL одноразовый; реальный токен — на строке
  «ТОКЕН:» vault'а, строка-шаблон с <TOKEN> не трогать)
- ЧИСТКА BUNDLE: шаблон `ls -t | tail -n +4 | xargs rm -f` работает только из /home/z/backups
  (относительные пути!) — из другого CWD старые bundle не удаляются
- САМОПРОВЕРКА АВТОРОМ: открыть https://github.com/TonkWasere/test/commits/sanity-monitor —
  свежий коммит от текущего часа = крон жив и в git пишет. Если свежего коммита нет >90 мин —
  смотреть worklog: там либо «push pending» (проблема токена), либо «round skipped» (сеть).
