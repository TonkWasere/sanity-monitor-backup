#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Дополнение patchnout_2026-10-28_sources.md: подтверждённые наблюдения (Атам-скрин,
0 таблиц) + числовая сверка RU↔EN (предложения с цифрами по порядку появления)."""
import re

EV = '/home/z/my-project/output/evidence_post'
MD = '/home/z/my-project/output/08_monitoring/patchnout_2026-10-28_sources.md'

ru = open(f'{EV}/patchnout2810_forum_post1_text_ru.txt', encoding='utf-8').read()
en = open(f'{EV}/patchnout2810_steam_body_text_en.txt', encoding='utf-8').read()

def numsent(t, maxn=40):
    out = []
    for line in t.split('\n'):
        line = line.strip()
        if not line or line.startswith('[IMG') or line.startswith('#') or line.startswith('!['):
            continue
        clean = re.sub(r'`|\*\*|_', '', line)
        if re.search(r'\d', clean) and len(clean) < 260:
            out.append(clean)
    return out[:maxn]

ru_n, en_n = numsent(ru), numsent(en)

add = f"""

## 6. Подтверждённые наблюдения (проверка претензий автора)

- **Статы «Атам» только скриншотом — ПОДТВЕРЖДЕНО:** в RU-тексте нож упомянут один раз, буллетом
  «- Охотничий нож «Атам»;», сразу под ним изображение `1793172624-256303-image.png` (меню осмотра).
  Текстовых статов нет ни в RU, ни в EN (в EN «Atam» не упоминается вовсе — транслитерация
  отсутствует, предмет не описан текстом).
- **Награды за Лиги рейтинга ОТС текстом/таблицей — ПОДТВЕРЖДЕНО ОТСУТСТВИЕ:** маркеров таблиц в
  обоих текстах 0; в разделе прогрессии («Прогрессия состоит из лиг. До лиги «Прозрение»...») награды
  не перечислены — либо картинки, либо ничего.
- **Масштаб «картиночного» патчноута: 49 изображений в RU (форум-CDN), 51 в EN (Steam clan image)** —
  практически каждый предмет/параметр дан скриншотом; текстовая часть несёт только качественные описания.
- Промокод события: `SZ-FESTIVITY-2026` (одноразовый, до декабря) — опубликован отдельным Steam-постом
  («maintenance completed»-лента), в патчноут-текстах отсутствует.
- Структура: RU использует h1 «Празднество» + h2-подразделы (Как играть? / Магазин и снаряжение /
  Награды / Прогрессия / Жетоны / Испытания), EN — плоский список h1 (Festivity / Safe Zones decorations /
  New season quests / Economic adjustments / Achievement Showcase / Interface and controls / Guide /
  Balance adjustments / Other changes and fixes); прямое соответствие подразделов Festivity ↔ «Празднество».

## 7. Числовая сверка RU ↔ EN (предложения с цифрами, по порядку)

**RU (форум):**

{{RU_NUMS}}

**EN (Steam):**

{{EN_NUMS}}

> Проверка автором: сопоставить тайминги (8:30-13:00 МСК, 10:00-00:00 МСК окна), шансы/вероятности,
> валютные курсы и лимиты; расхождение = пункт Большого Поста Санити.
"""

ru_block = '\n'.join(f'- {s}' for s in ru_n)
en_block = '\n'.join(f'- {s}' for s in en_n)
add = add.replace('{{RU_NUMS}}', ru_block).replace('{{EN_NUMS}}', en_block)

with open(MD, 'a', encoding='utf-8') as f:
    f.write(add)
print('APPENDED | RU nums:', len(ru_n), '| EN nums:', len(en_n))
print('RU sample:', ru_n[:4])
print('EN sample:', en_n[:4])
