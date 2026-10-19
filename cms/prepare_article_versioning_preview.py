"""Apply the dev-only article-versioning overlay to a completed public dist/ build.

Run only after build_content.py, package_public.py and Pagefind have succeeded.
This helper does not publish anything and must not be added to the production workflow.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SCRIPT = ROOT / "assets" / "article-versioning-preview.js"
DOC = ROOT / "docs" / "article-version-history.md"


def main():
    if not (DIST / "index.html").is_file() or not (DIST / "build-info.json").is_file():
        raise SystemExit("Expected a completed public dist/ artifact first")
    if not SCRIPT.is_file() or not DOC.is_file():
        raise SystemExit("Missing dev-only script or documentation")
    (DIST / "assets").mkdir(parents=True, exist_ok=True)
    (DIST / "docs").mkdir(parents=True, exist_ok=True)
    (DIST / "assets" / SCRIPT.name).write_bytes(SCRIPT.read_bytes())
    (DIST / "docs" / DOC.name).write_bytes(DOC.read_bytes())
    injection = '\n<script src="/assets/article-versioning-preview.js" defer></script>\n'
    count = 0
    for path in DIST.rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        is_article = all(marker in text for marker in (
            '<article class="article"', 'class="article-meta"',
            'class="lede"', 'class="prose"',
        ))
        if is_article and "/assets/article-versioning-preview.js" not in text:
            if "</body>" not in text:
                continue
            path.write_text(text.replace("</body>", injection + "</body>", 1), encoding="utf-8")
            count += 1
    (DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    print(f"Dev preview overlay prepared: {count} article pages instrumented.")
    print("Robots disallow-all set. Do not publish this artifact to production.")


if __name__ == "__main__":
    main()
