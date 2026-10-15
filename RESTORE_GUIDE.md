# RESTORE GUIDE — восстановление ВМ из sanity_workspace_full_*.tar

**Назначение:** полный слепок рабочего состояния воркспейса `/home/z/my-project` на момент 02.10.2026 ~18:00 UTC (21:00 МСК). Снимок содержит ВСЁ рабочее: исходники проекта, `output/` (доказательная база кампании + оба ZIP-архива), `worklog.md`, `db/`, `.env`, `.git`.

## Что внутри

- `my-project/` — весь проект, КРОМЕ регенерируемых папок `node_modules/` и `.next/` (сознательно исключены: они пересоздаются за минуты и раздули бы архив с ~150 МБ до 1.4+ ГБ)
- `my-project/backup_home_root_20261002/` — копия мелких файлов с уровня `/home/z/` (`pyproject.toml`, `uv.lock`, `TODO`, `.gitconfig`) — при восстановлении положить обратно на `/home/z/`, если чистая ВМ

## Где лежит архив на живой ВМ

**`/home/z/my-project/output/sanity_workspace_full_20261002_1951.tar`** (пересобран 02.10 19:51 UTC после появления v2-документации; SHA256 `1c2d106f2a0233981698e9b75456b65b3281acafe7ddfbbfacfbb9f12d528fb5`).

**Важно:** архив не содержит сам себя — слепок создавался, когда TAR лежал вне `my-project`, поэтому внутри собственного архива его нет. Это нормально. При ПЕРЕСБОРКЕ TAR в будущем обязательно исключать уже лежащие в `output/` архивы:

```bash
tar -cf /tmp/new_snapshot.tar --exclude='my-project/node_modules' --exclude='my-project/.next' --exclude='my-project/output/*.tar' -C /home/z my-project
```

## Восстановление

```bash
# 1. Распаковать на /home/z (структура внутри — my-project/...)
tar -xf sanity_workspace_full_20261002_1951.tar -C /home/z

# 2. Вернуть home-root файлы (если ВМ новая)
cp /home/z/my-project/backup_home_root_20261002/{pyproject.toml,uv.lock,TODO,.gitconfig} /home/z/

# 3. Зависимости и БД
cd /home/z/my-project
bun install          # восстановит node_modules из bun.lock
bun run db:push      # prisma schema → SQLite (db/ уже в архиве, команда идемпотентна)

# 4. Запуск
bun run dev          # dev-сервер на :3000, лог → /home/z/my-project/dev.log
```

## Python-окружение (для mega.py и парсеров)

```bash
cd /home/z
uv sync               # если есть uv; либо вручную:
python3 -m pip install --break-system-packages mega.py "tenacity==8.1.0"
# ВАЖНО: tenacity строго 8.1.0 — новее ломает mega.py (async-несовместимость)
```

## Целостность архива

- Листинг: `tar -tf sanity_workspace_full_*.tar | wc -l`
- Сверка: SHA256 записан в `worklog.md` (Task 14-g) и выведен при создании
- Внутри `output/` лежат два ZIP с собственными `MANIFEST.sha256` — каждый проверяется независимо:
  - `SanitySources_PatchNote3009_v1.zip` (исходники патчноута 30.09, 146 файлов)
  - `SanityModeration_195660_20261002_v1.zip` (документация модерационного события #387/#415)

## Известные ограничения снимка

- `node_modules/` и `.next/` не в архиве (см. выше)
- Dev-сервер на момент снимка работал: `dev.log` и SQLite могут содержать последние секунды активности — не критично
- Дискорд-ссылки на скрины постов A/B имеют срок годности, но сами PNG лежат в `output/evidence_post/` и в `SanityModeration_195660_20261002_v1.zip` — им срок не страшен

## Локальные секреты рядом (НЕ в git)

- `PAT_VAULT_LOCAL.md` (этот же каталог, gitignored, chmod 600) — классический PAT аккаунта
  TonkWasere для push ветки sanity-monitor (origin + backup). В git НИКОГДА не коммитить:
  инцидент 15.10.2026 — GitHub авто-отозвал токен, найденный секрет-сканером в содержимом
  gist'а (даже base64-обфускация не спасла). При распаковке tar-слепка файл возвращается
  вместе с my-project/; при утере — автор генерирует новый токен
  (GitHub → Settings → Developer settings → Tokens, scope repo+gist) и его кладут
  в `~/.git-credentials` + обновляют PAT_VAULT_LOCAL.md.
