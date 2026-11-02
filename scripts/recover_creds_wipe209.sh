#!/bin/bash
# Recovery creds после WIPE-209 (02.11.2026): vault MEGA -> creds + helper + verify.
# ТОКЕН НИКОГДА не печатается. Эталон vault: sha256 7f9edd5d...
set -u
cd /home/z/my-project

# 1) Полный vault-URL из git-истории (инцидент 54-61, ссылка file/r9QxQBCT)
URL=$(git grep -h -o 'mega\.nz/file/[A-Za-z0-9]\{8\}#[A-Za-z0-9_-]\{43\}' \
      $(git log --all --format=%H -S 'r9QxQBCT' -- worklog.md output/08_monitoring/GIT_AUTOMATION.md 2>/dev/null | head -20) \
      2>/dev/null | grep 'r9QxQBCT' | head -1)
if [ -z "$URL" ]; then
  echo "VAULT-URL NOT FOUND in history"
  exit 3
fi
echo "vault URL: found (r9QxQBCT...), ключ не печатается"

# 2) Скачивание и расшифровка vault
rm -f /tmp/pat_vault_54w209.bin
python3 tools/mega_pull.py "$URL" /tmp/pat_vault_54w209.bin || { echo MEGA-PULL-FAIL; exit 4; }

SHA=$(sha256sum /tmp/pat_vault_54w209.bin | cut -c1-8)
echo "vault sha256: $SHA"
if [ "$SHA" != "7f9edd5d" ]; then
  echo "SHA MISMATCH — эталон 7f9edd5d, vault другой/битый. СТОП."
  exit 5
fi
echo "vault MATCH эталон 54-61"

# 3) Извлечение токена: метка «ТОКЕН:» на своей строке, сам токен — следующая
#    подходящая строка (шаблон с <TOKEN> пропускается — урок регламента)
TOKEN=$(awk '/^ТОКЕН:/{f=1; next} f && !/&lt;TOKEN&gt;/ && !/<TOKEN>/ && /^[A-Za-z0-9_-]{30,}/{gsub(/\r/,""); print; exit}' /tmp/pat_vault_54w209.bin | tr -d '[:space:]')
if ! printf '%s' "$TOKEN" | grep -qE '^ghp_[A-Za-z0-9]{30,}$'; then
  echo "TOKEN FORMAT UNEXPECTED — СТОП без записи"
  exit 6
fi
echo "token: формат OK (ghp_..., значение не печатается)"

# 4) Creds с ОБЯЗАТЕЛЬНОЙ схемой https:// (урок recovery 22-й) + helper store
printf 'https://TonkWasere:%s@github.com/\n' "$TOKEN" > "$HOME/.git-credentials"
chmod 600 "$HOME/.git-credentials"
git config --global credential.helper store
echo "creds записаны (600), credential.helper=store"

# 5) Копия vault в проект (gitignored, 600) — как в прошлых recovery
cp /tmp/pat_vault_54w209.bin PAT_VAULT_LOCAL.md
chmod 600 PAT_VAULT_LOCAL.md
git check-ignore PAT_VAULT_LOCAL.md >/dev/null && echo "vault-копия: gitignored OK" || { echo "ВАЖНО: PAT_VAULT_LOCAL.md НЕ gitignored — убрать файл из worktree!"; rm -f PAT_VAULT_LOCAL.md; }

# 6) Верификация ls-remote (обе репы)
if git ls-remote origin sanity-monitor >/dev/null 2>&1; then echo "ls-remote origin: OK"; else echo "ls-remote origin: FAIL"; fi
if git ls-remote backup sanity-monitor >/dev/null 2>&1; then echo "ls-remote backup: OK"; else echo "ls-remote backup: FAIL"; fi

# 7) Утилизация временных файлов с токеном
rm -f /tmp/pat_vault_54w209.bin /tmp/vault_url_54w209
echo "RECOVERY-CREDS DONE"
