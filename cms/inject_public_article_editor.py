"""Inject the public article editor into rendered article pages before deployment."""
from pathlib import Path
import re

DIST = Path("dist")
SCRIPT = '<script src="/assets/article-versioning-preview.js?v=20261020-1" defer></script>'
OLD_SCRIPT = '<script src="/assets/article-versioning-preview.js" defer></script>'
INJECTION = f"\n{SCRIPT}\n"

count = 0
for path in DIST.rglob("*.html"):
    html = path.read_text(encoding="utf-8", errors="ignore")
    markers = ('<article class="article"', 'class="article-meta"', 'class="lede"', 'class="prose"')
    if not all(marker in html for marker in markers) or "</body>" not in html:
        continue
    if OLD_SCRIPT in html:
        updated = html.replace(OLD_SCRIPT, SCRIPT)
    elif SCRIPT in html:
        updated = html
    elif "/assets/article-versioning-preview.js" not in html:
        updated = html.replace("</body>", INJECTION + "</body>", 1)
    else:
        updated = re.sub(r'<script src="/assets/article-versioning-preview\.js(?:\?[^\"]*)?" defer></script>', SCRIPT, html)
    if updated != html:
        path.write_text(updated, encoding="utf-8")
        count += 1
if count < 1:
    raise SystemExit("No article pages received an editor cache-bust update")
print(f"Updated public version editor reference on {count} article pages")
