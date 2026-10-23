#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ext_sources.py — часовая линия внешних источников (по решению автора, 23.10.2026 ~21:1x UTC).

Источники (read-only, гостевой доступ, UA Chrome, sleep 1s):
  1. ТГК  t.me/s/stalzone        — офф. канал (новости разработчиков)
  2. ТГК  t.me/s/spectrum_zone   — фан-сообщество (датамайны/сливы), сравнение
  3. Steam RSS RU  cc=ru&l=russian  app/1818450 — рус. посты разработчиков
  4. Steam RSS EN  cc=us&l=english  app/1818450 — англ. посты (сравнение RU/EN)
  5. VK статьи группы -2677092 (stalzone): якорная статья + discovery ссылок
     /@stalzone-* на страницах статей (prev/next). Стена (посты) без логина
     недоступна — ограничение задокументировано в GIT_AUTOMATION.md.

События: строки '>>> EXT ...' (новые посты ТГК, новые Steam-новости RU/EN,
новые/изменённые VK-статьи). Первый запуск — посев state, без событий.
State:  output/08_monitoring/ext_sources_state.json
Снапы:  output/evidence_post/ext_<src>_<TS>.html/.xml
Exit 0 всегда (сбой источника = warn, не фатально). Никаких POST, никаких токенов.
"""
import json
import os
import re
import sys
import time
import hashlib
import urllib.request
from datetime import datetime, timezone

BASE = 'https://forum.exbo.net'  # не используется здесь, зафиксировано для единообразия
OUTDIR = 'output/evidence_post'
STATEDIR = 'output/08_monitoring'
STATE = os.path.join(STATEDIR, 'ext_sources_state.json')
TS = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

VK_ANCHOR = 'stalzone-start-ots-sobytiya-prazdnestvo-afdfvs4563'
VK_SEED_DISCOVERED = ['stalzone-cep-raspada-nagrazhdenie-la170998']
STEAM_URL = ('https://store.steampowered.com/feeds/news/app/1818450/?cc={cc}&l={lang}')
TG_URLS = {
    'stalzone': 'https://t.me/s/stalzone',
    'spectrum_zone': 'https://t.me/s/spectrum_zone',
}
MAX_SEEN = 40
MAX_VK_FETCH = 8
MAX_TG_EVENT = 6


def log(msg):
    print(msg, flush=True)


def fetch(url, snap_name, timeout=25):
    """GET через urllib с Chrome UA; снап в OUTDIR; возврат bytes/None."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA,
                                                   'Accept-Language': 'ru,en;q=0.8'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
        path = os.path.join(OUTDIR, snap_name)
        with open(path, 'wb') as f:
            f.write(data)
        log(f'OK {snap_name} ({len(data)}B)')
        return data
    except Exception as e:
        log(f'WARN fetch fail {snap_name}: {type(e).__name__}: {e}')
        return None


def strip_tags(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<') \
         .replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    return re.sub(r'\s+', ' ', s).strip()


def load_state():
    if os.path.exists(STATE):
        try:
            with open(STATE, encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {'v': 1, 'tg': {}, 'steam': {}, 'vk': {'articles': {}}}


def save_state(st):
    st['updated'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
    tmp = STATE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(st, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATE)


# ---------------- Telegram ----------------

def tg_parse(html):
    """[(id:int, dt:str, text:str)] из tgme-превью."""
    out = []
    blocks = re.split(r'<div[^>]*class="tgme_widget_message[^"]*"\s+data-post=', html)
    for b in blocks[1:]:
        m_id = re.match(r'"?([a-z0-9_]+)/(\d+)', b)  # блок начинается с '"channel/id' (после 'data-post=')
        m_dt = re.search(r'datetime="([^"]+)"', b)
        m_tx = re.search(r'<div[^>]*class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', b, re.S)
        if not m_id:
            continue
        out.append((int(m_id.group(2)), m_dt.group(1) if m_dt else '',
                    strip_tags(m_tx.group(1))[:180] if m_tx else ''))
    return out


def run_tg(st, name):
    url = TG_URLS[name]
    data = fetch(url, f'ext_tg_{name}_{TS}.html')
    if data is None:
        return 0
    html = data.decode('utf-8', errors='replace')
    msgs = tg_parse(html)
    if not msgs:
        log(f'WARN tg_{name}: 0 сообщений распознано (разметка?)')
        return 0
    cur = st['tg'].get(name, {})
    last = cur.get('last_id', 0)
    top = max(m[0] for m in msgs)
    events = 0
    if last == 0:
        log(f'>> EXT tg_{name}: посев, last_id={top} ({len(msgs)} постов в превью)')
    else:
        fresh = [m for m in msgs if m[0] > last]
        fresh.sort()
        for mid, dt, tx in fresh[:MAX_TG_EVENT]:
            log(f'>>> EXT TG {name} новый пост #{mid} ({dt}): {tx}')
            events += 1
        if len(fresh) > MAX_TG_EVENT:
            log(f'>>> EXT TG {name}: ещё {len(fresh)-MAX_TG_EVENT} постов (см. снап)')
            events += 1
    st['tg'][name] = {'last_id': top, 'last_dt': next((m[1] for m in reversed(msgs) if m[0] == top), '')}
    return events


# ---------------- Steam ----------------

def run_steam(st, lang):
    cc = 'ru' if lang == 'ru' else 'us'
    l = 'russian' if lang == 'ru' else 'english'
    data = fetch(STEAM_URL.format(cc=cc, lang=l), f'ext_steam_{lang}_{TS}.xml')
    if data is None:
        return 0
    xml = data.decode('utf-8', errors='replace')
    items = re.findall(r'<item>(.*?)</item>', xml, re.S)
    parsed = []
    for it in items:
        def cdtag(p):
            m = re.search(p, it, re.S)
            if not m:
                return ''
            v = m.group(1).strip()
            v = re.sub(r'^<!\[CDATA\[|\]\]>$', '', v)
            return v.strip()
        title = cdtag(r'<title>(.*?)</title>')
        link = cdtag(r'<link>(.*?)</link>')
        pub = cdtag(r'<pubDate>(.*?)</pubDate>')
        m_id = re.search(r'/news/app/1818450/view/(\d+)', link)
        if m_id:
            parsed.append((m_id.group(1), title, pub))
    if not parsed:
        log(f'WARN steam_{lang}: 0 items (RSS разметка?)')
        return 0
    cur = st['steam'].get(lang, {})
    seen = set(cur.get('seen', []))
    events = 0
    if not seen:
        log(f'>> EXT steam_{lang}: посев, {len(parsed)} items, топ: «{parsed[0][1][:60]}»')
    else:
        for gid, title, pub in parsed:
            if gid not in seen:
                log(f'>>> EXT STEAM {lang.upper()} новость: «{title}» ({pub}) '
                    f'https://store.steampowered.com/news/app/1818450/view/{gid}')
                events += 1
    new_seen = [g for g, _, _ in parsed][:MAX_SEEN]
    st['steam'][lang] = {'seen': new_seen, 'last_ts': parsed[0][2] if parsed else ''}
    return events


# ---------------- VK статьи ----------------

def run_vk(st):
    arts = st['vk'].get('articles', {})
    # якорь всегда; discovery-семена при пустом state
    targets = [VK_ANCHOR]
    if not arts:
        targets += VK_SEED_DISCOVERED
    targets += [s for s in arts if s != VK_ANCHOR]
    targets = targets[:MAX_VK_FETCH]
    events = 0
    discovered = []
    for slug in targets:
        data = fetch(f'https://vk.ru/@{slug}', f'ext_vk_{slug[:48]}_{TS}.html')
        if data is None:
            continue
        html = data.decode('cp1251', errors='replace')
        t = re.search(r'<title>(.*?)\s*\|\s*VK', html, re.S)
        title = strip_tags(t.group(1))[:120] if t else slug
        pub = (re.search(r'"datePublished"\s*:\s*"([^"]+)"', html) or [None, ''])[1]
        mod = (re.search(r'"dateModified"\s*:\s*"([^"]+)"', html) or [None, ''])[1]
        ogd = (re.search(r'property="og:description"\s+content="([^"]*)"', html) or [None, ''])[1]
        fp = hashlib.sha256((mod + '|' + ogd).encode('utf-8', 'ignore')).hexdigest()[:12]
        # discovery соседних статей
        for lnk in sorted(set(re.findall(r'href="(/@(stalzone|stalzone_news|exbo)[a-z0-9_-]{8,140})"', html))):
            slug2 = lnk[0][2:]
            if slug2 not in arts and slug2 not in targets:
                discovered.append(slug2)
        old = arts.get(slug)
        if old is None:
            # первая встреча: событие только если статья свежая (<48ч); старые — backfill без события
            fresh = False
            try:
                if pub:
                    pdt = datetime.fromisoformat(pub)
                    fresh = (datetime.now(timezone.utc) - pdt).total_seconds() < 48 * 3600
            except Exception:
                fresh = False
            if fresh:
                log(f'>>> EXT VK НОВАЯ статья: «{title}» (pub {pub}, mod {mod}) https://vk.ru/@{slug}')
                events += 1
            else:
                log(f'>> EXT vk: посев (backfill) «{title}» (pub {pub}, mod {mod}, fp {fp})')
        elif old.get('fp') and (old.get('fp') != fp or old.get('modified') != mod):
            log(f'>>> EXT VK статья ИЗМЕНЕНА: «{title}» '
                f'(mod {old.get("modified")} → {mod}, fp {old.get("fp")} → {fp}) '
                f'https://vk.ru/@{slug}')
            events += 1
        arts[slug] = {'title': title, 'published': pub, 'modified': mod, 'fp': fp}
        time.sleep(1)
    # discovery: в state СИЛО (событие решит следующий раунд по дате публикации:
    # свежая <48ч → '>>> НОВАЯ', старая → backfill-посев без события)
    for slug2 in discovered[:6]:
        if slug2 not in arts:
            arts[slug2] = {'title': '', 'published': '', 'modified': '', 'fp': '', 'discovered': TS}
            log(f'.. vk discovery: @{slug2} (в очередь на след. раунд)')
    if len(arts) > 24:  # гигиена: держим последние 24
        keys = [k for k in arts if k != VK_ANCHOR]
        for k in keys[:-23]:
            del arts[k]
        arts[VK_ANCHOR] = arts.get(VK_ANCHOR, {'title': '', 'published': '', 'modified': '', 'fp': ''})
    st['vk']['articles'] = arts
    return events


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    st = load_state()
    seed = (not st['tg']) and (not st['steam']) and (not st['vk']['articles'])
    total = 0
    total += run_tg(st, 'stalzone')
    time.sleep(1)
    total += run_tg(st, 'spectrum_zone')
    time.sleep(1)
    total += run_steam(st, 'ru')
    time.sleep(1)
    total += run_steam(st, 'en')
    time.sleep(1)
    total += run_vk(st)
    save_state(st)
    log(f'>>> итог EXT: events={total}{" (посев)" if seed else ""}')
    log(f'DONE EXT_SOURCES: events={total}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
