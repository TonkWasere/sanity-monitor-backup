#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sources_hourly.py — ежечасная линия внешних источников (решение автора 23.10 21:1x UTC).

Источники (всё read-only GET, Chrome UA, sleep между запросами):
  TG1 https://t.me/s/stalzone       — офф. ТГК Exbo: новости/анонсы (+просмотры как прокси охвата)
  TG2 https://t.me/s/spectrum_zone  — фан-сообщество Датамайны/Сливы (новости, слив-посты)
  ST  https://store.steampowered.com/news/app/1818450 — новости разработчиков RU+EN
      (список: api.steampowered.com ISteamNews v0002; для новых gid — деталь-страницы
       ?l=russian и ?l=english — снапшоты обоих языков)
  VK  https://vk.ru/@-2677092-start-ots-sobytiya-prazdnestvo-afdfvs4563 — статья-лонгрид
      (контент-контроль: sha256 og:title+og:description — детект правок)
      + https://vk.ru/wall-2677092 — посты стены (best-effort, VK может резать ботам)

Каденс: РАЗ В ЧАС, в составе часового раунда (cron 462533) — решение автора:
«часто проверять нет необходимости (другая архитектура, нежели Фларум), но раз в час
обязательно — на предмет новостей или потенциально ценной информации, а также сравнения».

Скрипт НЕ трогает worklog/ledger/git — только state + journal + снапшоты и печать '>>> ...'.
Пишет в: output/08_monitoring/sources_state.json (атомарно),
         output/08_monitoring/SOURCES_JOURNAL.md (append-only),
         output/evidence_post/sources_*_<TS>.* (снапшоты-доказательства).
Сетевые сбои отдельного источника → '>>> SKIP <src>' и продолжаем остальные.
"""

import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

BASE_DIR = '/home/z/my-project'
EV_DIR = os.path.join(BASE_DIR, 'output', 'evidence_post')
MON_DIR = os.path.join(BASE_DIR, 'output', '08_monitoring')
STATE = os.path.join(MON_DIR, 'sources_state.json')
JOURNAL = os.path.join(MON_DIR, 'SOURCES_JOURNAL.md')

TS = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
UTC_NOW = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
SLEEP = 1.5

TG_CHANNELS = [('stalzone', 'https://t.me/s/stalzone'),
               ('spectrum_zone', 'https://t.me/s/spectrum_zone')]
# NB: ключ = РЕАЛЬНЫЙ хэндл канала (data-post="<handle>/<id>") — иначе регулярка парсера пуста.
STEAM_APP = 1818450
STEAM_API = ('https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/'
             f'?appid={STEAM_APP}&count=25&maxlength=400&format=json')
STEAM_DETAIL = 'https://store.steampowered.com/news/app/{app}/detail/{gid}?l={lang}'
VK_ARTICLE = 'https://vk.ru/@-2677092-start-ots-sobytiya-prazdnestvo-afdfvs4563?subtype=primary'
# Стена: vk.ru отдаёт логин-стену ботам, а vk.com — полный HTML (2.3 МБ, посты в payload);
# статья через vk.com, наоборот, таймаутится — поэтому разные хосты, проверено 23.10 21:2x UTC.
VK_WALL = 'https://vk.com/wall-2677092'
VK_OWNER = '-2677092'

MAX_TG_NEW = 10
MAX_STEAM_NEW = 5
MAX_VK_WALL_NEW = 5
STEAM_SEEN_KEEP = 80
VK_SEEN_KEEP = 200

events = []  # строки '>>> ...' и журнал-строки


def journal(line):
    """append-only журнал: одна строка = одно событие."""
    events.append(line)
    try:
        if not os.path.exists(JOURNAL) or os.path.getsize(JOURNAL) == 0:
            with open(JOURNAL, 'w', encoding='utf-8') as f:
                f.write('# SOURCES_JOURNAL — ежечасная линия внешних источников (54-181)\n')
                f.write('# stalzone / spectrum / steam(RU+EN) / vk(статья+стена); решение автора 23.10 21:1x UTC\n\n')
        with open(JOURNAL, 'a', encoding='utf-8') as f:
            f.write('- ' + line + '\n')
    except OSError as e:
        print(f'>>> journal-write fail: {e}')


def http_get(url, timeout=25):
    req = Request(url, headers={
        'User-Agent': UA,
        'Accept-Language': 'ru,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.5',
    })
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.read()
    except HTTPError as e:
        print(f'>>> net HTTP {e.code}: {url}')
        return None
    except (URLError, TimeoutError, OSError) as e:
        print(f'>>> net FAIL: {url} ({e})')
        return None


def snap(data, name):
    """Снапшот-доказательство в evidence_post. Возвращает путь или None."""
    if data is None:
        return None
    path = os.path.join(EV_DIR, f'{name}_{TS}.{name.rsplit(".", 1)[-1] if "." in name else "bin"}')
    # имя уже с расширением: sources_tg_stalzone.html
    path = os.path.join(EV_DIR, name)
    try:
        with open(path, 'wb') as f:
            f.write(data)
        print(f'OK {os.path.basename(path)} ({len(data)}B)')
        return path
    except OSError as e:
        print(f'>>> snap fail {path}: {e}')
        return None


def smart_decode(raw):
    """HTML-декод с учётом charset: ВК отдаёт windows-1251, остальные UTF-8."""
    head = raw[:16384].lower()
    if b'windows-1251' in head:
        return raw.decode('cp1251', 'replace')
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('cp1251', 'replace')


def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    s = s.replace('&quot;', '"').replace('&#39;', "'").replace('« ', '«').replace(' »', '»')
    return re.sub(r'\s+', ' ', s).strip()


# ---------------------------------------------------------------- TG (t.me/s/)
def parse_tg(html_text, chan):
    msgs = []
    for chunk in html_text.split('<div class="tgme_widget_message_wrap')[1:]:
        m = re.search(r'data-post="' + re.escape(chan) + r'/(\d+)"', chunk)
        if not m:
            continue
        mid = int(m.group(1))
        t = re.search(r'<time[^>]*datetime="([^"]+)"', chunk)
        v = re.search(r'tgme_widget_message_views">([^<]+)<', chunk)
        mt = re.search(r'tgme_widget_message_text[^>]*>(.*?)</div>', chunk, re.S)
        text = strip_tags(mt.group(1))[:160] if mt else ''
        msgs.append({'id': mid, 'time': t.group(1) if t else '',
                     'views': v.group(1) if v else '', 'text': text})
    return msgs


def do_tg(chan, url, state, seed):
    raw = http_get(url)
    if raw is None:
        journal(f'{UTC_NOW} SKIP tg/{chan}: сеть/недоступен')
        print(f'>>> SKIP tg/{chan}: сеть')
        return
    snap(raw, f'sources_tg_{chan}.html')
    html_text = smart_decode(raw)
    msgs = parse_tg(html_text, chan)
    if not msgs:
        journal(f'{UTC_NOW} SKIP tg/{chan}: страница без сообщений (тг заблокировал?)')
        print(f'>>> SKIP tg/{chan}: 0 сообщений')
        return
    ids = [m['id'] for m in msgs]
    last_seen = state.get('tg', {}).get(chan, {}).get('last', None)
    if seed or last_seen is None:
        state.setdefault('tg', {})[chan] = {'last': max(ids)}
        journal(f"{UTC_NOW} SEED tg/{chan}: last={max(ids)} ({len(msgs)} постов на странице)")
        print(f'>>> SEED tg/{chan}: last={max(ids)}')
        return
    fresh = [m for m in msgs if m['id'] > last_seen]
    if ids and min(ids) > last_seen + 1:
        journal(f'{UTC_NOW} WARN tg/{chan}: возможен пропуск (стейт last={last_seen}, '
                f'старейший на странице={min(ids)})')
        print(f'>>> WARN tg/{chan}: possible gap {last_seen} -> {min(ids)}')
    if not fresh:
        print(f'>>> tg/{chan}: без новых (last={last_seen})')
        return
    fresh.sort(key=lambda m: m['id'])
    for m in fresh[:MAX_TG_NEW]:
        journal(f"{UTC_NOW} NEW tg/{chan} #{m['id']} ({m['time']}, views {m['views'] or '?'}): «{m['text']}»")
        print(f">>> TG NEW {chan} #{m['id']} ({m['time']}, views {m['views'] or '?'}): «{m['text']}»")
    if len(fresh) > MAX_TG_NEW:
        print(f">>> tg/{chan}: +{len(fresh) - MAX_TG_NEW} ещё сверх {MAX_TG_NEW}")
        journal(f"{UTC_NOW} tg/{chan}: +{len(fresh) - MAX_TG_NEW} ещё сверх {MAX_TG_NEW}")
    state.setdefault('tg', {})[chan] = {'last': max(ids)}


# ------------------------------------------------------------- Steam (RU+EN)
def do_steam(state, seed):
    raw = http_get(STEAM_API)
    if raw is None:
        journal(f'{UTC_NOW} SKIP steam: api недоступен')
        print('>>> SKIP steam: api')
        return
    snap(raw, 'sources_steam_api.json')
    try:
        j = json.loads(raw.decode('utf-8', 'replace'))
        items = j.get('appnews', {}).get('newsitems', []) or []
    except Exception as e:
        journal(f'{UTC_NOW} SKIP steam: api json сломан ({e})')
        print(f'>>> SKIP steam: bad json ({e})')
        return
    seen = list(state.get('steam', {}).get('seen', []))
    fresh = [it for it in items if str(it.get('gid')) not in seen]
    if seed or not seen:
        state['steam'] = {'seen': [str(it.get('gid')) for it in items][:STEAM_SEEN_KEEP]}
        journal(f"{UTC_NOW} SEED steam: {len(items)} постов в ленте (последний gid="
                f"{items[0].get('gid') if items else '-'} «{strip_tags(items[0].get('title', ''))[:60]}» )"
                if items else f'{UTC_NOW} SEED steam: лента пуста')
        print(f'>>> SEED steam: {len(items)} постов в ленте')
        return
    if not fresh:
        print(f'>>> steam: без новых ({len(items)} в ленте)')
        # лента может подсвечивать правки — не отслеживаем правки Steam (ре-посты редки)
        return
    fresh.sort(key=lambda it: int(it.get('date', 0)))
    for it in fresh[:MAX_STEAM_NEW]:
        gid = str(it.get('gid'))
        title = strip_tags(it.get('title', ''))[:120]
        d = datetime.fromtimestamp(int(it.get('date', 0)), tz=timezone.utc).strftime('%Y-%m-%d %H:%M')
        feed = it.get('feedlabel', it.get('feedname', ''))
        journal(f"{UTC_NOW} NEW steam gid={gid} ({d}, {feed}): «{title}»")
        print(f'>>> STEAM NEW gid={gid} ({d}, {feed}): «{title}»')
        for lang in ('russian', 'english'):
            time.sleep(SLEEP)
            dr = http_get(STEAM_DETAIL.format(app=STEAM_APP, gid=gid, lang=lang))
            snap(dr, f'sources_steam_{gid}_{ "ru" if lang == "russian" else "en"}.html')
    if len(fresh) > MAX_STEAM_NEW:
        print(f'>>> steam: +{len(fresh) - MAX_STEAM_NEW} ещё сверх {MAX_STEAM_NEW}')
        journal(f'{UTC_NOW} steam: +{len(fresh) - MAX_STEAM_NEW} ещё сверх {MAX_STEAM_NEW}')
    seen = [str(it.get('gid')) for it in items] + [s for s in seen if s not in
             {str(it.get('gid')) for it in items}]
    state['steam'] = {'seen': seen[:STEAM_SEEN_KEEP]}


# ------------------------------------------------------- VK (статья + стена)
def og_meta(html_text, prop):
    m = re.search(r'<meta[^>]+property="og:' + prop + r'"[^>]*content="([^"]*)"',
                  html_text) or \
        re.search(r'<meta[^>]+content="([^"]*)"[^>]*property="og:' + prop + r'"',
                  html_text)
    return strip_tags(m.group(1)) if m else ''


def do_vk_article(state, seed):
    raw = http_get(VK_ARTICLE)
    if raw is None:
        journal(f'{UTC_NOW} SKIP vk/статья: сеть/недоступен')
        print('>>> SKIP vk/статья: сеть')
        return
    snap(raw, 'sources_vk_article.html')
    html_text = smart_decode(raw)
    title = og_meta(html_text, 'title')
    desc = og_meta(html_text, 'description')
    if not title:
        journal(f'{UTC_NOW} SKIP vk/статья: нет og:title (анти-бот стена ВК?)')
        print('>>> SKIP vk/статья: анти-бот (нет og-меты)')
        return
    sha = hashlib.sha256((title + '\x00' + desc).encode('utf-8')).hexdigest()[:16]
    old = state.get('vk_article', {})
    if seed or not old:
        state['vk_article'] = {'sha': sha, 'title': title[:120]}
        journal(f'{UTC_NOW} SEED vk/статья: «{title[:100]}» sha={sha}')
        print(f'>>> SEED vk/статья: «{title[:80]}» sha={sha}')
        return
    if old.get('sha') != sha:
        journal(f'{UTC_NOW} EDIT vk/статья: sha {old.get("sha")} -> {sha}, '
                f'«{title[:100]}»')
        print(f'>>> VK ARTICLE EDIT: «{title[:80]}» sha {old.get("sha")}->{sha}')
    else:
        print(f'>>> vk/статья: без правок (sha={sha[:8]})')
    state['vk_article'] = {'sha': sha, 'title': title[:120]}


def do_vk_wall(state, seed):
    ids = []
    raw = None
    for attempt in (1, 2):
        raw = http_get(VK_WALL)
        if raw is None:
            break
        snap(raw, 'sources_vk_wall.html')
        html_text = smart_decode(raw)
        ids = []
        for m in re.finditer(r'wall' + re.escape(VK_OWNER) + r'_(\d+)', html_text):
            if int(m.group(1)) not in ids:
                ids.append(int(m.group(1)))
        if ids:
            break
        if attempt == 1:
            # VK отдаёт либо полный HTML (2+ МБ, посты в payload), либо JS-оболочку
            # без постов (~150 КБ, анти-бот вариация) — один ретрай, потом SKIP.
            print('>>> vk/стена: оболочка без постов, ретрай через 3с')
            time.sleep(3)
    if raw is None:
        journal(f'{UTC_NOW} SKIP vk/стена: сеть/недоступен')
        print('>>> SKIP vk/стена: сеть')
        return
    if not ids:
        journal(f'{UTC_NOW} SKIP vk/стена: посты не извлечены (логин-стена/анти-бот)')
        print('>>> SKIP vk/стена: 0 постов извлечено')
        return
    seen = list(state.get('vk_wall', {}).get('seen', []))
    if seed or not seen:
        state['vk_wall'] = {'seen': ids[:VK_SEEN_KEEP]}
        journal(f'{UTC_NOW} SEED vk/стена: {min(len(ids), 20)} последних id, top={max(ids)}')
        print(f'>>> SEED vk/стена: top={max(ids)}')
        return
    fresh = [i for i in ids if i not in seen]
    if not fresh:
        print(f'>>> vk/стена: без новых (top={max(ids)})')
    else:
        for i in sorted(fresh, reverse=True)[:MAX_VK_WALL_NEW]:
            journal(f'{UTC_NOW} NEW vk/стена wall{VK_OWNER}_{i}')
            print(f'>>> VK WALL NEW wall{VK_OWNER}_{i}')
    state['vk_wall'] = {'seen': (ids + seen)[:VK_SEEN_KEEP]}


# ------------------------------------------------------------------- main
def main():
    seed = False
    state = {}
    if os.path.exists(STATE):
        try:
            with open(STATE, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except Exception as e:
            print(f'>>> state сломан, пересев: {e}')
            seed = True
    else:
        seed = True
        print('>>> state отсутствует — ПЕРВЫЙ ЗАПУСК: сев базовой линии')

    os.makedirs(EV_DIR, exist_ok=True)
    os.makedirs(MON_DIR, exist_ok=True)

    for chan, url in TG_CHANNELS:
        do_tg(chan, url, state, seed)
        time.sleep(SLEEP)
    do_steam(state, seed)
    time.sleep(SLEEP)
    do_vk_article(state, seed)
    time.sleep(SLEEP)
    do_vk_wall(state, seed)

    state['updated_utc'] = UTC_NOW
    tmp = STATE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATE)

    print(f'>>> итог: events={len([e for e in events if " SEED " not in e and " SKIP " not in e and " WARN " not in e])}'
          f' (журнал строк: {len(events)}), seed={seed}')
    print('DONE SOURCES')


if __name__ == '__main__':
    main()
