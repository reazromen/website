#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

try:
    import markdown
except ImportError:
    print("Missing Python package: markdown", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
POSTS = ROOT / "posts"
GEN_MARKER = "<!-- RR-CMS-GENERATED:v1 -->"

@dataclass
class Entry:
    section: str
    slug: str
    meta: dict
    body_md: str

    @property
    def title(self):
        return str(self.meta.get("title", "")).strip()

    @property
    def excerpt(self):
        return str(self.meta.get("excerpt", "")).strip()

    @property
    def date(self):
        return str(self.meta.get("date", "")).split("T", 1)[0]

    @property
    def read_time(self):
        try:
            return int(self.meta.get("read_time", 6))
        except Exception:
            return 6

    @property
    def tags(self):
        value = self.meta.get("tags") or []
        if isinstance(value, str):
            return [x.strip() for x in value.split(",") if x.strip()]
        return [str(x).strip() for x in value if str(x).strip()]

    @property
    def draft(self):
        return bool(self.meta.get("draft", False))


def load_entry(path: Path, section: str) -> Entry:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not match:
        raise ValueError(f"{path}: expected YAML front matter")
    meta = yaml.safe_load(match.group(1)) or {}
    if not isinstance(meta, dict):
        raise ValueError(f"{path}: front matter must be a mapping")
    entry = Entry(section=section, slug=path.stem, meta=meta, body_md=match.group(2).strip())
    for required in ("title", "date", "excerpt"):
        if not str(meta.get(required, "")).strip():
            raise ValueError(f"{path}: missing {required}")
    return entry


def load_entries(section: str) -> list[Entry]:
    folder = CONTENT / section
    rows = []
    for path in sorted(folder.glob("*.md")):
        rows.append(load_entry(path, section))
    return sorted(rows, key=lambda x: (x.date, x.slug), reverse=True)


def esc(value) -> str:
    return html.escape(str(value or ""), quote=True)


def nav(current: str) -> str:
    items = [
        ("Work", "/portfolio.html", "work"),
        ("Perspectives", "/perspectives.html", "perspectives"),
        ("Music", "/music.html", "music"),
        ("বাংলা", "/bangla.html", "bangla"),
        ("About", "/about.html", "about"),
        ("Stack", "/systems.html", "stack"),
    ]
    links = []
    for label, href, key in items:
        current_attr = ' aria-current="page"' if current == key else ""
        lang = ' lang="bn"' if key == "bangla" else ""
        links.append(f'<a href="{href}"{lang}{current_attr}>{label}</a>')
    return "".join(links)


def render_post(entry: Entry) -> str:
    title = esc(entry.title)
    excerpt = esc(entry.excerpt)
    body = markdown.markdown(entry.body_md, extensions=["extra", "sane_lists"], output_format="html5")

    if entry.section == "music":
        artist = str(entry.meta.get("artist", "")).strip()
        album = str(entry.meta.get("album", "")).strip()
        kind = str(entry.meta.get("kind", "song")).strip()
        kind_label = {"song": "LISTENING NOTE", "album": "ALBUM NOTE", "performance": "PERFORMANCE NOTE"}.get(kind, "LISTENING NOTE")
        bits = [kind_label, artist, album]
        eyebrow = " · ".join(esc(x.upper()) for x in bits if x)
        crumb = f'<a href="/music.html">Music</a> / {esc(artist or "Listening note")}'
        page_type = "Music"
        page_format = kind_label.title()
        extra_css = '<link rel="stylesheet" href="/assets/music-v1.css">'
    elif entry.section == "bangla":
        topic = str(entry.meta.get("topic", "")).strip()
        eyebrow = "বাংলা" + (f" · {esc(topic)}" if topic else "")
        crumb = '<a href="/bangla.html" lang="bn">বাংলা</a>'
        page_type = "Bangla"
        page_format = "Article"
        extra_css = ""
    else:
        topic = str(entry.meta.get("topic", "")).strip()
        eyebrow = "PERSPECTIVE" + (f" · {esc(topic.upper())}" if topic else "")
        crumb = '<a href="/perspectives.html">Perspectives</a>' + (f" / {esc(topic)}" if topic else "")
        page_type = "Perspective"
        page_format = "Article"
        extra_css = ""

    tag_html = "".join(f"<span>{esc(t)}</span>" for t in entry.tags)
    lang = "bn" if entry.section == "bangla" else "en"

    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Reaz Romen</title>
<meta name="description" content="{excerpt}">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/sitewide-v2.css">
<link rel="stylesheet" href="/assets/phase1.css">
<link rel="stylesheet" href="/assets/phase2.css">
<link rel="stylesheet" href="/assets/responsive-v3.css">
{extra_css}
<meta data-pagefind-filter="type[content]" content="{esc(page_type)}">
<meta data-pagefind-filter="format[content]" content="{esc(page_format)}">
<meta data-pagefind-meta="title[content]" content="{title}">
</head>
<body class="rr-themed">
{GEN_MARKER}
<a class="skip-link" href="#rr-main">Skip to content</a>
<header class="site-header rr-global-header"><div class="site-header-inner"><a class="brand" href="/" aria-label="Reaz Romen home">RR</a><nav class="nav" aria-label="Main navigation"><div class="nav-scroll">{nav(entry.section)}</div><div class="nav-actions"><a class="icon-link github-action" href="https://github.com/reazromen" target="_blank" rel="noopener" aria-label="GitHub">GH</a><button class="theme-toggle" type="button" onclick="toggleTheme()" aria-label="Toggle color scheme">◐</button></div></nav></div></header>
<main id="rr-main" class="shell site-main">
<article class="article" data-pagefind-body>
<nav class="breadcrumbs" aria-label="Breadcrumb">{crumb}</nav>
<p class="eyebrow">{eyebrow}</p>
<h1>{title}</h1>
<p class="lede">{excerpt}</p>
<div class="article-meta"><address class="author-line">By <a href="/author/reaz-romen.html">Reaz Romen</a><span class="verified">✓ Site verified</span></address><span>Published {esc(entry.date)}</span><span>{entry.read_time} min read</span></div>
<div class="tags">{tag_html}</div>
<div class="prose">
{body}
</div>
</article>
</main>
<footer class="shell site-footer">
<div><span class="status-dot"></span><strong>Reaz Romen — independent systems engineer.</strong></div>
<p>Firmware, real-time communications, infrastructure and field notes. First-party HTML/CSS, no analytics, no third-party scripts.</p>
<nav aria-label="Footer"><a href="/topics.html">Topics</a><a href="/systems.html">Systems</a><a href="/archive.html">Archive</a><a href="/author/reaz-romen.html">Author record</a></nav>
</footer>
<script src="/assets/site.js"></script><script src="/assets/sitewide.js"></script><script src="/assets/phase1.js"></script><script src="/assets/phase2.js"></script><script src="/assets/responsive-v3.js"></script>
</body>
</html>
"""


def replace_marked(text: str, start: str, end: str, payload: str) -> str:
    block = f"{start}\n{payload.rstrip()}\n{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    raise ValueError(f"Markers not found: {start}")


def ensure_music_markers(text: str) -> str:
    start = "<!-- CMS-MUSIC-START -->"
    end = "<!-- CMS-MUSIC-END -->"
    if start in text:
        return text
    anchor = '<section class="section-block music-notes-section" aria-label="Music writing">'
    pos = text.find(anchor)
    if pos < 0:
        raise ValueError("music.html: Music writing section not found")
    open_div = text.find('<div class="music-bridge-list">', pos)
    close_div = text.find("</div>", open_div)
    if open_div < 0 or close_div < 0:
        raise ValueError("music.html: song list not found")
    return text[:close_div] + f"\n{start}\n{end}\n" + text[close_div:]


def ensure_perspective_markers(text: str) -> str:
    start = "<!-- CMS-PERSPECTIVES-START -->"
    end = "<!-- CMS-PERSPECTIVES-END -->"
    if start in text:
        return text
    latest = text.find("<span>LATEST</span>")
    if latest < 0:
        raise ValueError("perspectives.html: LATEST section not found")
    open_div = text.find('<div class="post-list editorial-list">', latest)
    if open_div < 0:
        raise ValueError("perspectives.html: latest list not found")
    insert = open_div + len('<div class="post-list editorial-list">')
    return text[:insert] + f"\n{start}\n{end}\n" + text[insert:]


def ensure_bangla_markers(text: str) -> str:
    start = "<!-- CMS-BANGLA-START -->"
    end = "<!-- CMS-BANGLA-END -->"
    if start in text:
        return text
    pos = text.rfind("</main>")
    if pos < 0:
        raise ValueError("bangla.html: </main> not found")
    section = f"""
<section class="section-block" aria-label="Published Bangla writing">
  <div class="section-kicker"><span>LATEST</span><span>CMS PUBLISHED</span></div>
  <div class="post-list editorial-list">
{start}
{end}
  </div>
</section>
"""
    return text[:pos] + section + text[pos:]


def music_card(entry: Entry, index: int) -> str:
    artist = str(entry.meta.get("artist", "")).strip()
    album = str(entry.meta.get("album", "")).strip()
    bits = [artist.upper()]
    if album:
        bits.append(album.upper())
    bits.append(f"{entry.read_time} MIN →")
    meta = " · ".join(x for x in bits if x)
    return (
        f'<a class="music-bridge-link" href="/posts/{esc(entry.slug)}.html">\n'
        f'  <span class="index">{index:02d}</span>\n'
        f'  <strong>{esc(entry.title)}</strong>\n'
        f'  <span>{esc(meta)}</span>\n'
        f'</a>'
    )


def perspective_card(entry: Entry, bangla: bool = False) -> str:
    topic = str(entry.meta.get("topic", "")).strip()
    topic_html = esc(topic or ("বাংলা" if bangla else "Perspective"))
    tags = "".join(f"<span>{esc(t)}</span>" for t in entry.tags)
    return f"""<article class="post-card">
  <p class="meta">{topic_html} · {entry.read_time} min read · {esc(entry.date)}</p>
  <h3><a href="/posts/{esc(entry.slug)}.html">{esc(entry.title)}</a></h3>
  <p>{esc(entry.excerpt)}</p>
  <p class="byline-mini">By <a href="/author/reaz-romen.html">Reaz Romen</a> <span class="verified mini">✓ verified</span></p>
  <div class="tags">{tags}</div>
</article>"""


def write_generated_posts(entries: list[Entry]) -> None:
    POSTS.mkdir(parents=True, exist_ok=True)
    desired = set()
    for entry in entries:
        if entry.draft:
            continue
        out = POSTS / f"{entry.slug}.html"
        desired.add(out.resolve())
        if out.exists() and GEN_MARKER not in out.read_text(encoding="utf-8", errors="ignore"):
            raise ValueError(f"Refusing to overwrite hand-authored post: {out.relative_to(ROOT)}")
        out.write_text(render_post(entry), encoding="utf-8")

    for path in POSTS.glob("*.html"):
        try:
            data = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if GEN_MARKER in data and path.resolve() not in desired:
            path.unlink()


def update_indexes(music_entries: list[Entry], perspective_entries: list[Entry], bangla_entries: list[Entry]) -> None:
    music_file = ROOT / "music.html"
    text = ensure_music_markers(music_file.read_text(encoding="utf-8"))
    prefix = text.split("<!-- CMS-MUSIC-START -->", 1)[0]
    existing_count = prefix.count('class="music-bridge-link"')
    published_music = [x for x in music_entries if not x.draft]
    cards = [music_card(e, existing_count + i + 1) for i, e in enumerate(reversed(published_music))]
    text = replace_marked(text, "<!-- CMS-MUSIC-START -->", "<!-- CMS-MUSIC-END -->", "\n".join(cards))
    music_file.write_text(text, encoding="utf-8")

    p_file = ROOT / "perspectives.html"
    text = ensure_perspective_markers(p_file.read_text(encoding="utf-8"))
    cards = [perspective_card(e) for e in perspective_entries if not e.draft]
    text = replace_marked(text, "<!-- CMS-PERSPECTIVES-START -->", "<!-- CMS-PERSPECTIVES-END -->", "\n".join(cards))
    p_file.write_text(text, encoding="utf-8")

    b_file = ROOT / "bangla.html"
    text = ensure_bangla_markers(b_file.read_text(encoding="utf-8"))
    cards = [perspective_card(e, bangla=True) for e in bangla_entries if not e.draft]
    text = replace_marked(text, "<!-- CMS-BANGLA-START -->", "<!-- CMS-BANGLA-END -->", "\n".join(cards))
    b_file.write_text(text, encoding="utf-8")


def main() -> None:
    music_entries = load_entries("music")
    perspective_entries = load_entries("perspectives")
    bangla_entries = load_entries("bangla")
    all_entries = music_entries + perspective_entries + bangla_entries

    slugs = {}
    for entry in all_entries:
        if entry.slug in slugs:
            raise ValueError(f"Duplicate CMS slug {entry.slug}: {slugs[entry.slug]} and {entry.section}")
        slugs[entry.slug] = entry.section

    write_generated_posts(all_entries)
    update_indexes(music_entries, perspective_entries, bangla_entries)
    print(
        "CMS build complete:",
        f"music={sum(not x.draft for x in music_entries)}",
        f"perspectives={sum(not x.draft for x in perspective_entries)}",
        f"bangla={sum(not x.draft for x in bangla_entries)}",
    )


if __name__ == "__main__":
    main()
