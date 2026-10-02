from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
exclude={'cms','content','dist','pagefind','node_modules','__pycache__'}
for p in ROOT.iterdir():
    if p.name.startswith('.') or p.name in exclude:continue
    if p.is_dir():shutil.copytree(p,OUT/p.name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    elif p.suffix in {'.html','.xml','.json','.svg','.ico','.png','.jpg','.webp','.txt'} or p.name in {'_headers','_redirects'}:shutil.copy2(p,OUT/p.name)
(OUT/'.nojekyll').touch()
print('Public artifact assembled without CMS source or drafts.')
