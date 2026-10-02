from cms_common import *
from build_content import load_all,select,render_page,post_values,original_or_md,fill,card,new_post,finalize

def main():
    entries,pages,tax,nav,owned=load_all()
    baseline=json.loads((ROOT/'cms/migration-baseline.json').read_text());errors=[]
    for url,old in baseline.items():
        p=target(url)
        if not p.exists():errors.append('Missing old URL '+url);continue
        s=soup(p.read_text());body=s.select_one('main article div.prose')
        if not body:errors.append('Missing article body '+url);continue
        if text(inner(body))!=old['body_text']:errors.append('Body text changed '+url)
        if [a.get('href') for a in body.select('a[href]')]!=old['links']:errors.append('Body links changed '+url)
        if [a.get('src') for a in body.select('img[src]')]!=old['images']:errors.append('Body images changed '+url)
        h=s.select_one('main article h1')
        if not h or h.get_text(' ',strip=True)!=old['title']:errors.append('Title changed '+url)
    # A new record must flow into all matching lists; drafts must be excluded.
    tag=next(iter(tax['tags']));topic=next(iter(tax['topics']))
    fixture={'title':'CMS verification fixture','url':'/posts/cms-verification-fixture.html','body':'A paragraph with **formatting** and [a link](/music.html).','excerpt':'Verification only.','section':'music','kind':'song','artist':'System of a Down','album':'Test','date':'2026-10-03','read_time':1,'tags':[tag],'topic':topic,'draft':False,'language':'en'}
    assert select([fixture],{'topic':topic})==[fixture]
    assert select([fixture],{'tag':tag})==[fixture]
    assert select([fixture],{'section':'music','kind':'song'})==[fixture]
    assert select([dict(fixture,draft=True)],{'all':True})==[]
    music=next(m for m in pages if m['url']=='/music.html')
    assert fixture['url'] in render_page(music,[fixture],tax)
    assert fixture['url'] not in render_page(music,[dict(fixture,draft=True)],tax)
    rendered=finalize(new_post(fixture,tax),fixture['url'],nav,fixture,tax)
    assert '<strong>formatting</strong>' in rendered and '/tags/'+tag+'.html' in rendered
    for m in entries:
        if m.get('outputs'):
            o=m['outputs'][0];source=json.loads((ROOT/o['source']).read_text())
            changed='A changed paragraph with **new words**.'
            result=fill((ROOT/o['template']).read_text(),post_values(dict(m,title='Edited title'),tax,original_or_md(changed,source)))
            assert 'Edited title' in result and '<strong>new words</strong>' in result
            break
    # Menu order/labels must affect generated HTML and the browser navigation source.
    changednav={'main':[{'label':'Music renamed','href':'/music.html','enabled':True}],'footer':[]}
    result=soup(finalize(rendered,fixture['url'],changednav,fixture,tax))
    assert result.select_one('.nav-scroll').get_text(strip=True)=='Music renamed'
    if errors:
        print('\n'.join(errors[:100]));raise SystemExit(str(len(errors))+' preservation failures')
    print(json.dumps({'verified_article_urls':len(baseline),'verified_titles_bodies_links_images':True,'draft_and_taxonomy_selection':True,'music_automatic_listing':True,'article_edit_rendering':True,'global_navigation_editing':True,'pages':len(pages)}))

if __name__=='__main__':main()
