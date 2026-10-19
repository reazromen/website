from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
exclude = {"cms", "content", "dist", "pagefind", "node_modules", "__pycache__"}
for p in ROOT.iterdir():
    if p.name.startswith(".") or p.name in exclude:
        continue
    if p.is_dir():
        shutil.copytree(p, OUT / p.name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    elif p.suffix in {".html", ".xml", ".json", ".svg", ".ico", ".png", ".jpg", ".webp", ".txt"} or p.name in {"_headers", "_redirects"}:
        shutil.copy2(p, OUT / p.name)

# Include the public article editor in the same packaging step used by the
# existing production workflow. Keeping this here avoids changing workflow YAML.
editor_source = ROOT / "assets" / "article-versioning-preview.js"
editor_target = OUT / "assets" / "article-versioning-preview.js"
if not editor_source.is_file():
    raise SystemExit(f"Public article editor asset is missing: {editor_source}")
editor_target.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(editor_source, editor_target)

injection = '\n<script src="/assets/article-versioning-preview.js" defer></script>\n'
injected = 0
markers = ('<article class="article"', 'class="article-meta"', 'class="lede"', 'class="prose"')
for page in OUT.rglob("*.html"):
    html = page.read_text(encoding="utf-8", errors="ignore")
    if all(marker in html for marker in markers) and "/assets/article-versioning-preview.js" not in html and "</body>" in html:
        page.write_text(html.replace("</body>", injection + "</body>", 1), encoding="utf-8")
        injected += 1
if injected < 1:
    raise SystemExit("No article pages received the public version editor")
print(f"Public article editor injected into {injected} article pages.")

(OUT / ".nojekyll").touch()
print("Public artifact assembled without CMS source or drafts.")
