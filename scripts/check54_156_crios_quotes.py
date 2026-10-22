import json, re

FN = '/home/z/my-project/output/evidence_post/discussion_159759_near999999_20261022_1330.json'
d = json.load(open(FN, encoding='utf-8'))

ums = {}
for u in d.get('included', []):
    if isinstance(u, dict) and u.get('type') == 'users':
        ums[u['id']] = u['attributes'].get('username', '?')

posts = []
for p in d.get('included', []):
    if isinstance(p, dict) and p.get('type') == 'posts':
        posts.append(p)
for p in d.get('data', []):
    if isinstance(p, dict) and p.get('type') == 'posts':
        posts.append(p)

# number map: number -> post
bynum = {}
for p in posts:
    n = p['attributes'].get('number')
    if n is not None:
        bynum[n] = p

print('=== tail posts 14595..14602: author / replyTo / quote-analysis ===')
for n in sorted(k for k in bynum if isinstance(k, int) and 14595 <= k <= 14602):
    p = bynum[n]
    a = p['attributes']
    pr = p.get('relationships', {})
    author = '?'
    ud = pr.get('user', {}).get('data')
    if ud:
        author = ums.get(ud['id'], f"user{ud['id']}")
    rt = pr.get('replyTo', {}).get('data')
    html = a.get('content_html') or ''
    # quote analysis
    bqs = re.findall(r'<blockquote[^>]*>', html)
    # flarum "Backwards" reply link renders via replyTo rel, not in html; but look for any 'DiscussionPost-link' or 'in reply to'
    backlink = 'PostReply-link' in html or 'in reply to' in html.lower() or ' в ответ ' in html.lower()
    bq_texts = re.findall(r'<blockquote[^>]*>(.*?)</blockquote>', html, re.S)
    texts = []
    for t in bq_texts:
        t2 = re.sub(r'<[^>]+>', '', t)
        t2 = re.sub(r'\s+', ' ', t2).strip()
        texts.append(t2[:120])
    print(f"#{n} [{a.get('createdAt','')}] {author} | replyTo={'YES->'+str(rt.get('id')) if rt else 'no'} | blockquotes={len(bqs)} backlink_html={backlink}")
    for t in texts:
        print(f"    QUOTE: {t}")
    # own text (outside quotes)
    own = re.sub(r'<blockquote.*?</blockquote>', '', html, flags=re.S)
    own = re.sub(r'<[^>]+>', ' ', own)
    own = re.sub(r'\s+', ' ', own).strip()
    if own:
        print(f"    OWN:   {own[:200]}")

print()
print('=== how many posts in WHOLE fetched slice use replyTo rel vs blockquotes (format baseline) ===')
n_replyto = n_bq = n_both = n_neither = 0
for p in posts:
    pr = p.get('relationships', {})
    has_rt = bool(pr.get('replyTo', {}).get('data'))
    html = p['attributes'].get('content_html') or ''
    has_bq = '<blockquote' in html
    if has_rt and has_bq: n_both += 1
    elif has_rt: n_replyto += 1
    elif has_bq: n_bq += 1
    else: n_neither += 1
print(f'posts={len(posts)} replyTo_only={n_replyto} bq_only={n_bq} both={n_both} neither={n_neither}')
