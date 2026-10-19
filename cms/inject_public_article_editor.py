"""Inject the public article editor into rendered article pages before deployment."""
from pathlib import Path

DIST = Path("dist")
INJECTION = '\n<script src="/assets/article-versioning-preview.js" defer></script>\n'

count = 0
for path in DIST.rglob("*.html"):
    html = path.read_text(encoding="utf-8", errors="ignore")
    markers = ('<article class="article"', 'class="article-meta"', 'class="lede"', 'class="prose"')
    if all(marker in html for marker in markers) and "/assets/article-versioning-preview.js" not in html and "</body>" in html:
        path.write_text(html.replace("</body>", INJECTION + "</body>", 1), encoding="utf-8")
        count += 1
if count < 1:
    raise SystemExit("No article pages received the public version editor")
print(f"Injected public version editor into {count} article pages")

[executed on device: hserver (e3ce91f8-8d4c-413e-b14d-04ad4fe8d7e3)]