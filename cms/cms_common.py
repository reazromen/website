from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import hashlib, html, json, re
import yaml, markdown
from bs4 import BeautifulSoup as Soup
from markdownify import markdownify

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
TEMPLATES = ROOT / 'cms' / 'templates'

def digest(s): return hashlib.sha256(s.encode()).hexdigest()
def esc(s): return html.escape(str(s or ''), quote=True)
def soup(s): return Soup(s, 'html.parser')
def html_string(s):
    return str(s).replace('viewbox=', 'viewBox=').replace('preserveaspectratio=', 'preserveAspectRatio=').replace('gradientunits=', 'gradientUnits=')
def text(s): return ' '.join(soup(s).stripped_strings)
def slug(s):
    value = re.sub(r'[^\w-]+', '-', str(s).casefold(), flags=re.U).strip('-')
    return value or ('item-' + digest(str(s))[:10])
def route(href, base='/'):
    u = urlsplit(urljoin('https://reazromen.com'+base, href))
    if u.netloc not in ('reazromen.com', 'www.reazromen.com'): return None
    p = unquote(u.path)
    return p + 'index.html' if p.endswith('/') else p
def target(url):
    if not url.startswith('/') or '?' in url or '#' in url or '\\' in url: raise ValueError('Invalid URL: '+url)
    p = (ROOT / url.lstrip('/')).resolve()
    if not p.is_relative_to(ROOT.resolve()) or p.suffix != '.html': raise ValueError('Unsafe output: '+url)
    return p
def read_doc(p):
    s=p.read_text(); m=re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$',s,re.S)
    if not m: raise ValueError('Missing frontmatter: '+str(p))
    return yaml.safe_load(m[1]) or {}, m[2].strip()
def write_doc(p,meta,body):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text('---\n'+yaml.safe_dump(meta,allow_unicode=True,sort_keys=False)+'---\n\n'+body.strip()+'\n')
def write_yaml(p,data):
    p.parent.mkdir(parents=True,exist_ok=True); p.write_text(yaml.safe_dump(data,allow_unicode=True,sort_keys=False))
def md(raw): return markdownify(raw,heading_style='ATX',bullets='-',wrap=False).strip()
def render_md(body): return markdown.markdown(body,extensions=['extra','sane_lists'],output_format='html5')
def inner(node): return node.decode_contents()
def slot(node,key):
    node.clear(); node.append('{{RR_'+key+'}}')
def template_save(key,s):
    p=TEMPLATES/(key+'.tpl'); p.parent.mkdir(parents=True,exist_ok=True);p.write_text(html_string(s));return str(p.relative_to(ROOT))
def fill(template,values):
    return re.sub(r'\{\{RR_([A-Z0-9_]+)\}\}',lambda m:values[m[1]],template)
def original_or_md(body,source):
    if source and digest(body)==source.get('hash'): return source['html']
    return render_md(body)
