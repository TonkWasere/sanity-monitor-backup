# check54_161_tg.py — верификация ТГК по сырому HTML (урок: data-post=)
# stalzone: 3226 последний (15:00) — ждём 3227+ (3-й час тишины); spectrum: 7954 (15:12) — ждём 7955+
import re, html, json

def posts_from(fn):
    raw = open(fn, encoding='utf-8', errors='replace').read()
    out = []
    for m in re.finditer(r'data-post="([^"]+)"(.*?)(?=data-post="|$)', raw, re.S):
        pid, seg = m.group(1), m.group(2)
        tm = re.search(r'datetime="([^"]+)"', seg)
        txt = re.sub(r'<[^>]+>', ' ', seg)
        txt = html.unescape(re.sub(r'\s+', ' ', txt)).strip()
        reactions = re.findall(r'aria-label="([^"]*?): (\d+)"', seg)
        out.append((pid, tm.group(1) if tm else '?', txt[:200], reactions))
    return out

print('=== stalzone page0 (TS 1830) ===')
for pid, tm, txt, rx in posts_from('/home/z/my-project/output/evidence_post/tg_stalzone_page0_20261022_1830.html'):
    print(f'[{pid}] {tm} rx={rx}')
    print(f'   {txt}')

print()
print('=== spectrum_zone page0 (TS 1830) ===')
for pid, tm, txt, rx in posts_from('/home/z/my-project/output/evidence_post/tg_spectrum_page0_20261022_1830.html'):
    print(f'[{pid}] {tm} rx={rx}')
    print(f'   {txt}')
