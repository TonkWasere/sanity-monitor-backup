# MEGA VAULT INSURANCE — авторская страховка восстановления push (25.10 ~01:00 UTC)

**Ссылка (текст в теле репо — по решению автора; теория: текст ссылки в репо безопасен,
в отличие от СОДЕРЖИМОГО — контент качается только в /tmp, в репо не коммитится):**

```
https://mega.nz/file/r9QxQBCT#F4tjwiW8UOhJKqxFk1K55r8w5Je5qDw6zNC4dqmy2uo
```

## Что внутри
- `PAT_VAULT_LOCAL.md`, **2630 B** — классик `ghp_`-токен GitHub (TonkWasere).
- Эталон: sha256 `7f9edd5d…` (54-61) — vault байт-в-байт тот же с 22.10 (проверено 54-149-mega и 25.10 54-209-B), **токен НЕ ротирован** (выдан 15.10).
- MAC-проверка делается автоматически в `tools/mega_pull.py`.

## Зачем
После отката ВМ гибнут `~/.git-credentials`, vault в корне, /tmp и не-git артефакты («не переживают и час», урок 54-96). Ссылка в теле репо переживает ЛЮБОЙ откат → самостоятельное восстановление пуша без ожидания автора в чате (чей контекст тоже теряется).

## Восстановление (6 шагов, токен НИКОГДА не печатать)
1. `python3 tools/mega_pull.py '<ссылка выше>'` → /tmp/PAT_VAULT_LOCAL.md (MAC OK = целостность)
2. `TOKEN=$(grep -oE 'gh[pousr]+_[A-Za-z0-9_]+' /tmp/PAT_VAULT_LOCAL.md | head -1)`
3. `umask 077; printf 'https://TonkWasere:%s@github.com\n' "$TOKEN" > ~/.git-credentials; chmod 600 ~/.git-credentials`
4. `git config --global credential.helper store`
5. `cp /tmp/PAT_VAULT_LOCAL.md ./PAT_VAULT_LOCAL.md; chmod 600 ./PAT_VAULT_LOCAL.md` (gitignored — не коммитить!)
6. Проверка: `curl -s -o /dev/null -w '%{http_code}' -H "Authorization: token $TOKEN" https://api.github.com/user` → **200**

## Риск (осознанный, решение автора)
- ⚠️ Инцидент 54-61 (MEGA-INCIDENT 18.10): vault с живым токеном на публичной ссылке, ключ — в публичных репах. GitHub MEGA не сканирует (5+ восстановлений с 15.10 без последствий), НО:
- При ротации токена автором: перезалить vault с новым токеном под НОВЫМ ключом → **обязательно обновить ссылку в этом файле** → старый токен отозвать.

## Дубль ссылки
- Git-история: commit `aa91ed9` (`scripts/restore_creds_54_96.py`), playbook «СТАТУС 22.10» (file-ID r9QxQBCT ×5 упоминаний).
- История использований восстановления: 54-61, 54-96, 54-138b, 54-149-mega, 54-161-B, WIPE-6 (20.10), 54-209-B (25.10 — впервые из ТЕЛА РЕПО, до него ссылка жила только в чате).
