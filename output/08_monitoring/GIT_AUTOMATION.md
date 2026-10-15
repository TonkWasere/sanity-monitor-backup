# GIT_AUTOMATION.md — регламент часовой автоматизации (Task 53, режим «пока не скажу Остановить»)

## Цель
Полная независимость состояния мониторинга от ВМ: после каждого раунда всё содержимое
(worklog, ledger, снапы, инструменты, документы) уходит в GitHub-репо автора.
Рекавери = git clone. Работает до команды автора «Остановить автоматизацию».

## Репозиторий
- remote: https://github.com/TonkWasere/test.git
- push из ВМ возможен ТОЛЬКО с PAT (Personal Access Token) аккаунта TonkWasere.
  Пат хранится локально: `git config credential.helper store` + один раз выполненный push.
- БЕЗ токена: раунды идут, коммиты копятся ЛОКАЛЬНО в /home/z/my-project (git),
  push выполняется отложенно, как только токен появится.

## Часовой раунд (executed by cron agentTurn, fixed_rate 3600s)
1. Прочитать хвост /home/z/my-project/worklog.md (последние 2-3 задачи) — не повторять уже сделанное.
2. Обход forum.exbo.net (гостевые GET, UA Chrome, sleep 1с, JSON-валидация):
   - news-витрина: /api/discussions?filter[tag]=news&sort=-lastPostedAt&page[size]=50&page[offset]=0
   - фронт: /api/discussions?page[offset]=0
   - ключевые линии (near=1 и/или near=999999): 196452 (Талоны/Доставки ПВЭ), 196488+196480 (Кейс),
     196411 (union-карта postsindex off0/20/40 + #48-канон sha256 e352e6a1…), 196424 (ОТС 16-18.10),
     196428, 196283, 196078 (магпулы), 196062, контролы 196315/196415
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
   - git push origin master (если PAT настроен; иначе — commit остаётся локальным,
     в резюме отметить «push pending, нет PAT»)
5. НЕ публиковать ничего на форуме (read-only), НЕ создавать ZIP-версии (это отдельная линия,
   только по чек-пойнтам/команде автора), НЕ трогать /tmp-стейджи.

## Рекавери-процедура (если ВМ откатилась/отвалилась)
1. git clone https://github.com/TonkWasere/test.git → вернуть worklog.md, tools/, output/ тексты.
2. Тяжёлое (ZIP vNN, png-баннеры) — из MEGA-оттяжки автора (свежая версия у автора всегда).
3. Продолжить раунды с нового HEAD.

## Ограничения
- GitHub: файл ≤100 МБ, репо мягкий лимит ~5 ГБ. Баннеры png исключены из git (в ZIP-линии).
- Токен в чате = риск; хранится только в credential store ВМ. Отзыв: GitHub → Settings → Tokens.
- Остановка: команда автора «Остановить автоматизацию» → удалить cron-задачу, отчитаться.
