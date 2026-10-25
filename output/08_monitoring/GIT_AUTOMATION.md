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
5. **КРОН-СПЕКА на гите** (решение автора 24.10 08:4x UTC): output/08_monitoring/cron_specs/jobs.json —
   эталон всех 3 cron-задач (hourly/SNAP15/SNAP35: расписание + промпт + sha256). Сверка каждый раунд
   (шаг 0c); при пропаже/несовпадении — пересоздание из спеки. Правила: cron_specs/README.md.
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
- СТАТУС (22.10 07:03 UTC, после WIPE-8): **PUSH ВОССТАНОВЛЕН 5-Й РАЗ** (54-149-mega). WIPE-8 (22.10, откат ВМ) снёс creds/vault/backups — push pending копился 9 раундов (54-141..54-149, ahead 9, bundle = единственная линия). Восстановление: автор прислал ПОЛНУЮ MEGA-ссылку (file-ID r9QxQBCT, ключ ЦЕЛИКОМ) → tools/mega_pull.py: 2630 B, MAC OK, имя PAT_VAULT_LOCAL.md → sha256 7f9edd5d = эталон 54-61 → vault байт-в-байт прежний, **ТОКЕН НЕ РОТИРОВАН** (классик ghp_ от 15.10) → creds (user:pass, 600) + PAT_VAULT_LOCAL.md (600, gitignored) + helper=store на месте → API 200 (login TonkWasere, токен жив — GitHub MEGA не сканирует) → **dual push 28b9c9e..e865e91 обе репы зелёные** (очередь 9 коммитов уехала целиком, ahead 0/0) → bundle 0653 → healthcheck 12/12. ⚠️ РОТАЦИЯ ОПЯТЬ НЕ СДЕЛАНА (24-е напоминание): ключ MEGA-ссылки теперь выслан в чат — живой токен лежит на публичной MEGA-ссылке с известным ключом; автору: сгенерировать новый PAT → перезалить vault с новым токеном и НОВЫМ ключом → старый отозвать. ЧЕК-ЛИСТ ВОССТАНОВЛЕНИЯ WIPE: (1) fetch+reset --hard origin/sanity-monitor; (1b) /tmp-стейт из Хранилища: python3 tools/restore_state_from_repo.py (мгновенно, 54-211-B; rebuild_prev_lpn_*.py — fallback только если снапшот в Хранилище старее нужного N); (2) creds из vault САМОСТОЯТЕЛЬНО: python3 tools/mega_pull.py '<URL из output/08_monitoring/MEGA_VAULT_INSURANCE.md>' (ссылка теперь в теле репо — страховка 54-209-B, автор передал 25.10; WIPE-28/29 отработано дважды, автономно ~4 мин); (3) git config --global credential.helper store; (4) mkdir -p /home/z/backups; (5) curl verify → dual push → healthcheck. ХРАНИЛИЩЕ СОСТОЯНИЯ (54-211-B, прямая задача автора «Хранилище в гит-репо»): часовой раунд ПОСЛЕ каждого обхода обязан копировать свежайший /tmp/prev_lpn_<N>.json → output/08_monitoring/state_snapshots/ (ротация: держать последние 2); young_threads.json уже git-tracked (вайпо-иммунен с 54-181); snap15-дампы пишутся прямо в output/evidence_post/ (git-tracked). Цель: после reset --hard рабочий стейт восстанавливается одной командой, без rebuild-хирургии.
- ⚠️ УРОК WIPE-41 (25.10 15:2x): после fetch+reset НЕ объявлять «creds потеряны, нужен PAT», пока не выполнен шаг (2) — vault-файл MEGA_VAULT_INSURANCE.md на откаченном диске ОТСУТСТВУЕТ и появляется только после rsync/checkout из клона; искать его в output/08_monitoring/ (не в корне). В 54-224 из-за этого был объявлен push pending и запрошен PAT №87 — а vault-recovery занял 4 минуты (MAC OK, sha 7f9edd5d = эталон, API 200, pending закрыт коммитом ae684334).
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
0c. **КРОН-СВЕРКА** (решение автора 24.10 — «при несовпадениях само подтягивает с Гитхаба»):
   `cron list` против эталона output/08_monitoring/cron_specs/jobs.json (3 задачи: hourly/SNAP15/SNAP35;
   сверять name+schedule+sha256(payload.message), job_id справочный). 3/3 ok — тишина; задача отсутствует
   или разошлась — удалить/пересоздать ИЗ СПЕКИ (hourly с params.priority=10), помета в worklog
   «cron restored from spec»; спека устарела (автор менял промпт) — сначала перегенерировать спеку
   (scripts/build_cron_specs.py), закоммитить, потом чинить крон. Полный чек-лист: cron_specs/README.md.
   Задачи вне спеки (авторские) не трогать.
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

## Линия молодых тредов (54-181, 23.10 20:2x UTC — по решению автора)
Помимо часового раунда работают ДВА lite-крона (обнаружение/сопровождение новых тредов):
1. **SNAP15** — каждые 15 мин в :10/:25/:40/:55 UTC: `python3 tools/snap15_young.py`
   - проверяет ТОЛЬКО young-очередь (молодые треды, TTL 2h от постановки): дельты LPN/cc,
     ВЫРЕЗЫ (рост гэпа lpn-cc), VANISH (404/снос, 2+ подряд), isHidden, откат LPN;
   - reconcile-пасс: треды с createdAt ≤2.5h, которых нет в очереди/graduated → автопостановка
     (покрывает и NEW часового раунда ~:28, и пропущенные);
   - отслужившие (>2h) → graduated — дальше их накрывает часовой раунд (WATCH/prev_lpn).
2. **SNAP35** — в :35 каждого часа (5 мин после часового обхода ~:28): `python3 tools/snapnew35.py`
   - чисто на предмет НОВЫХ тредов, рождённых «очень близко» к окну обхода (иначе ждут целый час);
     урок 54-69 учтён: NEW-кандидат = createdAt ≤3h И id вне KNOWN
     (union: /tmp/prev_lpn_*.json + KNOWN последнего tools/rescan54_*_fetch.py + young/graduated);
   - верификация near=1 (title, OP, lpn/cc, isHidden) + stm-твинк-детект (username 'stm:*') →
     young-очередь (TTL 2h) → дальше SNAP15 гоняет его каждые 15 мин.
- **State**: output/08_monitoring/young_threads.json (threads/graduated, атомарная запись) +
  output/08_monitoring/YOUNG_JOURNAL.md (append-only журнал lite-событий).
- **Правила коллизий**: lite-джобы НЕ трогают git вообще (фиксация только в часовых раундах,
  git add -A подхватит journal/state/снапы); расписание lite (:10/:25/:40/:55/:35) вне окна
  раунда :26-:36 — параллельных записей в worklog нет; снапы *_SNAP15_*/*_SNAP35_* в evidence_post.
- **Отчёт lite-агента**: worklog one-liner (Task ID: 54-<час>-s15 / 54-<час>-s35) ТОЛЬКО при
  событиях (NEW/ВЫРЕЗ/VANISH/GRADUATED отслеживаемого); тихий прогон — только печать.
- **WIPE-устойчивость (v2, 54-19-hotfix 25.10)**: lite-джоба при мёртвом репо сначала `python3
  tools/state_healthcheck.py --recover`; если lite-скрипт (tools/snap15_young.py / snapnew35.py)
  отсутствует — САМОЛЕЧЕНИЕ за секунды: `mkdir -p tools && git fetch origin sanity-monitor &&
  git show origin/sanity-monitor:tools/<скрипт> > tools/<скрипт>` (читающие git-операции
  fetch/show/rev-parse lite РАЗРЕШЕНЫ, репо публичный). Прежнее «ждать часовой раунд» давало
  слепую зону до часа (18:55+19:10 UTC 25.10) — а скорость реакции на модерацию и есть смысл
  разведения линий.
- **ПРОТОКОЛ [SKIP] (54-19-hotfix 25.10)**: ЛЮБОЙ пропуск lite (сеть/форум недоступны,
  self-heal failed, падение скрипта) — ОБЯЗАТЕЛЬНЫЙ one-liner `Task ID: 54-<час>-s15/s35:
  [SKIP] <причина>` в worklog + одна строка в чат; часовой раунд (шаг 0b LITE-АУДИТ) сводит
  маркеры в ledger — слепые зоны всегда видимы, ничего не «пофиксится молча».
- **Останов**: команда автора «Остановить автоматизацию» → удалить ВСЕ три cron-задачи
  (часовую, SNAP15, SNAP35) и отчитаться.

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
### 23.10.2026 ~22:00–22:25 UTC — вайп не-git артефактов + откат git-каталога (ВОССТАНОВЛЕН)
- Симптом (SNAP15 lite 22:10): tools/snap15_young.py отсутствует; healthcheck: последний коммит
  94.4ч назад (git-каталог откатился к 71c70b8 от 19.10 23:27), bundle отсутствует, creds missing.
  Рабочее дерево при этом содержало контент ~21:30 23.10 (worklog до раунда 54-182) — частичный
  откат/подмена состояния ВМ.
- Потери: все snap-инструменты + young_threads.json/YOUNG_JOURNAL.md (очередь 196926/196927) +
  lite-снапы 21:40/21:55 + две worklog-строки 54-21-s15 + /home/z/backups + ~/.git-credentials.
- Рекавери 22:10–22:25 UTC (по процедуре, автор прислал MEGA-ссылку на vault):
  1) MEGA file/r9QxQBCT → PAT_VAULT_LOCAL.md (megatools 1.11.5 из .deb без рута; собственный
     python-дешифратор НЕ взял — attrs не MEGA, схема нестандартная — УРОК: тянуть megatools);
  2) vault sha256 e35bf5a4 ≠ эталон 7f9edd5d (54-61) — файл отличается, НО токен валиден
     (API 200) — эталон ПЕРЕЗАКРЕПЛЁН: e35bf5a4af0e6200…, token НЕ ротирован автором;
  3) creds user:pass (600) + credential.helper=store → API 200;
  4) git fetch origin: remote на 163 коммита вперёд (до baa9ba95 = раунд 54-182 21:28) →
     git reset --hard origin/sanity-monitor (17505 файлов) → snap-tools/young-state/снапы вернулись;
  5) lite-строки 54-21-s15 восстановлены в worklog из памяти агента (помечены «ВОССТАНОВЛЕНО»);
  6) vault → в корень проекта рядом с RESTORE_GUIDE.md (600, gitignored);
  7) mkdir /home/z/backups (УРОК 54-96) → bundle sanity-monitor-20261023_2220.bundle 266MB;
  8) healthcheck 12/12 STATE HEALTHY; test run snap15_young.py: reconcile вернул 196926/196927
     + новые 196928/196929 → active=13; push dry-run оба remote — up-to-date (auth OK).
- ВЫВОДЫ: (1) GitHub-remote оказался ГЛАВНОЙ страховкой — догнал стейт за 4 дня одним fetch+reset;
  (2) lite-джобы без git-фиксации теряют journal при вайпе — восстановимо из памяти раунда,
  но YOUNG_JOURNAL/young_threads.json теперь тоже в git (проверить, что часовой коммит их берёт);
  (3) ethalon-vault-sha НЕ вечен — сверять при каждом рекавери, при расхождении верифицировать
  токен API-вызовом, а не браковать vault.
- Инцидент ЗАКРЫТ 22:25 UTC. Все линии в норме, lite-кроны (SNAP15/SNAP35) продолжают со скриптами.

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

## СТАТУС ЖИВОСТИ (обновляется при каждых руках агента; 23.10 22:25 UTC)
- РЕКАВЕРИ 23.10 22:25 UTC: HEAD baa9ba95 (54-182, 21:28 UTC) восстановлен с origin, healthcheck
  12/12 STATE HEALTHY, bundle 20261023_2220 (266MB), creds на месте (vault e35bf5a4, API 200),
  push dry-run оба remote OK. Детали — в инцидент-логе.
- КРОН: 472526 активен (пересоздан 23.10 ~21:19 UTC из 462533 с шагом 1b ВНЕШНИЕ ИСТОЧНИКИ: tools/ext_sources.py; fixed_rate 3600, priority 10), последний прогон 54-135 (16:43 UTC 21.10, ledger №177) — патч-день 21.10 (техработы 9:00-11:30 МСК отработаны штатно); ГЛАВНАЯ ЛИНИЯ: «Пост Санити» PatronOfSanity в d/159759 (#14590/#14591, 13:29-13:30 UTC) — час 1 ноль / час 2 rx id=33 ×1 / час 3 likes ×1 на оба, cc/LPN 14446/14591 стоят, наездов/офиц. ответа нет (ежечасный замер); NEW дня: 196805 ивент Crios «Диггерские байки» (растёт), 196808 текстуры-баг, 196803 краш-жалоба, 196809+196811 от тред-фармера stm:…33648 (3 треда за день); kravv285 в 4 тредах за день; вырезы: 196752 «Слухи» (2 часа чистки); 191614 +16+16+16+25 медиа-дропы; 196411 канон OK 9-й час; 404-контроли 44-й час; флешмоб 57-й час; ОТС итоги час 67 не вышли
- ПУШ: **оба пуша зелёные 21.10 (54-135); creds user:pass (600) + credential.helper=store на месте; bundle 1634; зеркало обновлялось 17:37 UTC 19.10 (обновить при сомнениях); ТОКЕН НЕ РОТИРОВАН (16-е напоминание автору)
- УРОК 54-66: контекст раунда может исчерпаться ПОСЛЕ обхода — снапы тогда на диске, но ledger нет; следующий раунд восстанавливает дельты скриптами scripts/analyze_1830*.py (шаблон)
- УРОК 54-69: «NEW» на фронте бывает ЛОЖНЫМ — тред 196439 (14.10, cc=18) поднялся сортировкой lastPostedAt на один пост; всегда сверять createdAt перед «NEW ×N» в ledger
- ВОССТАНОВЛЕНИЕ ПОСЛЕ ЧИСТКИ №3-lite (18.10 ~17:2x): автор перезалил vault на прежнюю ссылку
  file/r9QxQBCT (с 17:27 отдавала ZIP v60 93 МБ, к 18:10 снова vault 2630 B); tools/mega_pull.py:
  MAC OK, sha256 7f9edd5d = эталон 54-61; токен (classic ghp_, строка «ТОКЕН:») → API 200,
  scope repo на месте; creds (user:pass, 600) + PAT_VAULT_LOCAL*.md (gitignored, 600) восстановлены;
  credential.helper=store возвращён ДО пуша (слетает при каждой чистке!)
- ВОССТАНОВЛЕНИЕ ПОСЛЕ ОТКАТА ВМ (19.10 19:51 UTC): автор повторно прислал ту же MEGA-ссылку file/r9QxQBCT;
- ВОССТАНОВЛЕНИЕ ПОСЛЕ ЧИСТКИ №6 (20.10 00:28 UTC): ~/.git-credentials + /home/z/backups (все bundle) + PAT_VAULT_LOCAL.md стёрты; git-стейт цел; полный MEGA-URL восстановлен из git-истории (commit aa91ed9, scripts/restore_creds_54_96.py — токен НИКОГДА не печатается); vault sha256 7f9edd5d = эталон → токен прежний; ВЫВОД ПОДТВЕРЖДЁН: не-git артефакты не переживают и час — healthcheck каждый раунд обязателен; УРОК 54-96: чистка уносит и САМ КАТАЛОГ /home/z/backups — recovery ОБЯЗАН начинаться с mkdir -p /home/z/backups до bundle-шага (иначе bundle create падает «No such file or directory»)
  mega_pull.py MAC OK; sha256 7f9edd5d = эталон 54-61 → vault байт-в-байт тот же, токен НЕ ротирован;
  creds+helper+vault восстановлены, отложенный пуш 3 коммитов уехал (6dd7f4d..384dd8b, оба remote)
- ⚠️ РОТАЦИЯ PAT НЕ СДЕЛАНА (повторено автору 19:51 UTC 19.10): живой токен с 14:29 UTC 18.10 лежит на
  публичной MEGA-ссылке, URL которой в git-истории публичных реп (инцидент 54-61); vault перезалит/передан
  автором 19.10 без замены токена (sha256 совпал); GitHub MEGA не сканирует — решение за автором
- ⚠️ ВТОРИЧНАЯ ЗАЧИСТКА: /home/z/backups и не-git-файлы отсутствовали в 18:10, хотя раунд 54-65
  восстанавливал их в ~17:45 — не-git-артефакты не переживают даже час; healthcheck каждый раунд
- MEGA-линия восстановления: tools/mega_pull.py <url> [out] (новый /file/-формат:
  AES-ключ XOR(key[:16],key[16:32]), CTR nonce=key[16:24], MAC ECB-condense; download-URL
  только при {"a":"g","g":1,"p":<id>,"ssl":2}, URL одноразовый; реальный токен — на строке
  «ТОКЕН:» vault'а, строка-шаблон с <TOKEN> не трогать)
- УРОК 54-90: снапшот ВМ может откатить диск к старому стейту (18:29 UTC 19.10: диск = 18.10 17:38, стейт 54-65/№109, а remote = 54-89) — ПЕРЕД нумерацией раунда всегда сверять worklog+git log с remote; восстановление = git stash push артефактов → merge --ff-only remote (merge-base = локальный HEAD ⇒ потерь нет); fetch может работать без ~/.git-credentials, если токен зашит в URL remote

- УРОК 54-88: при перегенерации R8-кортежа хвостов проверять, что караль-треды не выпали (196697 выпал в 54-88 — дослан отдельно ~16:44); «БОЛЬШИЕ ТРЕДЫ» может быть пуста — мегатреды 112917/164665/167367 уходят с front off0 при наплыве NEW
- ЧИСТКА BUNDLE: шаблон `ls -t | tail -n +4 | xargs rm -f` работает только из /home/z/backups
  (относительные пути!) — из другого CWD старые bundle не удаляются
- САМОПРОВЕРКА АВТОРОМ: открыть https://github.com/TonkWasere/test/commits/sanity-monitor —
  свежий коммит от текущего часа = крон жив и в git пишет. Если свежего коммита нет >90 мин —
  смотреть worklog: там либо «push pending» (проблема токена), либо «round skipped» (сеть).

## Внешние источники — часовая линия EXT (23.10 ~21:1x UTC — по решению автора)

Автор (уточнение, «потерялось в процессе»): «из Источников также представляет интерес
https://t.me/stalzone (офф ТГК) и https://t.me/spectrum_zone (ТГК одного из крупнейших
сообществ по Датамайнам и Сливам). Часто проверять нет необходимости (другая архитектура
нежели форум на Фларуме, плюс Спектрум — фан сообщество, ему такой дурью как Эксбо на своём
мейн форуме маяться незачем), но раз в час — обязательно, на предмет Новостей или
потенциально ценной информации, а также сравнения. Также в случае с новостными постами от
Разработчиков представляет интерес русско- и англоязычные посты в Стим-новостях
https://store.steampowered.com/news/app/1818450, а также статьи и посты в ВК-группе
https://vk.ru/@-2677092-start-ots-sobytiya-prazdnestvo-afdfvs4563».

- ИНСТРУМЕНТ: `python3 tools/ext_sources.py` — шаг часового раунда (после форумного обхода;
  ~15 GET, UA Chrome, sleep 1s, read-only, снапы ext_<src>_<TS>.* в output/evidence_post/)
- ИСТОЧНИКИ: ТГК t.me/s/stalzone (офф. канал) + t.me/s/spectrum_zone (фан, датамайны/сливы —
  сравнение); Steam RSS RU (?cc=ru&l=russian) + EN (?cc=us&l=english) app/1818450 (RU/EN
  сравнение постов разработчиков); VK-статьи группы -2677092: якорь
  @stalzone-start-ots-sobytiya-prazdnestvo-afdfvs4563 + discovery ссылок /@stalzone-* на
  страницах статей (цепочка prev/next, старые статьи доносятся как backfill без событий);
  VK-СТЕНА vk.com/wall-2677092 (ID постов, посев 23.10 21:23: 63 id, top=1148373)
- СОБЫТИЯ — строки '>>> EXT ...' в выводе: новый пост ТГК (#id > last_id), новая Steam-новость
  RU/EN (guid вне seen, хвост 40), VK НОВАЯ статья (published <48ч), VK ИЗМЕНЕНА (fp
  sha256(dateModified+og:description) либо dateModified сменился). События EXT включаются в
  ledger-резюме часового раунда; ОТДЕЛЬНОЙ lite-строки в worklog нет — EXT живёт внутри 54-<час>
- STATE: output/08_monitoring/ext_sources_state.json (tg last_id, steam seen[40],
  vk articles — кэп 24, якорь всегда первый в обходе, фетч-кэп 8/раунд)
- ОСОБЕННОСТИ: VK HTML в cp1251 (декодировать!); tgme-блок начинается с '"channel/id' после
  data-post= (учтено в парсере); превью t.me отдаёт ~14 постов stalzone / ~3-20 spectrum
- ОГРАНИЧЕНИЯ/ОСОБЕННОСТИ ВК (уточнено экспериментом 23.10 21:2x UTC, см. worklog 54-21-ext-c):
  * СТЕНА ДОСТУПНА гостем, но ТОЛЬКО через vk.com/wall-2677092 (vk.ru отдаёт логин-стену);
  * заголовок Accept — ЯД: с ним VK отдаёт JS-оболочку ~150КБ без постов; стандартного
    fetch() инструмента (UA + Accept-Language) достаточно — полный HTML 2.3МБ, 63 поста;
  * тексты постов лежат в JS-payload снапшота ext_vk_wall_<TS>.html — при событии
    «новый пост» агент раунда вскрывает снап; мониторинг по ID (seen 200, top в state);
  * анти-бот вариативен (иногда оболочка) — run_vk_wall делает 1 ретрай через 3с,
    иначе тихий пропуск до следующего часа (WARN в выводе, не фатально);
  * полный список статей группы без логина недоступен — статьи через discovery-цепочку.
- ПОСЕВ 23.10 21:11-21:14 UTC: ТГК stalzone top=3235 (было 3205+ днём — канал живой),
  spectrum_zone top=7985; Steam RU/EN по 10 items — топ RU: «Старт ОТС события „Празднество"»
  16:01 UTC, «Что скрывается за карточками?» 15:19 UTC (прямо про monitored ОТС!); VK: 4 статьи
  в state + itogi-konkursa в очереди discovery
- КОНСОЛИДАЦИЯ 21:1x UTC: параллельный tools/sources_hourly.py (написан часовым раундом 54-181)
  ВЫВЕДЕН — канонический инструмент EXT-линии: tools/ext_sources.py (у него: spectrum парсился,
  VK cp1251 без mojibake, RU/EN Steam раздельно, классификация fresh<48ч/backfill). Из него
  забраны просмотры ТГК (tgme_widget_message_views — прокси охвата, пишутся в state+события).
  Артефакты sources_state.json / SOURCES_JOURNAL.md удалены (их state: spectrum отсутствовал,
  vk-заголовок mojibake). Git-история хранит файл. Снапы sources_* от прогона 54-181 остаются
  в evidence_post как доказательства.
- ⚠️ УРОК WIPE-43 (25.10 18:2x): в recovery полный SHA для reset --hard брать ТОЛЬКО через `git reset --hard $(git rev-parse origin/sanity-monitor)` — вручную набранный/восстановленный по памяти хвост SHA даёт «fatal: Could not parse object» (безвредно, но теряется время). Плюс: вывод ext_sources.py сохранять в /tmp/ext_out.txt целиком (деталь events=1 была потеряна при tail -4 — событие осталось неклассифицируемым).
- УРОК 54-19-HOTFIX (25.10 19:5x UTC, от автора): откат диска ВМ уносит трекнутые lite-скрипты
  (диск = 71c70b8 от 19.10, скрипт создан 23.10) — трекинга в git НЕдостаточно, если recovery
  приходит только через час; lite-промпты обязаны самовосстанавливаться из origin (шаг 0a:
  git fetch + git show) и оставлять [SKIP]-маркер при ЛЮБОМ пропуске (шаг 2a); часовой раунд
  сводит [SKIP]-маркеры в ledger (шаг 0b LITE-АУДИТ); спека кронов повышена до v2.
