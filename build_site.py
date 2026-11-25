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
        key = None
        for line in block.splitlines():
            if line[:1] in (" ", "\t") and key and line.strip():
                # continuation of a wrapped value from the line above
                meta[key] = (meta[key] + " " + line.strip()).strip()
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                key = k.strip()
                meta[key] = v.strip()
        for k, v in meta.items():
            if len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
                meta[k] = v[1:-1]
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
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-72K4162M29"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-72K4162M29');
</script>
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
      <a href="../index.html#outcomes">Outcomes</a>
      <a href="../index.html#method">The Method</a>
      <a href="../index.html#proof">Proof</a>
      <a href="../index.html#about">About</a>
      <a href="../index.html#services">Ways in</a>
      <a href="../musings.html">Musings</a>
      <a class="btn btn-primary" href="../contact.html">Book a conversation</a>
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
{related}
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
    <div class="footer-services">
      <span class="h">Services</span>
      <a href="../strategy-consultant">Strategy consulting</a>
      <a href="../brand-strategy">Brand strategy</a>
      <a href="../marketing-strategy">Marketing strategy</a>
      <a href="../strategy-workshops">Strategy workshops</a>
    </div>
    <div>
      <p><strong>Gareth O'Connor</strong><br>Founder &amp; Strategist<br>North Canterbury, New Zealand</p>
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

PERSON = {"@type": "Person", "name": "Gareth O'Connor",
          "url": f"{DOMAIN}/#about", "jobTitle": "Founder & Strategist",
          "sameAs": ["https://nz.linkedin.com/in/gareth-o-connor-3b755a29",
                     "https://www.canterbury.ac.nz/about-uc/contact-us/external-directory/gareth-oconnor"]}

# Which service page each category points readers to
SERVICE_FOR = {
    "Brand Strategy": ("brand-strategy", "Brand strategy"),
    "Marketing Strategy": ("marketing-strategy", "Marketing strategy"),
    "Business Strategy": ("strategy-consultant", "Strategy consulting"),
    "Useful Guides": ("strategy-consultant", "Strategy consulting"),
}

def trim_summary(text, limit=158):
    """First sentence(s) that fit within the limit, else cut at a word boundary."""
    out = ""
    for sent in re.split(r"(?<=[.!?])\s+", text):
        if len(out) + len(sent) + 1 > limit:
            break
        out = (out + " " + sent).strip()
    if not out:
        out = text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return out

try:
    CURATED = {p["url"].rstrip("/").split("/")[-1]: p["excerpt"]
               for p in json.load(open("posts_meta.json")) if p.get("excerpt")}
except Exception as e:
    print("curated excerpts not loaded:", e)
    CURATED = {}

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
    excerpt = fm_excerpt or CURATED.get(slug) or trim_summary(plain)

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
        "author": PERSON,
        "publisher": {"@type": "Organization", "name": "Something Different", "url": f"{DOMAIN}/",
                      "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/logo.png"}},
        "image": ogimage,
        "mainEntityOfPage": url,
        "articleSection": meta["category"],
    }
    jsonld = ('<script type="application/ld+json">\n'
              + json.dumps(jsonld_obj, ensure_ascii=False) + '\n</script>')

    page_args = dict(
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
    posts.append({
        "_slug": slug,
        "_args": page_args,
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

# ---- write article pages, each with related reading + a service link ----
for p in posts:
    same = [q for q in posts if q is not p and q["category"] == p["category"]][:3]
    items = "".join(
        f'<li><a href="{q["_slug"]}.html">{html.escape(q["title"])}</a></li>' for q in same)
    svc_slug, svc_name = SERVICE_FOR.get(p["category"], ("strategy-consultant", "Strategy consulting"))
    related = (
        '    <aside class="post-related">\n'
        f'      <h2>More on {html.escape(p["category"].lower())}</h2>\n'
        f'      <ul>{items}</ul>\n'
        f'      <p>Want help applying this to your business? See how I work on '
        f'<a href="../{svc_slug}">{svc_name.lower()}</a>, or <a href="../musings.html">browse all musings</a>.</p>\n'
        '    </aside>')
    open(f"{OUT}/{p['_slug']}.html", "w", encoding="utf-8").write(
        TPL.format(related=related, **p["_args"]))

public = [{k: v for k, v in p.items() if not k.startswith("_")} for p in posts]
json.dump(public, open("musings.json", "w"), indent=2, ensure_ascii=False)
with open("assets/musings-data.js", "w", encoding="utf-8") as f:
    f.write("window.MUSINGS = ")
    json.dump(public, f, ensure_ascii=False)
    f.write(";\n")

# ---- musings.html: write the archive into the page itself, so crawlers that
# don't run JavaScript still see every article. The script then re-renders it
# for search, filter and sort. ----
def card(p):
    return ('<article class="card">'
            f'<span class="tag {CAT_CLASS.get(p["category"], "")}">{html.escape(p["category"])}</span>'
            f'<h3><a href="{p["url"]}">{html.escape(p["title"])}</a></h3>'
            f'<p class="meta">{html.escape(p["dateDisplay"])} &middot; {p["readMin"]} min read</p>'
            f'<p class="excerpt">{html.escape(p.get("excerpt") or "")}</p>'
            f'<a class="read" href="{p["url"]}">Read musing →</a></article>')
arch = open("musings.html", encoding="utf-8").read()
arch = re.sub(r"<!-- CARDS:START -->.*?<!-- CARDS:END -->",
              lambda m: "<!-- CARDS:START -->\n" + "\n".join(card(p) for p in public) + "\n<!-- CARDS:END -->",
              arch, flags=re.S)
open("musings.html", "w", encoding="utf-8").write(arch)
posts = public

# ---- sitemap.xml ----
sm = [(f"{DOMAIN}/", None, "1.0"),
      (f"{DOMAIN}/strategy-consultant", None, "0.9"),
      (f"{DOMAIN}/brand-strategy", None, "0.9"),
      (f"{DOMAIN}/marketing-strategy", None, "0.9"),
      (f"{DOMAIN}/strategy-workshops", None, "0.9"),
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

# ---- llms.txt: a plain-text guide to the site for AI tools ----
llms = ["# Something Different", "",
        "> Something Different is a brand and growth strategy consultancy run by Gareth O'Connor, "
        "based in North Canterbury, New Zealand. Gareth works directly with leadership teams on strategic "
        "diagnosis, brand strategy, positioning, growth and marketing strategy, communications planning "
        "and executive advisory. He created and teaches Marketing & Strategic Intelligence in the "
        "University of Canterbury's Executive MBA.", "",
        "## Services", "",
        f"- [Strategy consulting]({DOMAIN}/strategy-consultant): independent strategy work for leadership teams facing complex business problems",
        f"- [Brand strategy]({DOMAIN}/brand-strategy): positioning, brand platforms and what a brand should mean",
        f"- [Marketing strategy]({DOMAIN}/marketing-strategy): marketing and communications strategy and planning",
        f"- [Strategy workshops]({DOMAIN}/strategy-workshops): facilitated executive workshops",
        f"- [Contact]({DOMAIN}/contact.html): book a conversation", "",
        "## Musings (articles by Gareth O'Connor)", ""]
for p in posts:
    llms.append(f"- [{p['title']}]({DOMAIN}/{p['url']}): {p.get('excerpt') or ''}".rstrip(": "))
open("llms.txt", "w", encoding="utf-8").write("\n".join(llms) + "\n")

print(f"Built {len(posts)} article pages -> {OUT}/")
print(f"Wrote sitemap.xml ({len(sm)} urls)")
print("Regenerated musings.json + assets/musings-data.js (local links)")
