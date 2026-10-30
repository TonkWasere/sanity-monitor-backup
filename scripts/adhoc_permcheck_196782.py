# -*- coding: utf-8 -*-
# Ad-hoc 54-permconfirm-1157: верификация авторских фактов (только чтение)
# 1) 196782 — isLocked/lockedAt + скан постов (просьба ОП закрыть?)
# 2) /api/tags — иконка тега swamps-newbie (Болота) -> этимология прозвища «Жабы»
import json, subprocess, datetime, time, re, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M")
EVID = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "evidence_post")

def get(url, name):
    last = None
    for attempt in range(3):
        try:
            out = subprocess.run(["curl", "-sS", "--max-time", "25", "-A", UA,
                                  "-H", "Accept: application/json", url],
                                 capture_output=True, text=True, timeout=30)
            data = json.loads(out.stdout)  # строгая валидация JSON
            path = os.path.join(EVID, f"{name}_{TS}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=1)
            print(f"[OK] {url} -> {path}")
            return data
        except Exception as e:
            last = e
            print(f"[retry {attempt+1}] {name}: {e}")
            time.sleep(2)
    raise SystemExit(f"FETCH FAILED {name}: {last}")

# --- 1) 196782: атрибуты лока + скан постов ---
d = get("https://forum.exbo.net/api/discussions/196782?include=posts,posts.user",
        "discussion_196782_lockreason")
a = d["data"]["attributes"]
print("=== 196782 attributes ===")
for k in ["title", "isLocked", "lockedAt", "lockPostNumber", "isSticky",
          "commentCount", "createdAt", "lastPostedAt"]:
    print(f"  {k}: {a.get(k)}")

posts = [x for x in d.get("included", []) if x["type"] == "posts"]
users = {x["id"]: x["attributes"].get("username", "?")
         for x in d.get("included", []) if x["type"] == "users"}
print(f"=== posts ({len(posts)}) ===")
for p in sorted(posts, key=lambda x: x["attributes"].get("number", 0)):
    pa = p["attributes"]
    uid = (p.get("relationships", {}).get("user", {}) or {}).get("data", {}).get("id")
    txt = pa.get("content") or ""
    if isinstance(txt, dict):
        txt = json.dumps(txt, ensure_ascii=False)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()[:220]
    print(f"#{pa.get('number')} [{pa.get('createdAt')}] {users.get(uid, '?')} "
          f"(edited={pa.get('editedAt')}) :: {txt}")

# --- 2) теги: иконка swamps-newbie (Болота) и соседи по секциям ---
time.sleep(1)
t = get("https://forum.exbo.net/api/tags", "tags_full")
print("=== tags: id | name | slug | icon | color | isRestricted | canStartDiscussion ===")
for tag in t.get("data", []):
    ta = tag["attributes"]
    print(f"  {tag['id']:>4} | {ta.get('name','')!r} | {ta.get('slug')!r} | "
          f"icon={ta.get('icon')!r} | color={ta.get('color')!r} | "
          f"restricted={ta.get('isRestricted')} | canStart={ta.get('canStartDiscussion','-')}")
