"""Regression checks for generated canonical, robots, and sitemap policy."""
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
import json

from bs4 import BeautifulSoup
from cms_common import CONTENT, read_doc

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://reazromen.com'
NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
SECTIONS = ('writing', 'perspectives', 'music', 'movies', 'archaeology', 'heritage', 'bangla', 'local-cultures', 'world-cultures')

def has_noindex(document):
    for node in document.select('meta[name="robots"]'):
        directives = {part.strip().lower() for part in (node.get('content') or '').split(',')}
        if 'noindex' in directives:
            return True
    return False

DOCUMENT_CACHE = {}
def document_for(path):
    path = Path(path)
    if path not in DOCUMENT_CACHE:
        DOCUMENT_CACHE[path] = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    return DOCUMENT_CACHE[path]

def local_html_path(url_path):
    if url_path == '/':
        return ROOT / 'index.html'
    relative = url_path.lstrip('/')
    candidate = ROOT / relative
    if url_path.endswith('/') or (candidate.is_dir() and not candidate.suffix):
        candidate = candidate / 'index.html'
    return candidate

sitemap_path = ROOT / 'sitemap.xml'
assert sitemap_path.is_file() and sitemap_path.stat().st_size, 'Missing generated sitemap.xml'
root = ET.parse(sitemap_path).getroot()
urls = [node.text.strip() for node in root.findall('sm:url/sm:loc', NS) if node.text and node.text.strip()]
assert urls, 'Sitemap contains no URLs'
assert len(urls) == len(set(urls)), 'Sitemap contains duplicate URLs'
url_set = set(urls)

for url in urls:
    parts = urlsplit(url)
    assert parts.scheme == 'https' and parts.netloc == 'reazromen.com', f'Noncanonical sitemap origin: {url}'
    assert not parts.query and not parts.fragment, f'Sitemap URL contains query or fragment: {url}'
    path = local_html_path(parts.path)
    assert path.is_file(), f'Sitemap URL has no generated HTML file: {url} -> {path.relative_to(ROOT)}'
    document = document_for(path)
    canonicals = document.select('link[rel="canonical"]')
    assert len(canonicals) == 1, f'Expected exactly one canonical tag for {url}; found {len(canonicals)}'
    assert canonicals[0].get('href') == url, f'Sitemap URL is not its page canonical: {url} -> {canonicals[0].get("href")}'
    assert not has_noindex(document), f'Noindex URL incorrectly included in sitemap: {url}'
    assert document.title and document.title.get_text(strip=True), f'Missing title on sitemap page: {url}'

manifest = set(json.loads((ROOT / 'cms' / 'generated-manifest.json').read_text(encoding='utf-8')))
# Do not advertise duplicate index.html aliases when an equivalent .html page
# is part of this build. A stale file on disk is not an eligible canonical target.
for url in urls:
    path = urlsplit(url).path
    if path.endswith('/index.html'):
        counterpart = path[:-len('/index.html')] + '.html'
        if counterpart in manifest:
            raise AssertionError(f'Sitemap contains an index.html alias with a generated .html counterpart: {url}')
assert BASE + '/' in url_set, 'Canonical homepage is missing from sitemap'

# Every generated canonical alias must point to a destination in the same build.
for generated_path in manifest:
    generated_page = local_html_path(generated_path)
    if not generated_page.is_file():
        raise AssertionError(f'Generated manifest page is missing: {generated_path}')
    generated_document = document_for(generated_page)
    generated_canonicals = generated_document.select('link[rel="canonical"]')
    if len(generated_canonicals) != 1:
        raise AssertionError(f'Expected exactly one canonical tag for generated page: {generated_path}')
    canonical = generated_canonicals[0].get('href') or ''
    if canonical != BASE + generated_path:
        target_path = urlsplit(canonical).path
        if target_path != '/':
            assert target_path in manifest, f'Canonical target is not part of this build: {generated_path} -> {canonical}'

# Utility search pages and the known placeholder post stay accessible but are
# explicitly non-indexable; neither belongs in the XML sitemap.
for policy_path in ('/search.html', '/posts/test.html'):
    policy_page = local_html_path(policy_path)
    assert policy_page.is_file(), f'Expected policy page is missing: {policy_path}'
    policy_document = document_for(policy_page)
    assert has_noindex(policy_document), f'Expected noindex,follow policy: {policy_path}'
    assert BASE + policy_path not in url_set, f'Non-indexable utility/placeholder page appears in sitemap: {policy_path}'

robots_txt = (ROOT / 'robots.txt').read_text(encoding='utf-8')
assert 'Sitemap: https://reazromen.com/sitemap.xml' in robots_txt, 'robots.txt must advertise the production sitemap'
assert 'Allow: /' in robots_txt, 'robots.txt must allow crawling of public content'

# Every intentionally noindex public HTML page must be omitted from the sitemap.
noindex_count = 0
for page in ROOT.rglob('*.html'):
    relative = page.relative_to(ROOT)
    if any(part in {'.git', 'cms', 'content', 'docs', 'static'} for part in relative.parts):
        continue
    document = document_for(page)
    if not has_noindex(document):
        continue
    noindex_count += 1
    page_path = '/' if relative.as_posix() == 'index.html' else '/' + relative.as_posix()
    assert BASE + page_path not in url_set, f'Noindex page appears in sitemap: {page_path}'

# Every generated page that is indexable and self-canonical must be discoverable
# through the sitemap; silently omitting a valid article is a regression too.
for generated_path in manifest:
    generated_page = local_html_path(generated_path)
    if not generated_page.is_file():
        raise AssertionError(f'Generated manifest page is missing: {generated_path}')
    generated_document = document_for(generated_page)
    generated_canonicals = generated_document.select('link[rel="canonical"]')
    if has_noindex(generated_document) or len(generated_canonicals) != 1:
        continue
    if generated_canonicals[0].get('href') != BASE + generated_path:
        continue
    if generated_path == '/index.html':
        continue
    assert BASE + generated_path in url_set, f'Indexable self-canonical generated page missing from sitemap: {generated_path}'

# Protect the low-value taxonomy policy: tag/topic pages with fewer than three
# associated published articles and no authored description/body remain accessible
# but noindex, and are never listed in the sitemap.
taxonomy_usage = {'tags': Counter(), 'topics': Counter()}
for section in SECTIONS:
    for source in (CONTENT / section).glob('*.md'):
        metadata, _body = read_doc(source)
        if metadata.get('draft'):
            continue
        for tag in metadata.get('tags') or []:
            taxonomy_usage['tags'][str(tag)] += 1
        if metadata.get('topic'):
            taxonomy_usage['topics'][str(metadata['topic'])] += 1
taxonomy_records = {'tags': {}, 'topics': {}}
for kind in ('tags', 'topics'):
    for source in (CONTENT / kind).glob('*.md'):
        metadata, body = read_doc(source)
        ident = str(metadata.get('id') or source.stem)
        taxonomy_records[kind][ident] = (metadata, body)
low_value_taxonomy_pages = 0
for kind in ('tags', 'topics'):
    identifiers = set(taxonomy_usage[kind]) | set(taxonomy_records[kind])
    for ident in identifiers:
        usage_count = taxonomy_usage[kind][ident]
        metadata, body = taxonomy_records[kind].get(ident, ({}, ''))
        if metadata.get('indexable') is True or usage_count >= 3 or str(metadata.get('description') or '').strip() or body.strip():
            continue
        page = ROOT / kind / f'{ident}.html'
        assert page.is_file(), f'Missing generated taxonomy page: /{kind}/{ident}.html'
        document = document_for(page)
        assert has_noindex(document), f'Thin taxonomy page must be noindex,follow: /{kind}/{ident}.html'
        assert BASE + f'/{kind}/{ident}.html' not in url_set, f'Thin taxonomy page must be omitted from sitemap: /{kind}/{ident}.html'
        low_value_taxonomy_pages += 1

# An authored topic landing page can be substantive even when the generic
# taxonomy association counter is incomplete. It must not inherit the thin-topic
# noindex rule from an empty taxonomy record.
terraform_url = BASE + '/topics/terraform-systems.html'
terraform_page = ROOT / 'topics' / 'terraform-systems.html'
assert terraform_page.is_file(), 'Authored Terraform Systems landing page is missing'
terraform_document = document_for(terraform_page)
assert not has_noindex(terraform_document), 'Substantive Terraform Systems landing page must remain indexable'
assert terraform_url in url_set, 'Substantive Terraform Systems landing page must be in the sitemap'
assert terraform_document.select_one('meta[name="description"][content]') and terraform_document.select_one('meta[name="description"]').get('content', '').strip(), 'Terraform Systems landing page must have a description'

# Homepage heading semantics and search-control accessible name are regressions.
homepage_document = document_for(ROOT / 'index.html')
assert len(homepage_document.select('main h1')) == 1, 'Homepage must render exactly one main h1'
search_document = document_for(ROOT / 'search.html')
search_input = search_document.select_one('#site-search-input')
assert search_input is not None, 'Site-search input is missing'
assert (search_input.get('aria-label') or search_input.get('aria-labelledby') or search_input.find_parent('label')) , 'Site-search input has no accessible name'

# Representative article metadata and Article JSON-LD are part of the release contract.
article_path = ROOT / 'posts' / 'zfs-scrub-resilver-snapshot-replication.html'
assert article_path.is_file(), 'Representative published article is missing'
article = document_for(article_path)
assert article.select_one('meta[name="description"][content]') and article.select_one('meta[name="description"]').get('content', '').strip(), 'Representative article has no description'
for prop in ('og:title', 'og:description', 'og:url'):
    assert article.select_one(f'meta[property="{prop}"]'), f'Representative article is missing {prop}'
schemas = []
for node in article.select('script[type="application/ld+json"]'):
    try:
        value = json.loads(node.string or node.get_text())
        schemas.extend(value if isinstance(value, list) else [value])
    except (TypeError, ValueError):
        raise AssertionError('Invalid JSON-LD in representative article')
assert any(item.get('@type') == 'Article' and item.get('url') == BASE + '/posts/zfs-scrub-resilver-snapshot-replication.html' for item in schemas), 'Representative article is missing matching Article JSON-LD'

assert low_value_taxonomy_pages > 0, 'Expected at least one thin tag page to exercise the noindex policy'
print(f'SEO checks passed: {len(urls)} unique canonical/indexable sitemap URLs; {noindex_count} noindex public HTML pages excluded; {low_value_taxonomy_pages} low-value tag/topic pages intentionally noindex; article metadata/schema, homepage, and robots.txt verified.')
