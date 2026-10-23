#!/usr/bin/env python3
"""54-175-audit2: сборка таблицы вырезов из cut_texts_audit_20261023.txt.
Сортировка по тредам (по числу вырезов) + дайджест содержания пропавшего.
Выход: output/08_monitoring/CUTS_TABLE_20261023.md
"""
import re
from collections import defaultdict
from pathlib import Path

SRC = Path("output/08_monitoring/cut_texts_audit_20261023.txt")
OUT = Path("output/08_monitoring/CUTS_TABLE_20261023.md")

text = SRC.read_text(encoding="utf-8")

# --- 1. заголовок "по тредам": счётчики ---
hdr = {}
for m in re.finditer(r"^\s+\[(\d+)\]: вырезов (\d+), с текстом (\d+)", text, re.M):
    hdr[int(m.group(1))] = {"cuts": int(m.group(2)), "withtext": int(m.group(3))}

# --- 2. разбор записей ---
entry_re = re.compile(
    r"^--- \[(\d+)\] #(\d+) (.+?) \| (\S+) \| (.+)$", re.M)
entries = []
matches = list(entry_re.finditer(text))
for i, m in enumerate(matches):
    tid, num, author, ts, snapinfo = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4), m.group(5)
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    body = text[start:end].strip("\n")
    lines = [l.strip() for l in body.splitlines()]
    body_clean = " ".join(l for l in lines if l).strip()
    entries.append({"tid": tid, "num": num, "author": author.strip(),
                    "ts": ts, "snap": snapinfo.strip(), "body": body_clean})

by_thread = defaultdict(list)
for e in entries:
    by_thread[e["tid"]].append(e)

# --- 3. сжатие номеров в диапазоны ---
def ranges(nums):
    nums = sorted(set(nums))
    out, s, p = [], None, None
    for n in nums:
        if s is None:
            s = p = n
        elif n == p + 1:
            p = n
        else:
            out.append(f"{s}-{p}" if p > s else f"{s}")
            s = p = n
    if s is not None:
        out.append(f"{s}-{p}" if p > s else f"{s}")
    return out

def short(body, n=170):
    b = re.sub(r"\s+", " ", body).strip()
    return b if len(b) <= n else b[:n].rstrip() + "…"

# --- 4. сборка markdown ---
all_tids = sorted(set(list(hdr.keys()) + list(by_thread.keys())), key=lambda t: (-hdr.get(t, {}).get("cuts", 0), t))
total_cuts = sum(v["cuts"] for v in hdr.values())
total_texts = len(entries)

L = []
L.append("# ТАБЛИЦА ВЫРЕЗОВ — дайджест по тредам (54-175-audit2)")
L.append("")
L.append(f"Источник: `cut_texts_audit_20261023.txt` (258KB). Поймано удалений: **{total_cuts}**, с сохранённым текстом: **{total_texts}**.")
L.append("Сортировка: по числу вырезов (убыв.). Треды текущих LPN-cc гэпов (196887=5, 196834=7, 196894=3, 196874=2, 196873/196898=1) и волна 196411 #63-70 — сверх этой таблицы.")
L.append("")
L.append("## Сводная таблица")
L.append("")
L.append("| Тред | Вырезов | С текстом | #№ пропавшего (диапазоны) | Авторов затронуто |")
L.append("|---|---|---|---|---|")
for t in all_tids:
    es = by_thread.get(t, [])
    c = hdr.get(t, {}).get("cuts", len(es))
    wt = hdr.get(t, {}).get("withtext", len(es))
    nums = [e["num"] for e in es]
    rng = ", ".join(ranges(nums)[:6]) + (" …" if len(ranges(nums)) > 6 else "")
    if not nums:
        rng = "— (тексты вне окна)"
    au = len({e["author"] for e in es})
    L.append(f"| [{t}](https://forum.exbo.net/threads/{t}/) | {c} | {wt} | {rng} | {au} |")
L.append("")

# топ-авторов вырезанного
ac = defaultdict(int)
for e in entries:
    ac[e["author"]] += 1
top_authors = sorted(ac.items(), key=lambda kv: -kv[1])[:12]
L.append("## Топ-авторов вырезанного")
L.append("")
L.append("| Автор | Вырезано постов |")
L.append("|---|---|")
for a, n in top_authors:
    L.append(f"| {a} | {n} |")
L.append("")

stm_cut = sum(n for a, n in ac.items() if a.startswith("stm:"))
L.append(f"- Всего авторов под нож: **{len(ac)}**; из них stm-твинков: **{sum(1 for a in ac if a.startswith('stm:'))}** (постов: {stm_cut}).")
L.append("")

# --- 5. пер-тредовые дайджесты ---
L.append("## Содержание пропавшего — по тредам")
L.append("")
for t in all_tids:
    es = sorted(by_thread.get(t, []), key=lambda e: e["num"])
    if not es:
        continue
    c = hdr.get(t, {}).get("cuts", len(es))
    ts_lo = min(e["ts"] for e in es)
    ts_hi = max(e["ts"] for e in es)
    L.append(f"### [{t}] — {c} вырезов (текстов: {len(es)}, {ts_lo[:10]} → {ts_hi[:10]})")
    L.append("")
    # топ-авторы треда
    tac = defaultdict(int)
    for e in es:
        tac[e["author"]] += 1
    tt = ", ".join(f"{a}×{n}" for a, n in sorted(tac.items(), key=lambda kv: -kv[1])[:5])
    L.append(f"Авторы: {tt}")
    L.append("")
    # сэмплы: короткие информативные строки, без дублей
    seen, picked = set(), 0
    for e in es:
        s = short(e["body"], 200)
        key = s[:60]
        if key in seen or len(s) < 25:
            continue
        seen.add(key)
        L.append(f"- **#{e['num']}** {e['author']} ({e['ts'][:16]}): {s}")
        picked += 1
        if picked >= 10:
            break
    L.append("")

OUT.write_text("\n".join(L), encoding="utf-8")
print(f"OK -> {OUT} ({OUT.stat().st_size} bytes), threads={len(all_tids)}, entries={total_texts}, cuts={total_cuts}")
