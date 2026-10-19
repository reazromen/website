(() => {
  'use strict';
  const article = document.querySelector('main article.article');
  if (!article) return;
  const titleEl = article.querySelector('h1');
  const ledeEl = article.querySelector('.lede');
  const bodyEl = article.querySelector('.prose');
  if (!titleEl || !ledeEl || !bodyEl || !article.querySelector('.article-meta')) return;

  const articleId = location.pathname;
  const apiBase = 'https://dev.reazromen.com/api/article-versions';
  const original = { title: titleEl.textContent.trim(), lede: ledeEl ? ledeEl.textContent.trim() : '', body: bodyEl.innerText.trim() };
  let versions = [];
  let selectedId = null;
  const css = document.createElement('style');
  css.textContent = `
  #avp-launch{position:fixed;right:18px;bottom:18px;z-index:9998;border:1px solid #888;background:#171717;color:#fff;border-radius:999px;padding:12px 17px;font:600 14px/1.2 system-ui;box-shadow:0 8px 30px #0003;cursor:pointer}
  #avp-panel{position:fixed;inset:0 0 0 auto;width:min(540px,100vw);z-index:9999;background:Canvas;color:CanvasText;border-left:1px solid #8888;box-shadow:-12px 0 38px #0002;display:none;overflow:auto;padding:20px;box-sizing:border-box;font:14px/1.45 system-ui}
  #avp-panel *{box-sizing:border-box} #avp-panel h2{font-size:20px;margin:0 0 6px} #avp-panel label{display:block;font-weight:650;margin:14px 0 5px}
  #avp-panel input,#avp-panel textarea,#avp-panel select{display:block;width:100%;padding:10px;border:1px solid #8888;border-radius:8px;background:Canvas;color:CanvasText;font:14px/1.45 system-ui}
  #avp-panel textarea{min-height:180px;resize:vertical} #avp-panel .avp-lede{min-height:72px} #avp-panel .avp-actions{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}
  #avp-panel button{padding:9px 12px;border:1px solid #8888;border-radius:8px;background:Canvas;color:CanvasText;font:600 13px system-ui;cursor:pointer} #avp-panel button.avp-primary{background:#222;color:#fff;border-color:#222}
  #avp-panel .avp-note{padding:10px;border-radius:8px;background:color-mix(in srgb,CanvasText 7%,Canvas);font-size:12px} #avp-panel .avp-status{min-height:20px;font-weight:600}
  #avp-panel .avp-diff{white-space:pre-wrap;overflow-wrap:anywhere;border:1px solid #8885;border-radius:8px;padding:10px;max-height:280px;overflow:auto;font:12px/1.5 ui-monospace,monospace}
  #avp-panel .avp-summary{border:1px solid #8885;border-radius:8px;padding:12px;margin:12px 0} #avp-panel .avp-summary h3{font-size:14px;margin:8px 0 4px} #avp-panel .avp-summary ul{padding-left:20px;margin:4px 0}
  @media(prefers-color-scheme:dark){#avp-launch{background:#eee;color:#111}#avp-panel button.avp-primary{background:#eee;color:#111;border-color:#eee}}
  `;
  document.head.appendChild(css);
  const launch = document.createElement('button'); launch.id='avp-launch'; launch.type='button'; launch.textContent='Article versions';
  const panel = document.createElement('aside'); panel.id='avp-panel'; panel.setAttribute('aria-label','Article version history');
  panel.innerHTML = `<div style="display:flex;justify-content:space-between;align-items:center;gap:12px"><h2>Article versions</h2><button type="button" data-avp="close" aria-label="Close panel">Close</button></div>
  <p class="avp-note">Public editing is enabled. Saved revisions become the latest public article version immediately; there is no approval queue. AI only summarizes changes and never rewrites text.</p>
  <label for="avp-author">Attribution</label><input id="avp-author" value="Public contributor" readonly maxlength="120">
  <label for="avp-title">Article title</label><input id="avp-title" maxlength="500">
  <label for="avp-lede">Intro / lede</label><textarea id="avp-lede" class="avp-lede" maxlength="10000"></textarea>
  <label for="avp-body">Article text (separate paragraphs with a blank line)</label><textarea id="avp-body" maxlength="200000"></textarea>
  <div class="avp-actions"><button class="avp-primary" type="button" data-avp="save">Save as new version</button><button type="button" data-avp="reset">Reset editor</button></div>
  <label for="avp-history">Saved version history</label><select id="avp-history"></select>
  <div class="avp-actions"><button type="button" data-avp="view">Preview selected version</button><button type="button" data-avp="compare">Show change summary</button><button type="button" data-avp="refresh">Refresh history</button></div>
  <div id="avp-diff" class="avp-diff" hidden></div><p id="avp-status" class="avp-status" role="status"></p>
  <p class="avp-note">Each new revision is saved before AI summarization. If the free AI mesh fails, the version remains saved and the summary is marked failed; no summary is invented.</p>`;
  document.body.append(launch,panel);
  const $ = id => panel.querySelector('#'+id);
  const status = message => { $('avp-status').textContent=message; };
  const baseline = {id:0,version_number:0,title:original.title,lede:original.lede,body:original.body,author:'Published baseline',summary_status:'baseline',summary:null,created_at:null};
  const allVersions = () => versions.length ? versions : [baseline];
  const selected = () => allVersions().find(v=>String(v.id)===String($('avp-history').value)) || allVersions()[allVersions().length-1];
  const populate = v => { $('avp-title').value=v.title||''; $('avp-lede').value=v.lede||''; $('avp-body').value=v.body||''; };
  const renderHistory = () => {
    const sel=$('avp-history'); sel.replaceChildren();
    allVersions().forEach(v=>{const o=document.createElement('option');o.value=String(v.id);const date=v.created_at?new Date(v.created_at).toLocaleString():'not archived yet';o.textContent=v.version_number?`v${v.version_number} · ${v.author||'Anonymous'} · ${date}`:'Published baseline · current site version';sel.append(o);});
    sel.value=String(selectedId ?? allVersions()[allVersions().length-1].id);
    if(![...sel.options].some(o=>o.value===sel.value))sel.value=String(allVersions()[allVersions().length-1].id);
  };
  const apply = v => {
    titleEl.textContent=v.title||''; if(ledeEl){ledeEl.textContent=v.lede||'';ledeEl.hidden=!(v.lede||'');}
    bodyEl.replaceChildren(...String(v.body||'').split(/\n\s*\n/).filter(Boolean).map(t=>{const p=document.createElement('p');p.textContent=t;return p;}));
    selectedId=v.id;populate(v);renderHistory();status(`Previewing ${v.version_number?`v${v.version_number}`:'the published baseline'}. This version is displayed locally.`);
  };
  const refresh = async () => {
    status('Loading shared version history…');
    try {
      const response=await fetch(apiBase+'?article_id='+encodeURIComponent(articleId),{cache:'no-store',credentials:'omit'});
      if(!response.ok)throw new Error(`History API returned ${response.status}`);
      const data=await response.json(); versions=Array.isArray(data.versions)?data.versions:[];
      if(!versions.length)selectedId=0;else if(!versions.some(v=>v.id===selectedId))selectedId=versions[versions.length-1].id;
      renderHistory();
      if(versions.length){const latest=versions[versions.length-1];selectedId=latest.id;apply(latest);}else{populate(baseline);}
      status(versions.length?`Loaded ${versions.length} shared version(s); latest revision is live.`:'No revisions saved yet; the published article is the baseline.');
    } catch(err) { versions=[];selectedId=0;renderHistory();populate(baseline);status('Could not load shared history. Check the version service and try Refresh history.'); }
  };
  const renderSummary = v => {
    const out=$('avp-diff');out.replaceChildren();out.hidden=false;
    const add=(tag,text,parent=out)=>{const el=document.createElement(tag);el.textContent=text;parent.append(el);return el;};
    add('strong',`Version ${v.version_number} · ${v.summary_status}`);
    if(v.summary_status==='pending')add('p','The version is saved; its AI summary is still pending.');
    else if(v.summary_status==='failed')add('p','The version is saved, but the free AI mesh did not produce a valid summary. The original text is intact.');
    else if(v.summary){
      const box=add('div','');box.className='avp-summary';add('p',v.summary.summary||'No narrative summary returned.',box);
      for(const [key,label] of [['added','Added'],['removed','Removed'],['revised','Revised']]){const list=v.summary[key]||[];if(list.length){add('h3',label,box);const ul=add('ul','',box);list.forEach(item=>add('li',String(item),ul));}}
      add('p',`Main argument changed: ${v.summary.main_argument_changed?'Yes':'No / not clearly changed'}. ${v.summary.main_argument_note||''}`,box);
      if(v.summary_provider)add('small',`Generated through the free AI mesh (${v.summary_provider}).`,box);
    } else add('p','This is the initial baseline and has no change summary.');
    const prev=versions.find(x=>x.id===v.parent_version_id);
    if(prev){const old=[prev.title,prev.lede,prev.body].join('\n\n').split('\n');const now=[v.title,v.lede,v.body].join('\n\n').split('\n');const diff=[...old.map(x=>'- '+x),...now.map(x=>'+ '+x)].join('\n');add('h3','Full text snapshots are available from the version selector');add('p','Select a version and choose Preview selected version to read its full saved text.');}
  };
  const showPanel=()=>{panel.style.display='block';populate(allVersions().find(v=>v.id===selectedId)||allVersions()[allVersions().length-1]);renderHistory();};
  launch.addEventListener('click',showPanel);
  panel.addEventListener('click',async e=>{
    const action=e.target.closest('[data-avp]')?.dataset.avp;if(!action)return;
    if(action==='close'){panel.style.display='none';return;}
    if(action==='reset'){populate(allVersions().find(v=>v.id===selectedId)||allVersions()[allVersions().length-1]);status('Editor reset.');return;}
    if(action==='refresh'){await refresh();return;}
    if(action==='view'){apply(selected());return;}
    if(action==='compare'){renderSummary(selected());return;}
    if(action==='save'){
      const title=$('avp-title').value.trim(),body=$('avp-body').value.trim();if(!title||!body){status('Title and article text are required.');return;}
      const button=e.target.closest('button');button.disabled=true;status('Saving the immutable version, then requesting a free AI change summary…');
      try{
        const response=await fetch(apiBase,{method:'POST',credentials:'omit',headers:{'Content-Type':'application/json'},body:JSON.stringify({article_id:articleId,title,lede:$('avp-lede').value.trim(),body,author:$('avp-author').value.trim()||'Public contributor',baseline:versions.length?null:original})});
        const type=response.headers.get('content-type')||'';if(!type.includes('application/json'))throw new Error('The public version service returned an unexpected response. Please retry later.');
        const data=await response.json();if(!response.ok)throw new Error(data.detail||data.error||`Save failed (${response.status})`);
        await refresh();const saved=data.version;if(saved){selectedId=saved.id;renderHistory();apply(saved);renderSummary(saved);}
        status(data.created?`Published public v${saved.version_number}; summary status: ${saved.summary_status}.`:'No new version created because the content is unchanged.');
      }catch(err){status(err.message||'Could not save this version.');}
      finally{button.disabled=false;}
    }
  });
  renderHistory();populate(baseline);refresh();
})();

[executed on device: hserver (e3ce91f8-8d4c-413e-b14d-04ad4fe8d7e3)]