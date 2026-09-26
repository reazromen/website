(()=> {
  let pfPromise=null, activeQuery=0;
  const loadPagefind=()=>pfPromise||(pfPromise=import('/pagefind/pagefind.js').then(async m=>{await m.init();return m}));
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const render=async(q,target,filters={},limit=12)=>{
    const token=++activeQuery;
    if(!target)return;
    const term=String(q??'').trim();
    const clean={};Object.entries(filters).forEach(([k,v])=>{if(v)clean[k]=v});
    if(!term&&!Object.keys(clean).length){target.innerHTML='<p class="command-empty">Type at least two characters.</p>';return}
    if(term&&term.length<2){target.innerHTML='<p class="command-empty">Type at least two characters.</p>';return}
    target.innerHTML='<p class="command-empty">Searching…</p>';
    try{
      const pf=await loadPagefind();
      const found=await pf.search(term||null,Object.keys(clean).length?{filters:clean}:undefined);
      const max=limit===Infinity?found.results.length:Math.min(limit,found.results.length);
      const rows=await Promise.all(found.results.slice(0,max).map(r=>r.data()));
      if(token!==activeQuery)return;
      if(!rows.length){target.innerHTML='<p class="command-empty">No matching pages.</p>';return}
      target.innerHTML=rows.map(r=>{
        const title=r.meta?.title||r.url;
        const meta=[r.meta?.type,r.meta?.format,r.meta?.domain].filter(Boolean).join(' · ');
        return '<a class="command-result" href="'+esc(r.url)+'"><span><strong>'+esc(title)+'</strong><small>'+String(r.excerpt||'').replace(/<(?!\/?mark\b)[^>]*>/g,'')+'</small></span><span class="command-result-meta">'+esc(meta)+'</span></a>';
      }).join('');
    }catch(e){target.innerHTML='<p class="command-empty">Search index is unavailable in this preview.</p>'}
  };
  const dialog=document.getElementById('command-palette'), input=document.getElementById('command-input'), results=document.getElementById('command-results');
  const open=()=>{if(!dialog)return;dialog.showModal();setTimeout(()=>input?.focus(),0)};
  document.querySelectorAll('[data-open-command]').forEach(b=>b.addEventListener('click',open));
  document.querySelectorAll('[data-close-command]').forEach(b=>b.addEventListener('click',()=>dialog?.close()));
  dialog?.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
  document.addEventListener('keydown',e=>{
    if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();dialog?.open?dialog.close():open()}
    if(e.key==='Escape'&&dialog?.open)dialog.close();
  });
  let timer;
  input?.addEventListener('input',()=>{
    clearTimeout(timer);
    const shortcuts=dialog.querySelector('.command-shortcuts');
    const q=input.value.trim();
    shortcuts.hidden=q.length>=2;
    if(q.length<2){results.innerHTML='';return}
    timer=setTimeout(()=>render(q,results),120);
  });

  document.querySelectorAll('.tags span').forEach(span=>{
    if(span.querySelector('a'))return;
    const tag=span.textContent.trim();
    if(!tag)return;
    const a=document.createElement('a');
    a.href='/search.html?topic='+encodeURIComponent(tag);
    a.textContent=tag;
    a.setAttribute('aria-label','Browse articles tagged '+tag);
    a.style.cssText='color:inherit;text-decoration:none;display:inline-flex;align-items:center';
    span.textContent='';
    span.append(a);
  });

  const siteInput=document.getElementById('site-search-input');
  const siteTarget=document.getElementById('site-search-results');
  const typeSel=document.getElementById('site-search-type');
  const domainSel=document.getElementById('site-search-domain');
  const topic=(new URLSearchParams(location.search).get('topic')||'').trim();
  const siteRun=()=>render(siteInput?.value||'',siteTarget,{type:typeSel?.value||'',domain:domainSel?.value||'',topic},topic?Infinity:12);
  siteInput?.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(siteRun,120)});
  typeSel?.addEventListener('change',siteRun);
  domainSel?.addEventListener('change',siteRun);
  if(topic&&siteTarget){
    const context=document.createElement('p');
    context.className='command-empty';
    context.innerHTML='Tag: <strong>'+esc(topic)+'</strong> · <a href="/search.html">Clear tag</a>';
    siteTarget.before(context);
    if(siteInput)siteInput.placeholder='Search within '+topic+'…';
    siteRun();
  }

  document.querySelectorAll('.heading-anchor').forEach(a=>a.addEventListener('click',()=>{
    const u=location.origin+location.pathname+a.getAttribute('href');
    navigator.clipboard?.writeText(u).catch(()=>{});
  }));
  const tocLinks=[...document.querySelectorAll('.article-toc a[href^="#"]')];
  if(tocLinks.length&&'IntersectionObserver'in window){
    const byId=new Map(tocLinks.map(a=>[a.getAttribute('href').slice(1),a]));
    const io=new IntersectionObserver(entries=>{
      const visible=entries.filter(x=>x.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top)[0];
      if(!visible)return;
      tocLinks.forEach(a=>a.removeAttribute('aria-current'));
      byId.get(visible.target.id)?.setAttribute('aria-current','true');
    },{rootMargin:'-15% 0px -70% 0px',threshold:0});
    byId.forEach((_,id)=>{const el=document.getElementById(id);if(el)io.observe(el)});
  }
})();