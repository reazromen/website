"""One-time, fail-closed migration from the preserved Git checkout."""
from cms_common import *
from collections import Counter

def main():
    if (CONTENT/'migration.json').exists(): raise SystemExit('Migration already exists; refusing to overwrite content.')
    original_files={str(p.relative_to(ROOT)):p.read_text() for p in ROOT.rglob('*.html') if not any(x in p.parts for x in ('.git','pagefind','cms'))}
    existing={}
    for sec in ('music','perspectives','bangla','writing'):
        for p in (CONTENT/sec).glob('*.md'):
            meta,body=read_doc(p);existing['/posts/'+p.stem+'.html']=(p,meta,body)
    perspective_urls={route(a.get('href',''),'/perspectives.html') for a in soup(original_files['perspectives.html']).select('main .post-card a')}
    tax={'topics':{},'tags':{}}
    def taxid(kind,label,ident=None):
        label=label.strip()
        ident=ident or slug(label)
        if ident in tax[kind] and tax[kind][ident]['title'].casefold()!=label.casefold(): ident+='-'+digest(label)[:6]
        tax[kind].setdefault(ident,{'title':label,'id':ident,'description':'','aliases':[]})
        return ident
    for name,raw in original_files.items():
        if re.match(r'^topics/[^/]+\.html$',name):
            s=soup(raw);h=s.select_one('main h1')
            taxid('topics',h.get_text(' ',strip=True) if h else Path(name).stem,Path(name).stem)
    records=[]; fingerprints={}; urlmap={}; originals={}; exceptions=[]
    for name,raw in original_files.items():
        if not name.startswith('posts/') or name=='posts/index.html': continue
        s=soup(raw);a=s.select_one('main article'); b=a.select_one('div.prose') if a else None
        if not a or not a.h1: raise ValueError('No article/title: '+name)
        title=a.h1.get_text(' ',strip=True)
        if b is None:
            # The one older standalone article places prose directly inside article.
            b=s.new_tag('div',attrs={'class':'prose'})
            for n in list(a.contents):
                if getattr(n,'name',None)=='h1' or (getattr(n,'attrs',None) and 'muted' in n.get('class',[])):continue
                b.append(n.extract())
            a.append(b)
        rawbody=inner(b); body=md(rawbody)
        if text(rawbody) and not body: raise ValueError('Empty conversion: '+name)
        fingerprint=digest(title+'\n'+text(rawbody))
        url='/'+name; key=slug(name[:-5].replace('/','--'))
        orig={'url':url,'title':title,'body_text':text(rawbody),'links':[x.get('href') for x in b.select('a[href]')],'images':[x.get('src') for x in b.select('img[src]')]}
        originals[url]=orig
        typ=s.select_one('meta[data-pagefind-filter="type[content]"]')
        typ=typ.get('content','') if typ else ''
        bn=sum('\u0980'<=c<='\u09ff' for c in text(rawbody)); latin=sum('a'<=c.lower()<='z' for c in text(rawbody))
        section='music' if typ=='Music' or a.select_one('a[href*="music.html"]') else ('bangla' if bn>latin//2 and bn>50 else ('perspectives' if url in perspective_urls else 'writing'))
        lede=a.select_one('.lede'); excerpt=lede.get_text(' ',strip=True) if lede else ''
        date=re.search(r'Published\s+(\d{4}-\d{2}-\d{2})',a.get_text(' ',strip=True))
        if not date:
            date=re.search(r'(September \d{1,2}, 2026)',a.get_text(' ',strip=True))
            date_value=__import__('datetime').datetime.strptime(date[1],'%B %d, %Y').date().isoformat() if date else ''
        else:date_value=date[1]
        read=re.search(r'(\d+)\s*min',a.get_text(' ',strip=True))
        tags_node=a.select_one('.tags'); tag_labels=[x.get_text(' ',strip=True) for x in tags_node.find_all(['span','a'],recursive=False)] if tags_node else []
        tags=[taxid('tags',t) for t in tag_labels if t]
        topic_node=a.select_one('.breadcrumbs a[href*="topics/"]')
        topic=Path(route(topic_node['href'],url)).stem if topic_node else ''
        if topic and topic not in tax['topics']:taxid('topics',topic_node.get_text(' ',strip=True),topic)
        artist_node=s.select_one('meta[data-pagefind-filter="artist[content]"]')
        artist=artist_node.get('content','') if artist_node else ''
        if section=='music' and not artist:
            artist=next((t for t in tag_labels if t in ('System of a Down','Pink Floyd')),'')
            if not artist: artist='Pink Floyd' if 'pink floyd' in a.get_text(' ',strip=True).lower() else 'System of a Down'
        album=''; year=''
        for n in a.select('.article-meta > span'):
            m=re.match(r'(.+?)\s*·\s*(\d{4})$',n.get_text(' ',strip=True))
            if m:album,year=m.groups()
        research='research-listening' in tag_labels or 'RESEARCH LISTENING' in a.get_text(' ',strip=True)
        eyebrow=a.select_one('.eyebrow'); eyebrow_text=eyebrow.get_text(' ',strip=True) if eyebrow else ''
        meta={'title':title,'url':url,'date':date_value,'read_time':int(read[1]) if read else max(1,len(body.split())//200),'excerpt':excerpt,'topic':topic,'tags':tags,'draft':False,'featured':False,'language':'bn' if bn>latin//2 and bn>50 else 'en','eyebrow':eyebrow_text}
        if section=='music':meta.update(artist=artist,album=album,year=year,kind='research' if research else ('album' if 'ALBUM' in eyebrow_text else 'song'))
        if url in existing:
            p,oldmeta,body=existing[url]; section=p.parent.name
            meta.update(oldmeta);meta['url']=url
            if oldmeta.get('topic'):meta['topic']=taxid('topics',oldmeta['topic'])
            meta['tags']=[taxid('tags',t) for t in oldmeta.get('tags',[])]
        slot(b,'BODY');slot(a.h1,'TITLE')
        if lede:slot(lede,'EXCERPT')
        if eyebrow:slot(eyebrow,'EYEBROW')
        if tags_node:slot(tags_node,'TAGS')
        else:
            tags_node=s.new_tag('div',attrs={'class':'tags'});slot(tags_node,'TAGS');b.insert_before(tags_node)
        if topic_node:topic_node['href']='{{RR_TOPIC_URL}}';slot(topic_node,'TOPIC_TITLE')
        for n in a.select('.article-meta > span'):
            t=n.get_text(' ',strip=True)
            if t.startswith('Published '):slot(n,'DATE')
            elif re.search(r'\d+\s*min',t):slot(n,'READ')
            elif re.match(r'.+?\s*·\s*\d{4}$',t):slot(n,'ALBUM_YEAR')
        if s.title:slot(s.title,'BROWSER_TITLE')
        desc=s.select_one('meta[name="description"]')
        if desc:desc['content']='{{RR_DESCRIPTION}}'
        for n in s.select('meta[data-pagefind-meta="title[content]"]'):n['content']='{{RR_TITLE}}'
        template=template_save('posts/'+key,s)
        source={'hash':digest(body),'html':rawbody}
        (TEMPLATES/'posts'/(key+'.json')).write_text(json.dumps(source,ensure_ascii=False))
        out={'url':url,'template':template,'source':str((TEMPLATES/'posts'/(key+'.json')).relative_to(ROOT))}
        if fingerprint in fingerprints and url not in existing:
            rec=fingerprints[fingerprint];rec['meta']['outputs'].append(out);urlmap[url]=rec
        else:
            file=CONTENT/section/(key.removeprefix('posts--')+'.md')
            meta['outputs']=[out]
            rec={'file':file,'section':section,'meta':meta,'body':body}
            records.append(rec);fingerprints[fingerprint]=rec;urlmap[url]=rec
    for rec in records:write_doc(rec['file'],rec['meta'],rec['body'])
    # Retire only the old structured filename when its content was migrated.
    for url,(p,meta,body) in existing.items():
        if url in urlmap and p!=urlmap[url]['file']:p.unlink()
    for kind,items in tax.items():
        for ident,m in items.items():write_doc(CONTENT/kind/(ident+'.md'),m,'')
    nav=json.loads((ROOT/'assets/navigation.json').read_text())
    footer=soup(original_files['index.html']).select_one('footer nav')
    nav['footer']=[{'label':x.get_text(' ',strip=True),'href':route(x.get('href',''),'/index.html'),'enabled':True} for x in footer.select('a')] if footer else []
    write_yaml(CONTENT/'site/navigation.yml',nav)
    pagecount=0; dynamic={}
    for name,raw in original_files.items():
        if '/'+name in urlmap:continue
        s=soup(raw); main=s.find('main')
        if not main:continue
        url='/'+name; key=slug(name[:-5].replace('/','--')); lists=[]
        # Existing card layouts become generated lists; introduction/design stays intact.
        containers=[]
        for card in main.select('.post-card'):
            if card.parent not in containers:containers.append(card.parent)
        if name in ('music.html','music/index.html'):
            for sel,kind in [('[aria-label="Music writing"] .music-bridge-list','song'),('[aria-label="Album writing"] .music-bridge-list','album')]:
                node=main.select_one(sel)
                if node:lists.append({'key':'LIST'+str(len(lists)),'filter':{'section':'music','kind':kind},'style':'music'});slot(node,lists[-1]['key'])
        for node in containers:
            # Keep each site's card style and original membership where no general filter applies.
            members=[]
            cards=node.find_all(class_='post-card',recursive=False)
            for c in cards:
                for a in c.select('a[href]'):
                    u=route(a['href'],url)
                    if u in urlmap:members.append(u);break
            if not members:continue
            rule={'urls':list(dict.fromkeys(members))}
            if name.startswith('topics/'):
                ident=Path(name).stem if Path(name).stem!='index' else Path(name).parent.name;rule={'topic':ident}
            elif name in ('archive.html','archive/index.html','author/reaz-romen.html'):rule={'all':True}
            elif name in ('writing.html','writing/index.html'):rule={'section':['writing','perspectives','bangla']}
            elif name in ('perspectives.html','perspectives/index.html') and len(members)>20:rule={'section':'perspectives'}
            item={'key':'LIST'+str(len(lists)),'filter':rule,'style':'cards'};lists.append(item)
            first=cards[0];first.insert_before('{{RR_'+item['key']+'}}')
            for c in cards:c.decompose()
        # Artist indexes use tables on some historical pages: detect their linked containers below.
        if name.startswith('music/') and name not in ('music/index.html',):
            artist='System of a Down' if 'system-of-a-down' in name else ('Pink Floyd' if 'pink-floyd' in name else '')
            if artist:
                candidates=main.select('.music-bridge-list, .post-list, tbody')
                for node in candidates:
                    if any(route(a.get('href',''),url) in urlmap for a in node.select('a[href]')):
                        item={'key':'LIST'+str(len(lists)),'filter':{'section':'music','artist':artist},'style':'table' if node.name=='tbody' else 'music'};lists.append(item);slot(node,item['key']);break
        if name in ('bangla.html','bangla/index.html') and not any(x['filter'].get('section')=='bangla' for x in lists):
            node=main.select_one('.post-list')
            if not node:node=s.new_tag('div',attrs={'class':'post-list editorial-list'});main.append(node)
            item={'key':'LIST'+str(len(lists)),'filter':{'section':'bangla'},'style':'cards'};lists.append(item);slot(node,item['key'])
        blocks=[];sources={}
        for node in list(main.find_all(['h1','h2','h3','h4','h5','h6','p','li','dt','dd','figcaption'])):
            if node.find_parent(['p','li','dt','dd','figcaption']) or node.find_parent(class_='post-card'):continue
            if '{{RR_' in str(node) or not node.get_text(strip=True):continue
            ident='BLOCK'+str(len(blocks));rawblock=inner(node);body=md(rawblock)
            blocks.append({'id':ident,'label':node.get_text(' ',strip=True)[:95],'body':body})
            sources[ident]={'hash':digest(body),'html':rawblock,'inline':node.name!='li'};slot(node,ident)
        title=s.title.get_text() if s.title else name;description=s.select_one('meta[name="description"]')
        meta={'title':(soup(raw).select_one('main h1').get_text(' ',strip=True) if soup(raw).select_one('main h1') else name),'browser_title':title,'description':description.get('content','') if description else '', 'url':url,'draft':False,'blocks':blocks,'lists':lists,'template':template_save('pages/'+key,s),'source':'cms/templates/pages/'+key+'.json'}
        (TEMPLATES/'pages'/(key+'.json')).write_text(json.dumps(sources,ensure_ascii=False))
        write_yaml(CONTENT/'pages'/(key+'.yml'),meta);pagecount+=1;dynamic[url]=lists
    manifest={'version':2,'original_commit':__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'posts':{u:{'source':str(r['file'].relative_to(ROOT))} for u,r in urlmap.items()},'counts':{'post_urls':len(urlmap),'unique_posts':len(records),'pages':pagecount,'sections':dict(Counter(r['section'] for r in records)),'topics':len(tax['topics']),'tags':len(tax['tags'])}}
    (CONTENT/'migration.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    (ROOT/'cms/migration-baseline.json').write_text(json.dumps(originals,ensure_ascii=False))
    print(json.dumps(manifest['counts'],ensure_ascii=False,indent=2))

if __name__=='__main__':main()
