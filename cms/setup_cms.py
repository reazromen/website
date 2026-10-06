from cms_common import *

def field(name,widget='string',**kw):return dict({'name':name,'label':name.replace('_',' ').title(),'widget':widget},**kw)
def relation(name,collection,multiple=False):return field(name,'relation',collection=collection,search_fields=['title'],value_field='{{slug}}',display_fields=['title'],multiple=multiple,required=False)

def main():
    root=ROOT
    # Use an original article shell so site icons, keyboard search and footer remain available.
    import subprocess
    baseline=json.loads((CONTENT/'migration.json').read_text())['original_commit']
    raw=subprocess.check_output(['git','show',baseline+':posts/reviewed-job-catalog-infrastructure-code-for-operations.html'],cwd=ROOT,text=True)
    (ROOT/'cms/shell.tpl').write_text(raw)
    for p in (CONTENT/'pages').glob('*.yml'):
        m=yaml.safe_load(p.read_text());s=soup((ROOT/m['template']).read_text());sources=json.loads((ROOT/m['source']).read_text());main=s.find('main')
        if not main:continue
        links=[]
        # Headings and prose are existing blocks. Expose remaining card labels and links too.
        for n in main.find_all(['strong','span']):
            if n.find_parent(['p','li','h1','h2','h3','h4','h5','h6']) or n.find(['strong','span']) or '{{RR_' in str(n) or not n.get_text(strip=True):continue
            ident='BLOCK'+str(len(m['blocks']));b=md(inner(n));sources[ident]={'hash':digest(b),'html':inner(n),'inline':True};m['blocks'].append({'id':ident,'label':n.get_text(' ',strip=True)[:95],'body':b});slot(n,ident)
        for n in main.select('a[href]'):
            href=n['href']
            if '{{RR_' in href:continue
            ident='LINK'+str(len(links));absolute=route(href,m['url']) if not href.startswith(('#','mailto:','tel:')) else None
            if absolute and '#' in href:absolute+='#'+href.split('#',1)[1]
            if absolute and '?' in href:absolute+='?'+href.split('?',1)[1].split('#')[0]
            links.append({'id':ident,'label':n.get_text(' ',strip=True)[:90] or href,'url':absolute or href});n['href']='{{RR_'+ident+'}}'
        # Recent writing updates automatically while retaining the compact homepage list.
        if m['url']=='/index.html':
            h=main.find(id='recent-writing');container=h.parent.select_one('.index-list') if h else None
            if container:
                key='LIST'+str(len(m['lists']));m['lists'].append({'key':key,'filter':{'all':True,'limit':3,'featured_first':True},'style':'home'});slot(container,key)
        # Artist research archives retain their editorial distinction.
        if m['url'].startswith('/music/') and m['url']!='/music/index.html':
            for listing in m.get('lists',[]):listing['filter']['kind']='research'
        m['links']=links
        (ROOT/m['template']).write_text(html_string(s));(ROOT/m['source']).write_text(json.dumps(sources,ensure_ascii=False));write_yaml(p,m)
    common=[field('draft','boolean',default=True,required=False,hint='A draft is saved in Git but excluded from the public site. Turn this off to publish.'),field('title'),field('url',required=False,hint='Existing public URL. Keep it unchanged to preserve links. New posts can leave this empty.'),field('date','datetime',required=False,date_format='YYYY-MM-DD',time_format=False,format='YYYY-MM-DD'),field('read_time','number',value_type='int',min=1,default=6),field('excerpt','text',required=False),relation('topic','topics'),relation('tags','tags',True),field('featured','boolean',default=False,required=False),field('language','select',options=['en','bn'],default='en'),field('eyebrow',required=False),field('cover_image','image',required=False),field('cover_alt',required=False),field('outputs','hidden',required=False),field('body','markdown')]
    collections=[]
    for name,label in [('writing','Writing · Engineering archive'),('perspectives','Perspectives'),('music','Music'),('bangla','বাংলা')]:
        fields=list(common)
        if name=='music':fields=fields[:-1]+[field('artist',required=False),field('album',required=False),field('year',required=False),field('kind','select',options=[{'label':'Personal song note','value':'song'},{'label':'Album note','value':'album'},{'label':'Performance note','value':'performance'},{'label':'Research listening note','value':'research'}],default='song')]+fields[-1:]
        collections.append(dict(name=name,label=label,folder='content/'+name,create=True,delete=True,extension='md',format='frontmatter',slug='{{slug}}',summary='{{title}}',sortable_fields=['title','date'],view_filters=[{'label':'Drafts','field':'draft','pattern':True},{'label':'Published','field':'draft','pattern':False}],fields=fields))
    for name in ('topics','tags'):
        collections.append(dict(name=name,label=name.title(),folder='content/'+name,create=True,delete=True,extension='md',format='frontmatter',identifier_field='title',slug='{{slug}}',fields=[field('title'),field('id','hidden',required=False),field('description','text',required=False),field('aliases','list',required=False,hint='Optional old URLs that should redirect to this archive.'),field('body','markdown',required=False)]))
    collections.append(dict(name='pages',label='Pages',folder='content/pages',create=True,delete=True,extension='yml',format='yaml',slug='{{slug}}',summary='{{title}} · {{url}}',fields=[field('title'),field('url',hint='Public path ending in .html, such as /contact.html.'),field('browser_title',required=False),field('description','text',required=False),field('draft','boolean',default=False),field('body','markdown',required=False,hint='Main content for a new page. Existing designed pages use Content blocks below.'),field('blocks','list',label='Content blocks',required=False,allow_add=False,collapsed=True,summary='{{fields.label}}',fields=[field('id','hidden'),field('label'),field('body','markdown')]),field('links','list',required=False,allow_add=False,collapsed=True,summary='{{fields.label}}',fields=[field('id','hidden'),field('label'),field('url')]),field('template','hidden',required=False),field('source','hidden',required=False),field('lists','hidden',required=False)]))
    linkfields=[field('label'),field('href',hint='Use a site path such as /music.html, or a full https:// URL.'),field('enabled','boolean',default=True),field('lang',required=False)]
    collections.append(dict(name='site',label='Site settings',editor={'preview':False},files=[dict(name='navigation',label='Menus · header and footer',file='content/site/navigation.yml',fields=[field('main','list',label='Main menu · drag to reorder',fields=linkfields+[field('children','list',required=False,fields=linkfields)]),field('footer','list',label='Footer menu · drag to reorder',fields=linkfields)])]))
    config={'backend':{'name':'proxy','proxy_url':'https://reazromen.com/admin/api/v1','branch':'main'},'site_url':'https://reazromen.com','display_url':'https://reazromen.com','media_folder':'static/uploads','public_folder':'/static/uploads','publish_mode':'simple','collections':collections}
    write_yaml(ROOT/'cms/admin/config.yml',config)
    (ROOT/'cms/requirements.txt').write_text('beautifulsoup4==4.14.3\nMarkdown==3.10.2\nmarkdownify==1.2.2\nPyYAML==6.0.3\n')
    print('CMS configuration and page controls ready.')

if __name__=='__main__':main()
