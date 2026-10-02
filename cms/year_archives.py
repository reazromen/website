"""Chronological archives: preserve recorded publication dates; never backdate."""
from collections import defaultdict
from datetime import date
from pathlib import Path
import json


def render_archives(entries, outputs, nav, root, shell, finalize, esc):
    public = [item for item in entries if not item.get('draft')]
    by_year = defaultdict(list)
    invalid = []
    for item in public:
        value = str(item.get('date', ''))[:10]
        try:
            published = date.fromisoformat(value)
            by_year[published.year].append(item)
        except ValueError:
            by_year['undated'].append(item)
            invalid.append(item['url'])
    years = sorted(set(range(2017, 2027)) | {y for y in by_year if isinstance(y, int)}, reverse=True)
    def links():
        return '<nav class="archive-years" aria-label="Publication year">' + ''.join(
            '<a href="/archive/'+str(y)+'.html">'+str(y)+' <span>('+str(len(by_year[y]))+')</span></a>' for y in years
        ) + '<a href="/archive/undated.html">Undated ('+str(len(by_year['undated']))+')</a></nav>'
    def rows(items):
        return '<ul class="archive-rows">' + ''.join(
            '<li><time datetime="'+esc(str(item.get('date',''))[:10])+'">'+esc(str(item.get('date',''))[:10] or 'Undated')+
            '</time><a href="'+esc(item['url'])+'"'+(' lang="bn"' if item.get('language')=='bn' else '')+'>'+esc(item['title'])+
            '</a><span>'+esc(item['section'])+'</span></li>' for item in items
        ) + '</ul>'
    counts = {str(y): len(by_year[y]) for y in years}
    counts['undated'] = len(by_year['undated'])
    for y in years + ['undated']:
        items = sorted(by_year[y], key=lambda m:(str(m.get('date','')),m['url']), reverse=True)
        name = str(y) if y != 'undated' else 'Undated'
        intro = '<section class="page-head"><p class="eyebrow">WRITING ARCHIVE</p><h1>'+name+'</h1><p>'+str(len(items))+' published posts.</p></section>'
        empty = '<p>No posts have a recorded publication date in this year.</p>' if not items else ''
        body = intro + links() + empty + rows(items)
        outputs['/archive/'+str(y)+'.html'] = finalize(shell(name+' — Archive', body), '/archive/'+str(y)+'.html', nav)
    body = '<section class="page-head"><p class="eyebrow">WRITING ARCHIVE</p><h1>Archive</h1><p>Posts organized by their recorded publication dates, 2017–2026.</p><p>New writing is dated when published. Earlier years remain empty until dated original material is available.</p></section>'+links()
    for y in years:
        if by_year[y]:
            body += '<section><h2><a href="/archive/'+str(y)+'.html">'+str(y)+'</a></h2>'+rows(sorted(by_year[y],key=lambda m:(str(m.get('date','')),m['url']),reverse=True))+'</section>'
    if by_year['undated']:
        body += '<section><h2>Undated</h2>'+rows(by_year['undated'])+'</section>'
    outputs['/archive.html'] = finalize(shell('Archive',body),'/archive.html',nav)
    outputs['/archive/index.html'] = finalize(shell('Archive',body),'/archive/index.html',nav)
    (root/'cms/archive-date-audit.json').write_text(json.dumps({'basis':'Recorded publication date; no invented historical dates','years':counts,'undated_urls':invalid},ensure_ascii=False,indent=2)+'\n')

