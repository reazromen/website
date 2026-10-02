<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>Home Server — Living Infrastructure Notebook | Reaz Romen</title>
<meta content="A living engineering notebook documenting how an old Mac mini evolved into a private infrastructure platform for networking, observability, device infrastructure, sensing, environmental data and telephony R&amp;D." name="description"/>
<meta content="light dark" name="color-scheme"/>
<link href="https://reazromen.com/homeserver/" rel="canonical"/>
<style>
    :root{--bg:#070a08;--panel:#0b100d;--text:#edf5ef;--soft:#aab8ae;--muted:#748179;--line:#1d2821;--line2:#2b3a30;--accent:#91f3a7}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 16% 0%,rgba(73,157,92,.11),transparent 34rem),linear-gradient(rgba(145,243,167,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(145,243,167,.025) 1px,transparent 1px),var(--bg);background-size:auto,72px 72px,72px 72px,auto;color:var(--text);font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    a{color:inherit;text-decoration:none}a:hover{color:var(--accent)}.shell{width:min(1180px,calc(100% - 44px));margin:0 auto}.mono,.kicker{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;text-transform:uppercase;letter-spacing:.11em;font-size:.68rem;font-weight:800}.kicker{color:var(--accent)}
    header{display:flex;align-items:center;justify-content:space-between;gap:28px;padding:22px 0;border-bottom:1px solid var(--line2)}.brand{display:flex;align-items:center;gap:12px}.mark{width:34px;height:34px;display:grid;place-items:center;border:1px solid #4a6251;color:var(--accent);font:850 .72rem ui-monospace,monospace}.brandcopy{display:grid;gap:2px}.brandcopy b{font-size:.94rem}.brandcopy span{color:var(--muted);font-size:.72rem}.nav{display:flex;gap:18px;flex-wrap:wrap;color:var(--soft);font-size:.8rem;font-weight:700}.nav a[aria-current="page"]{color:var(--accent)}
    .hero{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(300px,.55fr);gap:5rem;align-items:end;padding:6.2rem 0 4.5rem;border-bottom:1px solid var(--line2)}h1{max-width:900px;margin:.9rem 0 1.2rem;font-size:clamp(3.7rem,7.4vw,7rem);line-height:.9;letter-spacing:-.065em}.lede{max-width:790px;color:#c9d5cc;font-size:clamp(1.25rem,2.2vw,1.9rem);line-height:1.3;letter-spacing:-.03em}.hero p.note{max-width:760px;margin-top:1.4rem;color:var(--muted);line-height:1.68}
    .status{border-top:2px solid var(--accent);padding-top:1rem}.status h2{font-size:1.7rem;line-height:1.08;letter-spacing:-.035em;margin:.35rem 0 1rem}.status dl{margin:0}.status div{display:grid;grid-template-columns:92px 1fr;gap:12px;padding:.8rem 0;border-top:1px solid var(--line)}dt{color:var(--muted);font:800 .65rem ui-monospace,monospace;text-transform:uppercase;letter-spacing:.08em}dd{margin:0;color:var(--soft);font-size:.86rem;line-height:1.45}
    .section{padding:4.6rem 0;border-bottom:1px solid var(--line2)}.section-head{display:flex;align-items:end;justify-content:space-between;gap:24px;margin-bottom:1.8rem}.section h2{margin:.35rem 0 0;font-size:clamp(2.4rem,5vw,4.8rem);line-height:.94;letter-spacing:-.055em}.section-intro{max-width:830px;color:var(--soft);line-height:1.7}
    .why{display:grid;grid-template-columns:.7fr 1.3fr;gap:4rem}.why blockquote{margin:0;padding:1.2rem 0 1.2rem 1.3rem;border-left:3px solid var(--accent);font-size:clamp(1.45rem,3vw,2.4rem);line-height:1.2;letter-spacing:-.035em}.why p{color:var(--soft);line-height:1.72}
    .timeline{border-top:1px solid var(--line2)}.step{display:grid;grid-template-columns:64px 190px 1fr;gap:1.4rem;padding:1.2rem 0;border-bottom:1px solid var(--line)}.step span{color:var(--accent)}.step b{font-size:1rem}.step p{margin:0;color:var(--muted);line-height:1.6}
    .arch{display:grid;grid-template-columns:1fr 1.2fr 1fr;gap:14px;align-items:stretch}.node{border:1px solid #314337;background:#0a0f0c;padding:1.2rem;min-height:118px}.node.core{border-color:#70c982;box-shadow:inset 0 0 0 1px rgba(145,243,167,.08)}.node b{display:block;margin-bottom:.5rem;font-size:1.02rem}.node p{margin:0;color:var(--muted);font-size:.85rem;line-height:1.5}.node .mono{display:block;color:var(--accent);margin-bottom:.75rem}
    .threads{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-top:1px solid var(--line2)}.thread{padding:1.5rem 1.6rem 1.5rem 0;border-bottom:1px solid var(--line)}.thread:nth-child(odd){border-right:1px solid var(--line)}.thread:nth-child(even){padding-left:1.6rem}.thread h3{margin:.45rem 0 .7rem;font-size:1.4rem;letter-spacing:-.035em}.thread p{margin:0;color:var(--muted);line-height:1.62}.state{display:inline-flex;border:1px solid #38503f;padding:.25rem .42rem;color:var(--accent);font:800 .61rem ui-monospace,monospace;text-transform:uppercase;letter-spacing:.08em}
    .domains{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line2);border:1px solid var(--line2)}.domain{background:var(--bg);padding:1.35rem;min-height:175px}.domain h3{margin:.8rem 0 .55rem;font-size:1.22rem;letter-spacing:-.03em}.domain p{margin:0;color:var(--muted);font-size:.86rem;line-height:1.55}.tags{display:flex;gap:.45rem;flex-wrap:wrap;margin-top:1rem}.tags span{border-bottom:1px solid var(--line2);color:#9cab9f;font:700 .63rem ui-monospace,monospace}
    .log{border-top:1px solid var(--line2)}.logrow{display:grid;grid-template-columns:130px 1fr;gap:1.5rem;padding:1.1rem 0;border-bottom:1px solid var(--line)}.logrow time{color:var(--accent);font:800 .67rem ui-monospace,monospace;text-transform:uppercase}.logrow p{margin:0;color:var(--soft);line-height:1.6}.principle{margin-top:2rem;padding:1.5rem 1.7rem;border:1px solid #32463a;background:#0a0f0c;font-size:clamp(1.2rem,2.4vw,1.8rem);line-height:1.45;letter-spacing:-.025em}
    .next{display:grid;grid-template-columns:1fr 1fr;gap:3rem}.next ul{margin:0;padding:0;list-style:none}.next li{display:grid;grid-template-columns:34px 1fr;gap:.7rem;padding:.85rem 0;border-top:1px solid var(--line);color:var(--soft);line-height:1.5}.next li span{color:var(--accent);font:800 .65rem ui-monospace,monospace}.callout{border-top:2px solid var(--accent);padding-top:1rem}.callout p{color:var(--muted);line-height:1.65}.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:1.4rem}.button{display:inline-flex;min-height:40px;align-items:center;border:1px solid #435648;padding:0 13px;font-size:.78rem;font-weight:800}.button.primary{background:var(--accent);border-color:var(--accent);color:#071008}
    footer{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;padding:2rem 0 3rem;color:var(--muted);font-size:.78rem}
    @media(max-width:900px){.shell{width:min(100% - 28px,760px)}header{align-items:flex-start;flex-direction:column}.hero,.why,.next{grid-template-columns:1fr;gap:2.4rem}.hero{padding:4.3rem 0 3.3rem}.step{grid-template-columns:44px 1fr}.step p{grid-column:2}.arch,.domains{grid-template-columns:1fr}.threads{grid-template-columns:1fr}.thread,.thread:nth-child(odd),.thread:nth-child(even){padding:1.25rem 0;border-right:0}.logrow{grid-template-columns:1fr;gap:.4rem}}
  </style>
<link href="/assets/site.css" rel="stylesheet"/>
<link href="/assets/sitewide-v2.css" rel="stylesheet"/>
<link href="/assets/phase1.css" rel="stylesheet"/><link href="/feed.xml" rel="alternate" title="Reaz Romen — Writing" type="application/rss+xml"/><link href="/atom.xml" rel="alternate" title="Reaz Romen — Writing" type="application/atom+xml"/><link href="/assets/phase2.css" rel="stylesheet"/><link href="/assets/responsive-v3.css" rel="stylesheet"/></head>
<body class="rr-themed">
<a class="skip-link" href="#rr-main">Skip to content</a>
<header class="site-header rr-global-header"><div class="site-header-inner"><a aria-label="Reaz Romen home" class="brand" href="/">RR</a><nav aria-label="Main navigation" class="nav"><div class="nav-scroll"><a href="/portfolio.html">Work</a><a href="/perspectives.html">Perspectives</a><a href="/music.html">Music</a><a href="/bangla.html" lang="bn">বাংলা</a><a href="/about.html">About</a><a href="/systems.html">Stack</a></div><div class="nav-actions"><button aria-label="Search and quick navigation" class="icon-link search-action" data-open-command="" title="Search (Ctrl/⌘ K)" type="button"><svg aria-hidden="true" class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-4-4"></path></svg></button><a aria-label="GitHub" class="icon-link github-action" href="https://github.com/reazromen" rel="noopener" target="_blank"><svg aria-hidden="true" class="icon icon-fill" viewBox="0 0 24 24"><path d="M12 .7a11.3 11.3 0 0 0-3.57 22.03c.57.1.78-.25.78-.55v-2.18c-3.18.69-3.85-1.35-3.85-1.35-.52-1.32-1.27-1.67-1.27-1.67-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.75 2.68 1.25 3.33.95.1-.74.4-1.25.73-1.54-2.54-.29-5.21-1.27-5.21-5.65 0-1.25.45-2.27 1.18-3.07-.12-.29-.51-1.46.11-3.03 0 0 .96-.31 3.15 1.17A10.9 10.9 0 0 1 12 5.9c.98 0 1.96.13 2.87.39 2.19-1.48 3.15-1.17 3.15-1.17.62 1.57.23 2.74.11 3.03.74.8 1.18 1.82 1.18 3.07 0 4.39-2.68 5.35-5.23 5.64.41.36.78 1.06.78 2.14v3.18c0 .3.2.66.79.55A11.3 11.3 0 0 0 12 .7Z"></path></svg></a><button aria-label="Toggle color scheme" class="theme-toggle" onclick="toggleTheme()" type="button"><svg aria-hidden="true" class="icon" data-theme-icon="moon" viewBox="0 0 24 24"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3 6.5 6.5 0 0 0 21 12.8Z"></path></svg><svg aria-hidden="true" class="icon" data-theme-icon="sun" hidden="" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"></path></svg></button></div></nav></div></header>
<div class="shell">
<header>
<a class="brand" href="/"><span class="mark">RR</span><span class="brandcopy"><b>Reaz Romen</b><span>Systems · Embedded · Voice · Infrastructure</span></span></a>
<nav aria-label="Main navigation" class="nav"><a href="/portfolio">Portfolio</a><a href="/services">Services</a><a href="/about">About</a><a href="/writing">Writing</a><a href="/systems">Systems</a><a href="/archive">Archive</a><a aria-current="page" href="/homeserver/">Home Server</a></nav>
</header>
<main id="rr-main">
<section class="hero">
<div>
<p class="kicker">{{RR_BLOCK0}}</p>
<h1>{{RR_BLOCK1}}</h1>
<p class="lede">{{RR_BLOCK2}}</p>
<p class="note">{{RR_BLOCK3}}</p>
<div class="actions"><a class="button primary" href="{{RR_LINK0}}">Current work</a><a class="button" href="{{RR_LINK1}}">Evolution</a><a class="button" href="{{RR_LINK2}}">Change log</a></div>
</div>
<aside class="status">
<p class="kicker">{{RR_BLOCK4}}</p><h2>{{RR_BLOCK5}}</h2>
<dl>
<div><dt>{{RR_BLOCK6}}</dt><dd>{{RR_BLOCK7}}</dd></div>
<div><dt>{{RR_BLOCK8}}</dt><dd>{{RR_BLOCK9}}</dd></div>
<div><dt>{{RR_BLOCK10}}</dt><dd>{{RR_BLOCK11}}</dd></div>
<div><dt>{{RR_BLOCK12}}</dt><dd>{{RR_BLOCK13}}</dd></div>
</dl>
</aside>
</section>
<section class="section why">
<div><p class="kicker">{{RR_BLOCK14}}</p><blockquote>Every useful layer was added because the previous layer eventually became insufficient.</blockquote></div>
<div><p>{{RR_BLOCK15}}</p><p style="margin-top:1rem">{{RR_BLOCK16}}</p></div>
</section>
<section class="section" id="evolution">
<div class="section-head"><div><p class="kicker">{{RR_BLOCK17}}</p><h2>{{RR_BLOCK18}}</h2></div><span class="mono">{{RR_BLOCK76}}</span></div>
<div class="timeline">
<div class="step"><span class="mono">{{RR_BLOCK77}}</span><b>Ubuntu + Docker</b><p>{{RR_BLOCK19}}</p></div>
<div class="step"><span class="mono">{{RR_BLOCK78}}</span><b>Network recovery</b><p>{{RR_BLOCK20}}</p></div>
<div class="step"><span class="mono">{{RR_BLOCK79}}</span><b>Private + public access</b><p>{{RR_BLOCK21}}</p></div>
<div class="step"><span class="mono">{{RR_BLOCK80}}</span><b>Multi-machine compute</b><p>{{RR_BLOCK22}}</p></div>
<div class="step"><span class="mono">{{RR_BLOCK81}}</span><b>Observability</b><p>{{RR_BLOCK23}}</p></div>
<div class="step"><span class="mono">{{RR_BLOCK82}}</span><b>Control plane</b><p>{{RR_BLOCK24}}</p></div>
</div>
</section>
<section class="section">
<div class="section-head"><div><p class="kicker">{{RR_BLOCK25}}</p><h2>{{RR_BLOCK26}}</h2></div></div>
<div class="arch">
<div class="node"><span class="mono">{{RR_BLOCK83}}</span><b>Internet + private network</b><p>{{RR_BLOCK27}}</p></div>
<div class="node core"><span class="mono">{{RR_BLOCK84}}</span><b>hserver</b><p>{{RR_BLOCK28}}</p></div>
<div class="node"><span class="mono">{{RR_BLOCK85}}</span><b>Desktop + laptop</b><p>{{RR_BLOCK29}}</p></div>
<div class="node"><span class="mono">{{RR_BLOCK86}}</span><b>Metrics + flows</b><p>{{RR_BLOCK30}}</p></div>
<div class="node"><span class="mono">{{RR_BLOCK87}}</span><b>ESP32 + Android collectors</b><p>{{RR_BLOCK31}}</p></div>
<div class="node"><span class="mono">{{RR_BLOCK88}}</span><b>Voice + environment + sensing</b><p>{{RR_BLOCK32}}</p></div>
</div>
</section>
<section class="section" id="current">
<div class="section-head"><div><p class="kicker">{{RR_BLOCK33}}</p><h2>{{RR_BLOCK34}}</h2></div><span class="mono">{{RR_BLOCK89}}</span></div>
<div class="threads">
<article class="thread"><span class="state">{{RR_BLOCK90}}</span><h3>{{RR_BLOCK35}}</h3><p>{{RR_BLOCK36}}</p></article>
<article class="thread"><span class="state">{{RR_BLOCK91}}</span><h3>{{RR_BLOCK37}}</h3><p>{{RR_BLOCK38}}</p></article>
<article class="thread"><span class="state">{{RR_BLOCK92}}</span><h3>{{RR_BLOCK39}}</h3><p>{{RR_BLOCK40}}</p></article>
<article class="thread"><span class="state">{{RR_BLOCK93}}</span><h3>{{RR_BLOCK41}}</h3><p>{{RR_BLOCK42}}</p></article>
<article class="thread"><span class="state">{{RR_BLOCK94}}</span><h3>{{RR_BLOCK43}}</h3><p>{{RR_BLOCK44}}</p></article>
<article class="thread"><span class="state">{{RR_BLOCK95}}</span><h3>{{RR_BLOCK45}}</h3><p>{{RR_BLOCK46}}</p></article>
</div>
</section>
<section class="section">
<div class="section-head"><div><p class="kicker">{{RR_BLOCK47}}</p><h2>{{RR_BLOCK48}}</h2></div></div>
<div class="domains">
<article class="domain"><span class="mono">{{RR_BLOCK96}}</span><h3>{{RR_BLOCK49}}</h3><p>{{RR_BLOCK50}}</p><div class="tags"><span>{{RR_BLOCK97}}</span><span>{{RR_BLOCK98}}</span><span>{{RR_BLOCK99}}</span><span>{{RR_BLOCK100}}</span></div></article>
<article class="domain"><span class="mono">{{RR_BLOCK101}}</span><h3>{{RR_BLOCK51}}</h3><p>{{RR_BLOCK52}}</p><div class="tags"><span>{{RR_BLOCK102}}</span><span>{{RR_BLOCK103}}</span><span>{{RR_BLOCK104}}</span></div></article>
<article class="domain"><span class="mono">{{RR_BLOCK105}}</span><h3>{{RR_BLOCK53}}</h3><p>{{RR_BLOCK54}}</p><div class="tags"><span>{{RR_BLOCK106}}</span><span>{{RR_BLOCK107}}</span><span>{{RR_BLOCK108}}</span></div></article>
<article class="domain"><span class="mono">{{RR_BLOCK109}}</span><h3>{{RR_BLOCK55}}</h3><p>{{RR_BLOCK56}}</p><div class="tags"><span>{{RR_BLOCK110}}</span><span>{{RR_BLOCK111}}</span><span>{{RR_BLOCK112}}</span></div></article>
<article class="domain"><span class="mono">{{RR_BLOCK113}}</span><h3>{{RR_BLOCK57}}</h3><p>{{RR_BLOCK58}}</p><div class="tags"><span>{{RR_BLOCK114}}</span><span>{{RR_BLOCK115}}</span><span>{{RR_BLOCK116}}</span></div></article>
<article class="domain"><span class="mono">{{RR_BLOCK117}}</span><h3>{{RR_BLOCK59}}</h3><p>{{RR_BLOCK60}}</p><div class="tags"><span>{{RR_BLOCK118}}</span><span>{{RR_BLOCK119}}</span><span>{{RR_BLOCK120}}</span><span>{{RR_BLOCK121}}</span></div></article>
</div>
<div class="principle">The same pattern keeps repeating: source → collector → storage → query → visualization → alert or action.</div>
</section>
<section class="section" id="changelog">
<div class="section-head"><div><p class="kicker">{{RR_BLOCK61}}</p><h2>{{RR_BLOCK62}}</h2></div></div>
<div class="log">
<div class="logrow"><time>Sep 2026</time><p>{{RR_BLOCK63}}</p></div>
<div class="logrow"><time>Sep 2026</time><p>{{RR_BLOCK64}}</p></div>
<div class="logrow"><time>Sep 2026</time><p>{{RR_BLOCK65}}</p></div>
<div class="logrow"><time>Sep 2026</time><p>{{RR_BLOCK66}}</p></div>
<div class="logrow"><time>Earlier</time><p>{{RR_BLOCK67}}</p></div>
</div>
</section>
<section class="section next">
<div>
<p class="kicker">{{RR_BLOCK68}}</p>
<ul><li>{{RR_BLOCK69}}</li><li>{{RR_BLOCK70}}</li><li>{{RR_BLOCK71}}</li><li>{{RR_BLOCK72}}</li></ul>
</div>
<aside class="callout"><p class="kicker">{{RR_BLOCK73}}</p><h2 style="font-size:2.1rem">{{RR_BLOCK74}}</h2><p>{{RR_BLOCK75}}</p><div class="actions"><a class="button primary" href="{{RR_LINK3}}">Portfolio</a><a class="button" href="{{RR_LINK4}}">Systems</a><a class="button" href="{{RR_LINK5}}">Field notes</a></div></aside>
</section>
</main>
<footer><span>Reaz Romen — independent systems engineer.</span><span>Home Server / living infrastructure notebook · updated 25 Sep 2026</span></footer>
</div>
<script src="/assets/site.js"></script><script src="/assets/sitewide.js"></script>
<dialog aria-label="Search and quick navigation" class="command-palette" data-pagefind-ignore="" id="command-palette">
<div class="command-shell">
<div class="command-input-row"><svg aria-hidden="true" class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-4-4"></path></svg><input aria-label="Search site" autocomplete="off" id="command-input" placeholder="Search writing, work, topics…" type="search"/><button aria-label="Close" class="command-close" data-close-command="" type="button"><svg aria-hidden="true" class="icon" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"></path></svg></button></div>
<div class="command-hint"><span>Quick navigation</span><kbd>Esc</kbd></div>
<nav aria-label="Quick navigation" class="command-shortcuts">
<a href="/portfolio.html">Work <span>Projects and systems</span></a>
<a href="/writing.html">Writing <span>Articles and engineering notes</span></a>
<a href="/domains/">Domains <span>Browse engineering areas</span></a>
<a href="/now.html">Now <span>Current public focus</span></a>
<a href="/systems.html">Stack <span>Tools by engineering layer</span></a>
<a href="/about.html">About <span>Background and approach</span></a>
</nav>
<div aria-live="polite" class="command-results" id="command-results"></div>
<div class="command-footer"><span>Search</span><kbd>⌘/Ctrl K</kbd><span>Open result</span><kbd>Enter</kbd></div>
</div></dialog><script src="/assets/phase1.js"></script><div class="context-preview" data-pagefind-ignore="" hidden="" id="context-preview" role="tooltip"></div><script src="/assets/phase2.js"></script><script src="/assets/responsive-v3.js"></script></body>
</html>