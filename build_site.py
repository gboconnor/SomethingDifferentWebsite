#!/usr/bin/env python3
"""Builds article pages for each musing from musings_src/*.md, and regenerates
the musings index data so it links to the local pages.
Run: python3 build_site.py
"""
import os, re, json, glob, html, datetime
import markdown

SRC = "musings_src"
OUT = "musings"
DOMAIN = "https://somethingdifferent.co.nz"
os.makedirs(OUT, exist_ok=True)

CAT_CLASS = {
    "Marketing Strategy": "c-marketing",
    "Business Strategy": "c-business",
    "Brand Strategy": "c-brand",
    "Useful Guides": "c-guides",
}

def parse_front(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    meta, body = {}, text
    if m:
        block, body = m.group(1), m.group(2)
        for line in block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                v = v.strip()
                if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
                    v = v[1:-1]
                meta[k.strip()] = v
    return meta, body.strip()

def drive_embed(m):
    """Turn a Google Drive / Docs anchor into an embedded viewer + open button."""
    url = m.group("href")
    fid = None
    kind = "file"
    dm = re.search(r"/(document|presentation|spreadsheets)/d/([A-Za-z0-9_-]+)", url)
    fm = re.search(r"/file/d/([A-Za-z0-9_-]+)", url)
    im = re.search(r"[?&]id=([A-Za-z0-9_-]+)", url)
    if dm:
        kind, fid = dm.group(1), dm.group(2)
        embed = f"https://docs.google.com/{kind}/d/{fid}/embed"
    elif fm:
        fid = fm.group(1)
        embed = f"https://drive.google.com/file/d/{fid}/preview"
    elif im:
        fid = im.group(1)
        embed = f"https://drive.google.com/file/d/{fid}/preview"
    else:
        return m.group(0)  # leave unchanged
    return (f'<div class="embed"><iframe src="{embed}" allow="autoplay" '
            f'allowfullscreen loading="lazy"></iframe></div>'
            f'<p class="embed-btn"><a class="btn btn-outline" target="_blank" '
            f'rel="noopener" href="{html.escape(url)}">Open in Google Drive ↗</a></p>')

ANCHOR = re.compile(r'<a [^>]*href="(?P<href>[^"]*(?:drive\.google\.com|docs\.google\.com)[^"]*)"[^>]*>.*?</a>', re.S)

TPL = """<!DOCTYPE html>
<html lang="en-NZ">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Something Different</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#004240">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/favicon.png" sizes="64x64">
<link rel="apple-touch-icon" href="/assets/favicon.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Something Different">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{ogimage}">
<meta property="article:published_time" content="{date_iso}">
<meta property="article:section" content="{category}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ogimage}">
{jsonld}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/styles.css">
</head>
<body>

<header class="nav">
  <div class="container">
    <a class="brand" href="../index.html"><img src="../assets/logo.png" alt="Something Different"></a>
    <button class="nav-toggle" aria-label="Menu" onclick="document.getElementById('nav').classList.toggle('open')">&#9776;</button>
    <nav class="nav-links" id="nav">
      <a href="../index.html#what">What I do</a>
      <a href="../index.html#who">Who it's for</a>
      <a href="../musings.html">Musings</a>
      <a href="../contact.html">Contact</a>
      <a class="btn btn-primary" href="../contact.html">Get in touch</a>
    </nav>
  </div>
</header>

<article class="post">
  <div class="post-wrap">
    <a class="back-link" href="../musings.html">&larr; All musings</a>
    <div class="post-header">
      <span class="tag {catclass}">{category}</span>
      <h1>{title}</h1>
      <p class="post-meta">{dateDisplay} &middot; {readMin} min read</p>
    </div>
    {hero}
    <div class="prose">
{body}
    </div>
    <div class="post-author">
      <img src="../assets/gareth.jpg" alt="Gareth O'Connor">
      <div>
        <div class="n">Gareth O'Connor</div>
        <div class="r">Founder &amp; Strategist, Something Different</div>
      </div>
    </div>
  </div>
</article>

<section class="cta-band">
  <div class="container narrow">
    <h2>Ready to find the real problem?</h2>
    <p class="lead">If performance has stalled and you want to fix the cause, not just the symptoms, let's have a short, no-obligation conversation.</p>
    <a class="btn btn-primary" href="../contact.html" style="margin-top:10px;">Get in touch</a>
  </div>
</section>

<footer class="footer">
  <div class="container footer-grid">
    <div>
      <a class="brand" href="../index.html"><img src="../assets/logo.png" alt="Something Different"></a>
      <p style="margin-top:10px;max-width:36ch;">Brand &amp; growth strategy consultancy. Helping leadership teams get to the root and grow.</p>
    </div>
    <div>
      <a class="btn btn-primary" href="../contact.html">Get in touch</a>
    </div>
  </div>
</footer>

</body>
</html>
"""

def fmt_display(iso):
    """2026-08-05 -> 5 Aug 2026"""
    try:
        d = datetime.datetime.strptime(iso, "%Y-%m-%d")
        return f"{d.day} {d.strftime('%b')} {d.year}"
    except Exception:
        return iso

def est_read(text):
    """Estimate reading time in minutes from word count (~200 wpm)."""
    words = len(re.findall(r"\w+", text))
    return max(1, round(words / 200))

md = markdown.Markdown(extensions=["extra", "sane_lists"])

posts = []
fm_excerpt_slugs = set()   # posts that supplied their own excerpt in frontmatter
for path in sorted(glob.glob(f"{SRC}/*.md")):
    slug = os.path.splitext(os.path.basename(path))[0]
    meta, body = parse_front(open(path, encoding="utf-8").read())
    if not meta.get("title"):
        continue
    md.reset()
    body_html = md.convert(body)
    body_html = ANCHOR.sub(drive_embed, body_html)
    hero = ""
    if meta.get("hero"):
        hero = f'<img class="post-hero" src="{html.escape(meta["hero"])}" alt="{html.escape(meta["title"])}">'

    plain = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", body_html)).strip()
    date_iso = meta.get("date", "")
    dateDisplay = (meta.get("dateDisplay") or "").strip() or fmt_display(date_iso)
    read_min = int(meta.get("readMin") or 0) or est_read(plain)
    fm_excerpt = (meta.get("excerpt") or "").strip()
    if fm_excerpt:
        fm_excerpt_slugs.add(slug)
    excerpt = fm_excerpt or plain[:155].strip()

    url = f"{DOMAIN}/musings/{slug}.html"
    if meta.get("hero"):
        h = meta["hero"]
        ogimage = h if h.startswith("http") else DOMAIN + (h if h.startswith("/") else "/" + h)
    else:
        ogimage = f"{DOMAIN}/assets/og-image.png"
    jsonld_obj = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": meta["title"],
        "description": excerpt,
        "datePublished": date_iso,
        "author": {"@type": "Person", "name": "Gareth O'Connor"},
        "publisher": {"@type": "Organization", "name": "Something Different",
                      "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/logo.png"}},
        "image": ogimage,
        "mainEntityOfPage": url,
        "articleSection": meta["category"],
    }
    jsonld = ('<script type="application/ld+json">\n'
              + json.dumps(jsonld_obj, ensure_ascii=False) + '\n</script>')

    page = TPL.format(
        title=html.escape(meta["title"]),
        desc=html.escape(excerpt.replace('"', "'")),
        category=html.escape(meta["category"]),
        catclass=CAT_CLASS.get(meta["category"], ""),
        dateDisplay=html.escape(dateDisplay),
        readMin=read_min,
        hero=hero,
        body=body_html,
        url=url,
        ogimage=html.escape(ogimage),
        date_iso=date_iso,
        jsonld=jsonld,
    )
    open(f"{OUT}/{slug}.html", "w", encoding="utf-8").write(page)
    posts.append({
        "title": meta["title"],
        "category": meta["category"],
        "date": date_iso,
        "dateDisplay": dateDisplay,
        "readMin": read_min,
        "url": f"musings/{slug}.html",
        "excerpt": excerpt,
    })

# For the original 77, prefer the curated excerpts in posts_meta.json — but never
# override a post that provided its own excerpt (e.g. new ones written in the CMS).
try:
    curated = {p["url"].rstrip("/").split("/")[-1]: p["excerpt"]
               for p in json.load(open("posts_meta.json"))}
    for p in posts:
        s = p["url"].split("/")[-1].replace(".html", "")
        if s not in fm_excerpt_slugs and curated.get(s):
            p["excerpt"] = curated[s]
except Exception as e:
    print("excerpt merge skipped:", e)

posts.sort(key=lambda p: p["date"], reverse=True)
json.dump(posts, open("musings.json", "w"), indent=2, ensure_ascii=False)
with open("assets/musings-data.js", "w", encoding="utf-8") as f:
    f.write("window.MUSINGS = ")
    json.dump(posts, f, ensure_ascii=False)
    f.write(";\n")

# ---- sitemap.xml ----
sm = [(f"{DOMAIN}/", None, "1.0"),
      (f"{DOMAIN}/musings.html", None, "0.8"),
      (f"{DOMAIN}/contact.html", None, "0.7")]
for p in posts:
    sm.append((f"{DOMAIN}/{p['url']}", p["date"], "0.6"))
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, lastmod, pr in sm:
    lines.append("  <url>")
    lines.append(f"    <loc>{loc}</loc>")
    if lastmod:
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines.append(f"    <priority>{pr}</priority>")
    lines.append("  </url>")
lines.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(lines) + "\n")

print(f"Built {len(posts)} article pages -> {OUT}/")
print(f"Wrote sitemap.xml ({len(sm)} urls)")
print("Regenerated musings.json + assets/musings-data.js (local links)")
