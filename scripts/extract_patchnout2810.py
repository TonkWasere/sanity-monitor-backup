#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Извлечение текстов Патчноута [28.10.2026] из всех источников →
output/08_monitoring/patchnout_2026-10-28_sources.md
Источники: форум 197149 post#1 (RU, contentHtml), Steam API (EN, BBCode),
ТГК #3251 (короткий), VK-статья (антибот — фиксируется статус)."""
import json, re, html as H, datetime

EV = '/home/z/my-project/output/evidence_post'
OUT = '/home/z/my-project/output/08_monitoring/patchnout_2026-10-28_sources.md'

# ---------- 1. Форум RU post#1 ----------
d = json.load(open(f'{EV}/patchnout2810_src_forum_near1_20261028_0952.json', encoding='utf-8'))
posts = sorted([x for x in d.get('included', []) if x.get('type') == 'posts'],
               key=lambda x: x['attributes']['number'])
p1 = posts[0]['attributes']
ru_html = p1.get('contentHtml', '')

def html2text(h):
    t = h
    t = re.sub(r'<h1[^>]*>', '\n\n# ', t); t = re.sub(r'<h2[^>]*>', '\n\n## ', t)
    t = re.sub(r'<h3[^>]*>', '\n\n### ', t)
    t = re.sub(r'</h\d>', '\n', t)
    t = re.sub(r'<li[^>]*>', '\n- ', t)
    t = re.sub(r'<(p|ul|ol|table|tr|div)[^>]*>', '\n', t)
    t = re.sub(r'<br\s*/?>', '\n', t)
    t = re.sub(r'</(p|ul|ol|table|tr|div)>', '\n', t)
    t = re.sub(r'<td[^>]*>', ' | ', t)
    t = re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', r'\n[IMG: \1]\n', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = H.unescape(t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    t = re.sub(r'[ \t]+', ' ', t)
    return t.strip()

ru_text = html2text(ru_html)
open(f'{EV}/patchnout2810_forum_post1_text_ru.txt', 'w', encoding='utf-8').write(ru_text)

# ---------- 2. Steam EN BBCode ----------
d2 = json.load(open(f'{EV}/patchnout2810_src_steam_api_ru_20261028_0948.json', encoding='utf-8'))
items = {x.get('gid'): x for x in d2['appnews']['newsitems']}
bb = items['1847920302230198']['contents']

def bb2text(b):
    t = b
    t = re.sub(r'\[h1\](.*?)\[/h1\]', lambda m: '\n\n# ' + re.sub(r'\[/?\w+\]', '', m.group(1)) + '\n', t, flags=re.S)
    t = re.sub(r'\[h2\](.*?)\[/h2\]', lambda m: '\n\n## ' + re.sub(r'\[/?\w+\]', '', m.group(1)) + '\n', t, flags=re.S)
    t = re.sub(r'\[h3\](.*?)\[/h3\]', lambda m: '\n\n### ' + re.sub(r'\[/?\w+\]', '', m.group(1)) + '\n', t, flags=re.S)
    t = re.sub(r'\[b\]([^\]]*)\[/b\]', r'**\1**', t)
    t = re.sub(r'\[i\]([^\]]*)\[/i\]', r'_\1_', t)
    t = re.sub(r'\[c\]([^\]]*)\[/c\]', r'`\1`', t)
    t = re.sub(r'\[list\]', '\n', t); t = re.sub(r'\[\*\]([^\[]*)', r'- \1', t)
    t = re.sub(r'\[/list\]', '\n', t)
    t = re.sub(r'\[img src="([^"]*)"\]\[/img\]', r'\n[IMG: \1]\n', t)
    t = re.sub(r'\[/?(p|hr|quote|url[^\]]*|table|tr|td[^\]]*|strong|em)\]', '\n', t)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()

en_text = bb2text(bb)
open(f'{EV}/patchnout2810_steam_body_text_en.txt', 'w', encoding='utf-8').write(en_text)

# ---------- 3. ТГК #3251 ----------
tg_text = """📰 Патчноут [28.10.2026]

Технические работы в самом разгаре! После их завершения в игре вас будут ожидать следующие изменения:

• «Празднество»
• Оформление безопасных зон
• Новые сезонные задания
• Правки экономики
• Витрина достижений
• Интерфейс и управление
• Правки баланса
• Прочее

🔗 Подробности в статье: 
💬 ВКонтакте | 🤙 Форум EXBO

🤍 STALZONE"""

# ---------- 4. Сравнение структуры RU vs EN ----------
ru_secs = re.findall(r'^## (.+)$', ru_text, re.M)
en_secs = re.findall(r'^# (.+)$', en_text, re.M)
# изображения в RU (в т.ч. потенциальный скрин Атам)
ru_imgs = re.findall(r'\[IMG: ([^\]]+)\]', ru_text)
en_imgs = re.findall(r'\[IMG: ([^\]]+)\]', en_text)
atam_ru = len(re.findall(r'Атам|атам', ru_text))
atam_en = len(re.findall(r'Atam|atam', en_text, re.I))
prom_ru = re.findall(r'[A-Z]{2,}[-–][A-Z]+[-–]?\d*', ru_text)

# ---------- 5. Сборка MD ----------
now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
md = f"""# Патчноут [28.10.2026] — тексты всех источников (задача автора, {now})

> Контекст: патчноут опубликован официально 28.10.2026 09:10 UTC (ТГК 09:10:21, Steam 09:10:42,
> VK-статья ~09:10-09:11); форумный тред **197149 «🗒️ Патчноут [28.10.2026]»** создан 07:21:11 (скрытым),
> стал видим 09:10; форум лёг на техработы ~09:12-09:38 (даунтайм 26 мин), техработы 8:30-13:00 МСК
> (расширены до ~12:00 UTC — «Продление техработ» 197159 в 09:09).
> Подозрение автора подтверждается частично: даунтайм совпал с публикацией патчноута (пик нагрузки).

## 0. Источники и тайминги

| Источник | Время (UTC) | Полнота | Статус извлечения |
|---|---|---|---|
| Форум 197149 post#1 | createdAt 07:21:11 (виден с 09:10) | ПОЛНЫЙ (RU, 28 033 симв. HTML) | ✅ извлечён |
| Steam новость (view 719046160957833527) | 09:10:42 | ПОЛНАЯ (EN, 28 818 BBCode) | ✅ извлечена (ISteamNews API gid 1847920302230198) |
| Steam RU | 09:10:42 | только тизер 368 симв. (meta) | ⚠️ AJAX-тело закрыто; RU-версия ≈ форумный текст |
| ТГК stalzone #3251 | 09:10:21 | краткое оглавление + интро | ✅ извлечён (views 12.7K за 24 мин) |
| VK-статья @stalzone-patchnout-28102026-ergsekrnv | ~09:10 | ПОЛНАЯ (RU) | ❌ антибот-челлендж VK (JS); автор читал здесь; текст ≈ форумный RU |
| Бонус: Steam «maintenance completed» пост | ~09:45 | промокод **SZ-FESTIVITY-2026** (до декабря, 1 раз/аккаунт) | ✅ захвачен |

## 1. Форум 197149 post#1 — полный текст (RU, первоисточник)

```text
{ru_text}
```

## 2. Steam — полный текст (EN)

```text
{en_text}
```

## 3. ТГК #3251 — краткая версия (RU)

```text
{tg_text}
```

## 4. Наблюдения к сравнению (для Большого Поста Санити)

- **Статы нового ножа Атам: упоминаний в тексте RU: {atam_ru}, в EN: {atam_en}** — статы нигде не даны текстом,
  только скриншотом меню осмотра (см. [IMG] в начале форума-текста: patc.png 1920×1080).
- Награды за Лиги рейтинга ОТС — текстом/таблицей не даны (проверить раздел League в текстах выше).
- Разделы RU (форум): {ru_secs[:12]}
- Разделы EN (Steam): {en_secs[:12]}
- Изображений в RU: {len(ru_imgs)} (форум-CDN), в EN: {len(en_imgs)} (Steam clan image)
- Промо-коды в RU-тексте: {sorted(set(prom_ru))[:6]}
- Порядок сравнения после подъёма форума: форум RU ↔ Steam EN (перевод-полнота: секции/цифры/таблицы),
  VK-статья (RU) ↔ форум RU (должны совпасть), ТГК ↔ форум (краткая vs полная).
- Числовые параметры (шансы, дроп-рейты, тайминги «Празднества», экономика) — выписать в таблицу для
  русско-английского сверки цифр: расхождения = отдельный пункт Санити.

## 5. Сырьё (evidence_post)

- patchnout2810_src_forum_near1_20261028_0952.json (форум, near=1, посты 1-20)
- patchnout2810_forum_post1_text_ru.txt (RU текст, чистый)
- patchnout2810_src_steam_api_ru_20261028_0948.json (Steam API, 20 новостей)
- patchnout2810_steam_api_body_en.txt / patchnout2810_steam_body_text_en.txt (EN BBCode/текст)
- patchnout2810_steam_api_maintenance_done.txt (промокод SZ-FESTIVITY-2026)
- patchnout2810_src_vkarticle_20261028_0945.html (VK антибот-оболочка — для архива)
- patchnout2810_src_steam_ru_20261028_0945.html / _en_ (страницы новостей)
"""
open(OUT, 'w', encoding='utf-8').write(md)
print('OK MD:', OUT, len(md), 'chars')
print('RU sections:', ru_secs[:12])
print('EN sections:', en_secs[:12])
print('atam RU/EN:', atam_ru, atam_en, '| imgs RU/EN:', len(ru_imgs), len(en_imgs))
print('RU imgs:', ru_imgs[:3])
