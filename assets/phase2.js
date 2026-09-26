(()=> {
  const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
  document.querySelectorAll('.network-diagram').forEach(diagram=>{
    const nodes=[...diagram.querySelectorAll('.network-node')];
    const arrows=[...diagram.querySelectorAll('.network-arrow')];
    const clear=diagram.previousElementSibling?.querySelector?.('.trace-clear');
    let locked=0;
    const apply=idx=>{
      diagram.classList.toggle('trace-active',idx>0);
      nodes.forEach((n,i)=>{
        n.classList.toggle('is-path',idx>0&&i<idx);
        n.classList.toggle('is-focus',idx>0&&i===idx-1);
        n.setAttribute('aria-pressed',locked===i+1?'true':'false');
      });
      arrows.forEach((a,i)=>a.classList.toggle('is-path',idx>0&&i<idx-1));
      if(clear)clear.hidden=!locked;
    };
    const preview=i=>{if(!locked)apply(i)};
    const restore=()=>apply(locked);
    nodes.forEach((n,i)=>{
      const idx=i+1;
      if(fine)n.addEventListener('pointerenter',()=>preview(idx));
      if(fine)n.addEventListener('pointerleave',restore);
      n.addEventListener('focus',()=>preview(idx));
      n.addEventListener('blur',restore);
      n.addEventListener('click',()=>{
        locked=locked===idx?0:idx;
        apply(locked);
      });
      n.addEventListener('keydown',e=>{
        if(e.key==='Enter'||e.key===' '){e.preventDefault();n.click()}
      });
    });
    clear?.addEventListener('click',()=>{locked=0;apply(0)});
  });

  const tip=document.getElementById('context-preview');
  let indexPromise=null,activeAnchor=null;
  const loadIndex=()=>indexPromise||(indexPromise=fetch('/assets/context-index.json',{cache:'force-cache'}).then(r=>r.ok?r.json():{}).catch(()=>({})));
  const hide=()=>{if(!tip)return;tip.hidden=true;activeAnchor=null};
  const position=a=>{
    if(!tip||!a)return;
    const r=a.getBoundingClientRect(), pad=12;
    tip.hidden=false;
    const box=tip.getBoundingClientRect();
    let left=Math.min(Math.max(pad,r.left),innerWidth-box.width-pad);
    let top=r.bottom+8;
    if(top+box.height>innerHeight-pad)top=Math.max(pad,r.top-box.height-8);
    tip.style.left=left+'px';
    tip.style.top=top+'px';
  };
  const show=async a=>{
    if(!fine||!tip||!a)return;
    let u;
    try{u=new URL(a.getAttribute('href'),location.href)}catch{return}
    if(u.origin!==location.origin||u.hash&&u.pathname===location.pathname)return;
    const data=(await loadIndex())[u.pathname];
    if(!data)return;
    activeAnchor=a;
    tip.replaceChildren();
    const meta=document.createElement('div');meta.className='context-meta';
    [data.type,data.domain].filter(Boolean).forEach(v=>{const s=document.createElement('span');s.textContent=v;meta.append(s)});
    const strong=document.createElement('strong');strong.textContent=data.title||'';
    const p=document.createElement('p');p.textContent=data.description||'';
    tip.append(meta,strong,p);
    position(a);
  };
  if(fine&&tip){
    document.addEventListener('pointerover',e=>{
      const a=e.target.closest?.('main a[href]');
      if(a&&!a.closest('.article-toc,.command-palette'))show(a);
    });
    document.addEventListener('pointerout',e=>{
      const a=e.target.closest?.('main a[href]');
      if(a===activeAnchor&&!a.contains(e.relatedTarget))hide();
    });
    document.addEventListener('focusin',e=>{
      const a=e.target.closest?.('main a[href]');
      if(a&&!a.closest('.article-toc,.command-palette'))show(a);
    });
    document.addEventListener('focusout',e=>{
      if(e.target===activeAnchor)hide();
    });
    addEventListener('scroll',hide,{passive:true});
    addEventListener('resize',()=>{if(activeAnchor)position(activeAnchor)});
  }
})();