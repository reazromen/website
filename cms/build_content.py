"""Deterministic CMS renderer. Validate every record before changing public output."""
from cms_common import *
from datetime import datetime, timezone
from email.utils import format_datetime
from collections import defaultdict
from copy import deepcopy
import xml.etree.ElementTree as ET

SECTIONS=('writing','perspectives','music','movies','archaeology','heritage','bangla','local-cultures','world-cultures')
ASSET_VERSIONS={}
# Keep one indexable URL for legacy .html and /index.html copies. The
# alternate paths remain accessible but canonicalize to the .html URL.
CANONICAL_ALIASES = {
    '/archive/index.html': '/archive.html',
    '/bangla/index.html': '/bangla.html',
    '/movies/index.html': '/movies.html',
    '/music/index.html': '/music.html',
    '/notes/index.html': '/notes.html',
    '/now/index.html': '/now.html',
    '/perspectives/index.html': '/perspectives.html',
    '/portfolio/index.html': '/portfolio.html',
    '/reference-reader/index.html': '/reference-reader.html',
    '/services/index.html': '/services.html',
    '/systems/index.html': '/systems.html',
    '/topics/redis-systems/index.html': '/topics/redis-systems.html',
    '/topics/terraform-systems/index.html': '/topics/terraform-systems.html',
}
_SHARED_CHROME=None

def shared_chrome():
    global _SHARED_CHROME
    if _SHARED_CHROME is None:
        _SHARED_CHROME=soup((ROOT/'cms/shell.tpl').read_text())
    return _SHARED_CHROME

def load_all():
    tax={k:{} for k in ('tags','topics')}
    for k in tax:
        for p in sorted((CONTENT/k).glob('*.md')):
            m,b=read_doc(p);ident=m.get('id') or p.stem
            if ident in tax[k] or '/' in ident or not m.get('title'):raise ValueError('Invalid taxonomy: '+str(p))
            m.update(id=ident,body=b);tax[k][ident]=m
    entries=[];owned={}
    def own(url,source):
        target(url)
        if url in owned:raise ValueError('Duplicate output '+url+' in '+source+' and '+owned[url])
        owned[url]=source
    for section in SECTIONS:
        for p in sorted((CONTENT/section).glob('*.md')):
            m,b=read_doc(p);m.update(section=section,body=b,source_file=str(p.relative_to(ROOT)))
            if not m.get('title') or not b:raise ValueError('Missing title/body: '+str(p))
            m['url']=m.get('url') or '/posts/'+p.stem+'.html'; m['tags']=m.get('tags') or [];m['topic']=m.get('topic') or ''
            # Content can introduce a new topic or tag. Create a minimal taxonomy
            # record automatically so one unregistered label cannot block the
            # entire production publish queue. Editors can refine its metadata later.
            def ensure_taxonomy(kind, ident):
                if not isinstance(ident, str) or not re.fullmatch(r'[a-z0-9]+(?:[-_][a-z0-9]+)*', ident):
                    raise ValueError('Invalid '+kind[:-1]+' identifier '+repr(ident)+' in '+str(p))
                if ident not in tax[kind]:
                    title = ident.replace('-', ' ').title()
                    tax[kind][ident] = {'id': ident, 'title': title, 'description': ''}
            if m['topic']:
                ensure_taxonomy('topics', m['topic'])
            if not isinstance(m['tags'],list):
                raise ValueError('Tags must be a list in '+str(p))
            for tag in m['tags']:
                ensure_taxonomy('tags', tag)
            if m.get('date'):datetime.fromisoformat(str(m['date']).replace('Z','+00:00'))
            if int(m.get('read_time',1))<1:raise ValueError('Reading time must be positive')
            urls={m['url']}|{o['url'] for o in m.get('outputs',[])}
            for url in urls:own(url,str(p))
            for o in m.get('outputs',[]):
                for key in ('template','source'):
                    f=(ROOT/o[key]).resolve()
                    if not f.is_relative_to(TEMPLATES.resolve()) or not f.is_file():raise ValueError('Missing/unsafe template '+str(f))
            entries.append(m)
    pages=[]
    for p in sorted((CONTENT/'pages').glob('*.yml')):
        m=yaml.safe_load(p.read_text());m.setdefault('url','/'+p.stem+'.html')
        own(m['url'],str(p));pages.append(m)
        if m.get('template'):
            for key in ('template','source'):
                f=(ROOT/m[key]).resolve()
                if not f.is_relative_to(TEMPLATES.resolve()) or not f.is_file():raise ValueError('Invalid page template '+str(f))
            ids=[x['id'] for x in m.get('blocks',[])]
            if len(ids)!=len(set(ids)):raise ValueError('Duplicate page block: '+str(p))
    nav=yaml.safe_load((CONTENT/'site/navigation.yml').read_text())
    def checklink(x):
        href=x.get('href','')
        if href and not re.match(r'^(https?://|mailto:|tel:|/|#)',href):raise ValueError('Unsafe navigation URL '+href)
        for child in x.get('children',[]):checklink(child)
    for key in ('main','footer'):
        for x in nav.get(key,[]):checklink(x)
    entries.sort(key=lambda m:(str(m.get('date','')),m['url']),reverse=True)
    return entries,pages,tax,nav,owned

def label(tax,kind,ident):return tax[kind].get(ident,{}).get('title',ident)
def tags_html(m,tax):
    return ''.join('<a data-pagefind-filter="tag" href="/tags/'+esc(t)+'.html">'+esc(label(tax,'tags',t))+'</a>' for t in m.get('tags',[]))
def post_values(m,tax,body):
    topic=m.get('topic','')
    return {'BODY':body,'TITLE':esc(m['title']),'EXCERPT':esc(m.get('excerpt','')),'EYEBROW':esc(m.get('eyebrow') or label(tax,'topics',topic) or m['section'].title()),'TAGS':tags_html(m,tax),'TOPIC_URL':'/topics/'+esc(topic)+'.html' if topic else '/topics.html','TOPIC_TITLE':esc(label(tax,'topics',topic)),'DATE':'Published '+esc(m.get('date','')),'READ':str(int(m.get('read_time',1)))+' min read','ALBUM_YEAR':esc(' · '.join(str(m.get(k,'')) for k in ('album','year') if m.get(k))),'BROWSER_TITLE':esc(m['title'])+' — Reaz Romen','DESCRIPTION':esc(m.get('description') or m.get('excerpt',''))}

def shell(title,body,description='',lang='en'):
    # Reuse the original site chrome and monochrome technical icons.
    base=soup((ROOT/'cms/shell.tpl').read_text())
    main=base.find('main');main.clear();main.append(soup(body))
    base.html['lang']=lang
    if base.title:base.title.string=title+' — Reaz Romen'
    d=base.select_one('meta[name="description"]')
    if d:d['content']=description
    for n in base.select('meta[data-pagefind-filter],meta[data-pagefind-meta]'):n.decompose()
    return str(base)

def new_post(m,tax):
    body=render_md(m['body'])
    image=m.get('cover_image')
    cover=f'<figure><img src="{esc(image)}" alt="{esc(m.get("cover_alt",""))}" loading="lazy"></figure>' if image else ''
    return shell(m['title'],f'<article class="article" data-pagefind-body><p class="eyebrow">{esc(m.get('eyebrow') or m["section"].replace('-', ' ').title())}</p><h1>{esc(m["title"])}</h1><p class="lede">{esc(m.get("excerpt",""))}</p><div class="article-meta"><span>Published {esc(m.get("date",""))}</span><span>{int(m.get("read_time",1))} min read</span></div><div class="tags">{tags_html(m,tax)}</div>{cover}<div class="prose">{body}</div></article>',m.get('excerpt',''),m.get('language','en'))

def card(m,tax,style='cards',index=1):
    if style=='home':
        return f'<a class="index-row" href="{esc(m["url"])}"><span class="index-icon"><svg class="tech-icon" aria-hidden="true" viewBox="0 0 24 24"><path d="M4 3h16v18H4zM8 8h8M8 12h8M8 16h5"/></svg></span><div><strong>{esc(m["title"])}</strong><span>{esc(m.get("excerpt",""))}</span></div><span class="row-meta">{esc(m.get("date",""))}</span></a>'
    if style=='music':
        detail=' · '.join(str(m.get(k,'')) for k in ('artist','album') if m.get(k))
        return f'<a class="music-bridge-link" href="{esc(m["url"])}"><span class="index">{index:02d}</span><strong>{esc(m["title"])}</strong><span>{esc(detail)} · {int(m.get("read_time",1))} MIN →</span></a>'
    if style=='table':return f'<tr><td>{index}</td><td><a href="{esc(m["url"])}">{esc(m["title"])}</a></td><td>{esc(m.get("album",""))}</td><td>{esc(m.get("year",""))}</td></tr>'
    return f'<article class="post-card"><p class="meta">{esc(label(tax,"topics",m.get("topic","")) or m["section"].title())} · {int(m.get("read_time",1))} min read · {esc(m.get("date",""))}</p><h3><a href="{esc(m["url"])}">{esc(m["title"])}</a></h3><p>{esc(m.get("excerpt",""))}</p><div class="tags">{tags_html(m,tax)}</div></article>'

def select(entries,rule):
    result=[]
    for m in entries:
        if m.get('draft'):continue
        if 'urls' in rule and not ({m['url']}|{x['url'] for x in m.get('outputs',[])})&set(rule['urls']):continue
        if 'section' in rule and m['section'] not in (rule['section'] if isinstance(rule['section'],list) else [rule['section']]):continue
        if 'topic' in rule and m.get('topic')!=rule['topic']:continue
        if 'tag' in rule and rule['tag'] not in m.get('tags',[]):continue
        if 'language' in rule and m.get('language')!=rule['language']:continue
        if 'artist' in rule and m.get('artist')!=rule['artist']:continue
        if 'kind' in rule and m.get('kind','song')!=rule['kind']:continue
        result.append(m)
    if rule.get('featured_first'):result.sort(key=lambda x:not x.get('featured',False))
    return result[:int(rule.get('limit',len(result)))]

def related_articles(entry,entries,limit=3):
    body=entry.get('body','') or ''
    if re.search(r'\]\(/|<a\b[^>]+href=[\"\']/',body,re.I):return []
    tags=set(entry.get('tags',[]) or []);topic=entry.get('topic')
    if not tags and not topic:return []
    language=entry.get('language','en');scored=[]
    for other in entries:
        if other.get('draft') or other.get('url')==entry.get('url'):continue
        if other.get('language','en')!=language:continue
        overlap=len(tags & set(other.get('tags',[]) or []))
        same_topic=bool(topic and topic==other.get('topic'))
        score=overlap*2+(4 if same_topic else 0)
        if score:scored.append((score,other))
    scored.sort(key=lambda pair:(-pair[0],str(pair[1].get('date','')),pair[1].get('title','').casefold()),reverse=False)
    # Prefer the strongest topical/tag overlap, then the newest publication date.
    scored.sort(key=lambda pair:(-pair[0],pair[1].get('date','')),reverse=True)
    return [m for _,m in scored[:limit]]

def render_page(m,entries,tax):
    if not m.get('template'):
        body='<article class="article" data-pagefind-body><h1>'+esc(m['title'])+'</h1><div class="prose">'+render_md(m.get('body',''))+'</div></article>'
        for listing in m.get('lists',[]):
            rows=select(entries,listing['filter'])
            body+='<section class="section-block"><div class="post-list editorial-list">'+''.join(card(x,tax,listing.get('style','cards'),i+1) for i,x in enumerate(rows))+'</div></section>'
        return shell(m['title'],body,m.get('description',''))
    template=(ROOT/m['template']).read_text();sources=json.loads((ROOT/m['source']).read_text());values={}
    # Blocks are stable template locations. Removed blocks become empty, never leak slot markers.
    for ident,source in sources.items():values[ident]=''
    for b in m.get('blocks',[]):
        source=sources.get(b['id']);rendered=original_or_md(b.get('body',''),source)
        if source and source.get('inline') and rendered.startswith('<p>') and rendered.endswith('</p>') and rendered.count('<p>')==1:rendered=rendered[3:-4]
        values[b['id']]=rendered
    for listing in m.get('lists',[]):
        rows=select(entries,listing['filter']);values[listing['key']]='\n'.join(card(x,tax,listing.get('style','cards'),i+1) for i,x in enumerate(rows))
    for item in m.get('links',[]):
        href=item.get('url','')
        if not re.match(r'^(https?://|mailto:|tel:|/|#)',href):raise ValueError('Unsafe page link '+href)
        values[item['id']]=esc(href)
    rendered=fill(template,values);s=soup(rendered)
    if s.title:s.title.string=m.get('browser_title') or m['title']+' — Reaz Romen'
    d=s.select_one('meta[name="description"]')
    if d:d['content']=m.get('description','')
    return html_string(s)

def link(item,current):
    if item.get('enabled',True) is False:return ''
    href=item.get('href','');children=item.get('children',[]);name=esc(item.get('label',''))
    attr=' aria-current="page"' if route(href)==current else ''
    lang=' lang="'+esc(item['lang'])+'"' if item.get('lang') else ''
    a=f'<a href="{esc(href)}"{attr}{lang}>{name}</a>' if href else ''
    if children:
        overview=a.replace(f'>{name}</a>', '>Overview</a>')
        return f'<details class="nav-group"><summary>{name}</summary><div class="nav-submenu">{overview}{"".join(link(x,current) for x in children)}</div></details>'
    return a

def finalize(raw,url,nav,entry=None,tax=None,related_entries=None):
    s=soup(raw)
    # Every published page uses the same reviewed global header/footer. Legacy
    # article templates may still contain nav-right markup or omit a footer;
    # normalize the public output here instead of fixing each page by hand.
    chrome=shared_chrome()
    shared_header=chrome.select_one('body > header.rr-global-header')
    shared_footer=chrome.select_one('body > footer.site-footer')
    if s.body and shared_header:
        old_header=s.select_one('body > header.rr-global-header')
        new_header=deepcopy(shared_header)
        if old_header:
            old_header.replace_with(new_header)
        else:
            main=s.select_one('body > main')
            if main:main.insert_before(new_header)
            else:s.body.insert(0,new_header)
    if s.body and shared_footer:
        old_footer=s.select_one('body > footer')
        keep_research_note=bool(old_footer and 'Research listening notes are separated from personal listening-memory essays.' in old_footer.get_text(' ',strip=True))
        new_footer=deepcopy(shared_footer)
        if keep_research_note:
            note=s.new_tag('p',attrs={'class':'footer-note'})
            note.string='Research listening notes are separated from personal listening-memory essays.'
            description=new_footer.find('p')
            if description:description.insert_after(note)
        if old_footer:
            old_footer.replace_with(new_footer)
        else:
            main=s.select_one('body > main')
            if main:main.insert_after(new_footer)
            else:s.body.append(new_footer)
    # Use a new, separately cacheable asset URL for the mobile navigation fix.
    # The existing responsive-v3.css path may remain cached at the edge after a release.
    if s.head and s.select_one('body > main') and not s.select_one('link[rel="stylesheet"][href*="/assets/mobile-nav.css"]'):
        s.head.append(s.new_tag('link',rel='stylesheet',href='/assets/mobile-nav.css'))
    # Version stylesheet/script URLs so a new HTML deployment cannot reuse stale browser assets.
    for node in s.select('link[rel="stylesheet"][href],script[src]'):
        attr='href' if node.name=='link' else 'src';asset=route(node[attr],url)
        if not asset:continue
        path=(ROOT/asset.lstrip('/')).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():continue
        if asset not in ASSET_VERSIONS:ASSET_VERSIONS[asset]=hashlib.sha256(path.read_bytes()).hexdigest()[:12]
        node[attr]=urlsplit(node[attr]).path+'?v='+ASSET_VERSIONS[asset]
    for n in s.select('.rr-global-header .nav-scroll,.rr-global-header .nav-right'):
        n.clear();n.append(soup(''.join(link(x,url) for x in nav.get('main',[]))))
    for n in s.select('footer nav'):
        n.clear();n.append(soup(''.join(link(x,url) for x in nav.get('footer',[]))))
    canonical=s.select_one('link[rel="canonical"]')
    if not canonical:canonical=s.new_tag('link',rel='canonical');s.head.append(canonical)
    canonical['href']='https://reazromen.com'+CANONICAL_ALIASES.get(url, url)
    if entry and entry.get('indexable') is False:
        robots=s.select_one('meta[name="robots"]')
        if not robots:
            robots=s.new_tag('meta',attrs={'name':'robots'})
            s.head.append(robots)
        robots['content']='noindex,follow'
    # Structured data belongs in the renderer, not only in generated HTML:
    # build_content.py recreates these pages on every publish.
    schema_by_url = {
        '/index.html': {
            '@context': 'https://schema.org',
            '@type': 'WebSite',
            '@id': 'https://reazromen.com/#website',
            'name': 'Reaz Romen',
            'url': 'https://reazromen.com/',
            'description': 'Systems engineering across Linux infrastructure, SIP/RTP and VoIP, embedded systems, cloud infrastructure, networking and observability.',
            'publisher': {'@id': 'https://reazromen.com/author/reaz-romen.html#person'}
        },
        '/about.html': {
            '@context': 'https://schema.org',
            '@type': 'Person',
            '@id': 'https://reazromen.com/author/reaz-romen.html#person',
            'name': 'Reaz Romen',
            'url': 'https://reazromen.com/author/reaz-romen.html',
            'jobTitle': 'Systems Engineer and Technical Author',
            'description': 'Systems engineer working across Linux infrastructure, SIP/RTP and VoIP, embedded systems, cloud infrastructure, networking and observability.',
            'sameAs': [
                'https://www.linkedin.com/in/reaz-romen',
                'https://github.com/reazromen',
                'https://medium.com/@returnofhe'
            ],
            'knowsAbout': [
                'Linux system administration', 'SIP', 'RTP', 'VoIP', 'Asterisk',
                'FreeSWITCH', 'OpenSIPS', 'Cloud infrastructure', 'Embedded systems',
                'ESP32', 'ESP-IDF', 'Kubernetes', 'Observability'
            ]
        }
    }
    page_topics = {
        '/systems.html': ['Linux infrastructure', 'embedded firmware', 'real-time communications', 'observability'],
        '/portfolio.html': ['embedded systems projects', 'SIP/RTP systems', 'Linux infrastructure', 'observability'],
        '/telecom.html': ['SIP', 'RTP', 'VoIP', 'PBX infrastructure', 'telecommunications'],
        '/observability.html': ['Linux infrastructure', 'monitoring', 'metrics', 'logs', 'reliability engineering']
    }
    if url in page_topics:
        schema_by_url[url] = {
            '@context': 'https://schema.org',
            '@type': 'WebPage',
            'name': s.title.get_text(' ', strip=True) if s.title else url.strip('/'),
            'description': (s.select_one('meta[name="description"]').get('content', '') if s.select_one('meta[name="description"]') else ''),
            'url': 'https://reazromen.com' + url,
            'about': {'@id': 'https://reazromen.com/author/reaz-romen.html#person'},
            'keywords': page_topics[url],
            'isPartOf': {'@id': 'https://reazromen.com/#website'}
        }
    schema_data = schema_by_url.get(url)
    if schema_data and not s.select_one('script[type="application/ld+json"]'):
        schema_node = s.new_tag('script', type='application/ld+json')
        schema_node.string = json.dumps(schema_data, ensure_ascii=False, separators=(',', ':'))
        s.head.append(schema_node)
    if entry:
        s.html['lang']=entry.get('language','en')
        # Explicit schema.org identity: make every published article unambiguously
        # attributable to the site's canonical author entity.
        author_url='https://reazromen.com/author/reaz-romen.html'
        article_url='https://reazromen.com'+url
        schema={
            '@context':'https://schema.org',
            '@type':'Article',
            'headline':entry['title'],
            'description':entry.get('excerpt',''),
            'url':article_url,
            'mainEntityOfPage':{'@type':'WebPage','@id':article_url},
            'datePublished':str(entry.get('date',''))[:10],
            'author':{
                '@type':'Person',
                '@id':author_url+'#person',
                'name':'Reaz Romen',
                'url':author_url,
                'sameAs':[
                    'https://reazromen.com/',
                    'https://www.linkedin.com/in/reaz-romen',
                    'https://github.com/reazromen',
                    'https://medium.com/@returnofhe'
                ]
            },
            'publisher':{'@type':'Person','@id':author_url+'#person','name':'Reaz Romen'},
            'isPartOf':{'@type':'WebSite','@id':'https://reazromen.com/#website','name':'Reaz Romen','url':'https://reazromen.com/'}
        }
        node=s.new_tag('script',type='application/ld+json')
        node.string=json.dumps(schema,ensure_ascii=False,separators=(',',':'))
        s.head.append(node)
        article=s.select_one('main article')
        if article:article['data-pagefind-body']=''
        if related_entries and article:
            section=soup('<section class="section-block related-reading" aria-labelledby="related-reading-title"><h2 id="related-reading-title">Related reading</h2><div class="post-list editorial-list">'+''.join(card(item,tax) for item in related_entries)+'</div></section>')
            article.insert_after(section)
        if entry.get('cover_image'):
            article=s.select_one('main article');body=article.select_one('.prose') if article else None
            if body and not article.select_one('figure.cms-cover'):
                figure=s.new_tag('figure',attrs={'class':'cms-cover'});img=s.new_tag('img',src=entry['cover_image'],alt=entry.get('cover_alt',''));figure.append(img);body.insert_before(figure)
            og=s.select_one('meta[property="og:image"]')
            if not og:og=s.new_tag('meta',property='og:image');s.head.append(og)
            og['content']=urljoin('https://reazromen.com'+url,entry['cover_image'])
        for n in s.select('meta[data-pagefind-filter="tag[content]"],meta[data-pagefind-filter="topic[content]"]'):n.decompose()
        for kind,ids in [('tag',entry.get('tags',[])),('topic',[entry['topic']] if entry.get('topic') else [])]:
            for ident in ids:
                n=s.new_tag('meta');n['data-pagefind-filter']=kind+'[content]';n['content']=label(tax,kind+'s',ident);s.head.append(n)
        for prop,val in [('og:title',entry['title']),('og:description',entry.get('excerpt','')),('og:url','https://reazromen.com'+url)]:
            n=s.select_one('meta[property="'+prop+'"]')
            if not n:n=s.new_tag('meta',property=prop);s.head.append(n)
            n['content']=val
    # The author page is the canonical identity record used by Article.author/@id.
    if url == '/author/reaz-romen.html':
        author_schema={
            '@context':'https://schema.org',
            '@type':'Person',
            '@id':'https://reazromen.com/author/reaz-romen.html#person',
            'name':'Reaz Romen',
            'url':'https://reazromen.com/author/reaz-romen.html',
            'jobTitle':'Systems Engineer & Technical Author',
            'description':'Systems engineer working across embedded devices, networks, real-time communications, backend systems, Linux infrastructure, observability, and operational tooling.',
            'sameAs':[
                'https://reazromen.com/',
                'https://www.linkedin.com/in/reaz-romen',
                'https://github.com/reazromen',
                'https://medium.com/@returnofhe'
            ],
            'knowsAbout':[
                'SIP','RTP','WebRTC','FreeSWITCH','VoIP','Linux',
                'embedded systems','Kubernetes','networking','observability',
                'real-time audio','telecommunications'
            ]
        }
        node=s.new_tag('script',type='application/ld+json')
        node.string=json.dumps(author_schema,ensure_ascii=False,separators=(',',':'))
        s.head.append(node)
    if url == '/':
        website_schema={
            '@context':'https://schema.org',
            '@type':'WebSite',
            '@id':'https://reazromen.com/#website',
            'name':'Reaz Romen',
            'url':'https://reazromen.com/',
            'description':'Systems engineering across embedded devices, real-time communications, Linux infrastructure, networking and observability.',
            'author':{'@id':'https://reazromen.com/author/reaz-romen.html#person'}
        }
        node=s.new_tag('script',type='application/ld+json')
        node.string=json.dumps(website_schema,ensure_ascii=False,separators=(',',':'))
        s.head.append(node)
    if '{{RR_' in str(s):raise ValueError('Unresolved template slot at '+url)
    return html_string(s)

def main():
    entries,pages,tax,nav,owned=load_all(); outputs={};public=[m for m in entries if not m.get('draft')]
    for m in public:
        legacy=m.get('outputs',[])
        if legacy:
            for o in legacy:
                source=json.loads((ROOT/o['source']).read_text())
                rendered=fill((ROOT/o['template']).read_text(),post_values(m,tax,original_or_md(m['body'],source)))
                outputs[o['url']]=finalize(rendered,m['url'],nav,m,tax,related_articles(m,public))
            if m['url'] not in outputs:outputs[m['url']]=outputs[legacy[0]['url']]
        else:outputs[m['url']]=finalize(new_post(m,tax),m['url'],nav,m,tax,related_articles(m,public))
    for m in pages:
        if m['url'].startswith('/topics/'):
            ident=Path(m['url']).stem if not m['url'].endswith('/index.html') else Path(m['url']).parent.name
            if ident not in tax['topics']:continue
        if not m.get('draft'):
            raw=render_page(m,entries,tax)
            if not m.get('lists'):
                s=soup(raw)
                if s.find('main'):s.find('main')['data-pagefind-body']=''
                raw=html_string(s)
            outputs[m['url']]=finalize(raw,m['url'],nav)
    # New research notes stay distinct from personal listening memories.
    new_music=[m for m in public if m.get('section')=='music' and m.get('editorial_batch')=='20261003-100-niches']
    for music_url in ('/music.html','/music/index.html'):
        if music_url in outputs and new_music:
            s=soup(outputs[music_url]); main=s.find('main')
            section=soup('<section class="section-block music-notes-section" id="new-listening-notes"><h2>নতুন লিসেনিং নোট</h2><p>গান, অ্যালবাম ও শোনার পদ্ধতি নিয়ে বিশ্লেষণ।</p><div class="music-bridge-list">'+''.join(card(m,tax,'music',i) for i,m in enumerate(new_music,1))+'</div></section>')
            if main:main.append(section)
            outputs[music_url]=finalize(html_string(s),music_url,nav)
    for kind in ('topics','tags'):
        for ident,t in tax[kind].items():
            url='/'+kind+'/'+ident+'.html';rows=select(entries,{kind[:-1]:ident})
            if url in outputs:
                s=soup(outputs[url]);h=s.select_one('main h1')
                if h:h.string=t['title']
                if s.title:s.title.string=t['title']+' — Reaz Romen'
                if t.get('description'):
                    lead=s.select_one('main .lede')
                    if lead:lead.string=t['description']
                if t.get('body'):
                    main=s.find('main');intro=s.new_tag('div',attrs={'class':'prose'});intro.append(soup(render_md(t['body'])))
                    if h:h.insert_after(intro)
                    elif main:main.insert(0,intro)
                outputs[url]=str(s)
            else:
                body='<h1>'+esc(t['title'])+'</h1><div class="prose">'+render_md(t.get('body') or t.get('description',''))+'</div><div class="post-list editorial-list">'+''.join(card(x,tax) for x in rows)+'</div>'
                outputs[url]=finalize(shell(t['title'],body,t.get('description','')),url,nav)
            if kind=='tags' and len(rows)<3 and not str(t.get('description','')).strip() and not str(t.get('body','')).strip():
                page=soup(outputs[url]);robots=page.select_one('meta[name="robots"]')
                if not robots:
                    robots=page.new_tag('meta',attrs={'name':'robots'});page.head.append(robots)
                robots['content']='noindex,follow';outputs[url]=str(page)
            for alias in t.get('aliases',[]):
                target(alias)
                if alias in owned and alias!=url:raise ValueError('Taxonomy alias collision: '+alias)
                outputs[alias]=redirect(url)
        url='/'+kind+'.html'
        rows=[]
        for ident,t in sorted(tax[kind].items(),key=lambda x:x[1]['title'].casefold()):
            count=len(select(entries,{kind[:-1]:ident}))
            rows.append('<a class="topic-card" href="/'+kind+'/'+esc(ident)+'.html"><strong>'+esc(t['title'])+'</strong><span>'+str(count)+(' post' if count==1 else ' posts')+'</span></a>')
        if kind=='topics' and url in outputs:
            s=soup(outputs[url]);grid=s.select_one('.topic-grid')
        else:
            s=soup(shell(kind.title(),'<section class="page-head"><h1>'+kind.title()+'</h1></section><div class="topic-grid"></div>'));grid=s.select_one('.topic-grid')
        if grid:
            grid.clear();grid.append(soup(''.join(rows)));grid['class']=['topic-grid','taxonomy-index']
            control=soup('<p><label>Find '+kind+' <input type="search" data-taxonomy-filter placeholder="Type to filter '+kind+'" aria-label="Find '+kind+'" style="width:100%;padding:.7rem;margin-top:.5rem;font:inherit;background:transparent;color:inherit;border:1px solid var(--line)"></label><span data-taxonomy-count role="status">'+str(len(rows))+' '+kind+'</span></p>')
            grid.insert_before(control)
            s.body.append(s.new_tag('script',src='/assets/taxonomy-v1.js'))
            outputs[url]=finalize(html_string(s),url,nav)
    from year_archives import render_archives
    render_archives(entries,outputs,nav,ROOT,shell,finalize,esc)
    # No mutations happen above this line. All output collisions are detected first.
    previous_path=ROOT/'cms/generated-manifest.json'
    if previous_path.exists():previous=json.loads(previous_path.read_text())
    else:previous=list(json.loads((CONTENT/'migration.json').read_text())['posts'])
    for url in set(previous)-set(outputs):
        p=target(url)
        if p.exists():p.unlink()
    for url,raw in outputs.items():
        p=target(url);p.parent.mkdir(parents=True,exist_ok=True)
        if not p.exists() or p.read_text()!=raw:p.write_text(raw)
    previous_path.write_text(json.dumps(sorted(outputs),ensure_ascii=False,indent=2)+'\n')
    (ROOT/'assets/navigation.json').write_text(json.dumps(nav,ensure_ascii=False,indent=2)+'\n')
    import os,subprocess
    commit=os.environ.get('GITHUB_SHA') or subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    (ROOT/'build-info.json').write_text(json.dumps({'commit':commit,'posts':len(public),'pages':len(pages),'topics':len(tax['topics']),'tags':len(tax['tags'])})+'\n')
    feeds(public,outputs,tax)
    print(json.dumps({'published_posts':len(public),'drafts':len(entries)-len(public),'pages':len(pages),'topics':len(tax['topics']),'tags':len(tax['tags']),'output_urls':len(outputs)},ensure_ascii=False))

def redirect(url):return '<!doctype html><html><head><meta http-equiv="refresh" content="0;url='+esc(url)+'"><link rel="canonical" href="https://reazromen.com'+esc(url)+'"></head><body><a href="'+esc(url)+'">Continue</a></body></html>'

def feeds(entries,outputs,tax=None):
    feed={'version':'https://jsonfeed.org/version/1.1','title':'Reaz Romen — Writing','home_page_url':'https://reazromen.com','feed_url':'https://reazromen.com/feed.json','items':[]}
    rss=ET.Element('rss',version='2.0');channel=ET.SubElement(rss,'channel')
    for k,v in [('title','Reaz Romen — Writing'),('link','https://reazromen.com'),('description','Articles and listening notes')]:ET.SubElement(channel,k).text=v
    atom=ET.Element('feed',xmlns='http://www.w3.org/2005/Atom');ET.SubElement(atom,'title').text='Reaz Romen — Writing';ET.SubElement(atom,'id').text='https://reazromen.com/'
    ET.SubElement(atom,'link',href='https://reazromen.com/atom.xml',rel='self')
    for m in entries[:100]:
        url='https://reazromen.com'+m['url'];item={'id':url,'url':url,'title':m['title'],'content_html':render_md(m['body']),'summary':m.get('excerpt',''),'tags':m.get('tags',[])}
        date=str(m.get('date',''))[:10]
        if date:item['date_published']=date+'T00:00:00+06:00'
        feed['items'].append(item)
        r=ET.SubElement(channel,'item')
        for k,v in [('title',m['title']),('link',url),('guid',url),('description',m.get('excerpt',''))]:ET.SubElement(r,k).text=v
        if date:ET.SubElement(r,'pubDate').text=format_datetime(datetime.fromisoformat(date).replace(tzinfo=timezone.utc))
        a=ET.SubElement(atom,'entry');ET.SubElement(a,'title').text=m['title'];ET.SubElement(a,'id').text=url;ET.SubElement(a,'link',href=url)
        ET.SubElement(a,'updated').text=(date or '2026-10-02')+'T00:00:00Z';ET.SubElement(a,'summary').text=m.get('excerpt','')
    ET.SubElement(atom,'updated').text=(str(entries[0].get('date',''))[:10] or '2026-10-02')+'T00:00:00Z' if entries else '2026-10-02T00:00:00Z'
    (ROOT/'feed.json').write_text(json.dumps(feed,ensure_ascii=False,indent=2)+'\n')
    for filename,tree in [('feed.xml',rss),('atom.xml',atom)]:ET.ElementTree(tree).write(ROOT/filename,encoding='utf-8',xml_declaration=True)
    non_indexable_urls={u for m in entries if not m.get('draft') and m.get('indexable') is False for u in ({m['url']}|{o['url'] for o in m.get('outputs',[])})}
    for ident,t in (tax or {}).get('tags',{}).items():
        post_count=sum(1 for m in entries if not m.get('draft') and ident in m.get('tags',[]))
        if post_count<3 and not str(t.get('description','')).strip() and not str(t.get('body','')).strip():
            non_indexable_urls.add('/tags/'+ident+'.html')
            non_indexable_urls.update(t.get('aliases',[]))
    sitemap=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for url in sorted(outputs):
        if url in CANONICAL_ALIASES or url in non_indexable_urls:continue
        ET.SubElement(ET.SubElement(sitemap,'url'),'loc').text='https://reazromen.com'+url
    ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)

if __name__=='__main__':main()
