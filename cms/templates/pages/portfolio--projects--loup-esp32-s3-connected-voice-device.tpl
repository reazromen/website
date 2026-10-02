<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<meta content="light dark" name="color-scheme"/>
<meta content="Custom ESP32-S3 voice device spanning codec bring-up, I2S audio, AEC, jitter/playout, SIP/RTP, e-paper UI, controls, provisioning and OTA." name="description"/>
<meta content="Reaz Romen" name="author"/>
<link href="../../about.html" rel="author"/>
<title>LOUP ESP32-S3 Connected Voice Device — Reaz Romen Portfolio</title>
<link href="../../static/css/site.css" rel="stylesheet"/>
<link href="/assets/site.css" rel="stylesheet"/>
<link href="/assets/sitewide-v2.css" rel="stylesheet"/>
<meta content="Work" data-pagefind-filter="type[content]"/><meta content="Embedded &amp; Devices" data-pagefind-filter="domain[content]"/><meta content="Embedded &amp; Devices" data-pagefind-meta="domain[content]"/><meta content="Work" data-pagefind-meta="type[content]"/><meta content="Project" data-pagefind-filter="format[content]"/><meta content="Project" data-pagefind-meta="format[content]"/><meta content="LOUP ESP32-S3 Connected Voice Device" data-pagefind-meta="title[content]"/><link href="/assets/phase1.css" rel="stylesheet"/><link href="/feed.xml" rel="alternate" title="Reaz Romen — Writing" type="application/rss+xml"/><link href="/atom.xml" rel="alternate" title="Reaz Romen — Writing" type="application/atom+xml"/><link href="/assets/phase2.css" rel="stylesheet"/><link href="/assets/responsive-v3.css" rel="stylesheet"/></head>
<body class="rr-themed">
<a class="skip-link" href="#rr-main">Skip to content</a>
<header class="site-header rr-global-header"><div class="site-header-inner"><a aria-label="Reaz Romen home" class="brand" href="/">RR</a><nav aria-label="Main navigation" class="nav"><div class="nav-scroll"><a href="/portfolio.html">Work</a><a href="/perspectives.html">Perspectives</a><a href="/music.html">Music</a><a href="/bangla.html" lang="bn">বাংলা</a><a href="/about.html">About</a><a href="/systems.html">Stack</a></div><div class="nav-actions"><button aria-label="Search and quick navigation" class="icon-link search-action" data-open-command="" title="Search (Ctrl/⌘ K)" type="button"><svg aria-hidden="true" class="icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"></circle><path d="m20 20-4-4"></path></svg></button><a aria-label="GitHub" class="icon-link github-action" href="https://github.com/reazromen" rel="noopener" target="_blank"><svg aria-hidden="true" class="icon icon-fill" viewBox="0 0 24 24"><path d="M12 .7a11.3 11.3 0 0 0-3.57 22.03c.57.1.78-.25.78-.55v-2.18c-3.18.69-3.85-1.35-3.85-1.35-.52-1.32-1.27-1.67-1.27-1.67-1.04-.71.08-.7.08-.7 1.15.08 1.76 1.18 1.76 1.18 1.02 1.75 2.68 1.25 3.33.95.1-.74.4-1.25.73-1.54-2.54-.29-5.21-1.27-5.21-5.65 0-1.25.45-2.27 1.18-3.07-.12-.29-.51-1.46.11-3.03 0 0 .96-.31 3.15 1.17A10.9 10.9 0 0 1 12 5.9c.98 0 1.96.13 2.87.39 2.19-1.48 3.15-1.17 3.15-1.17.62 1.57.23 2.74.11 3.03.74.8 1.18 1.82 1.18 3.07 0 4.39-2.68 5.35-5.23 5.64.41.36.78 1.06.78 2.14v3.18c0 .3.2.66.79.55A11.3 11.3 0 0 0 12 .7Z"></path></svg></a><button aria-label="Toggle color scheme" class="theme-toggle" onclick="toggleTheme()" type="button"><svg aria-hidden="true" class="icon" data-theme-icon="moon" viewBox="0 0 24 24"><path d="M21 12.8A8.5 8.5 0 1 1 11.2 3 6.5 6.5 0 0 0 21 12.8Z"></path></svg><svg aria-hidden="true" class="icon" data-theme-icon="sun" hidden="" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"></path></svg></button></div></nav></div></header>
<main class="shell site-main" id="rr-main">
<article class="project-dossier" data-pagefind-body="">
<header class="dossier-hero">
<a class="back-link" href="{{RR_LINK0}}"><svg aria-hidden="true" class="icon" viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"></path></svg><span>{{RR_BLOCK50}}</span></a>
<div class="dossier-hero-grid">
<div class="dossier-hero-copy">
<p class="eyebrow">{{RR_BLOCK0}}</p>
<h1>{{RR_BLOCK1}}</h1>
<p class="lede">{{RR_BLOCK2}}</p>
<div class="project-hero-actions">
<a class="button" href="{{RR_LINK1}}"><svg aria-hidden="true" class="tech-icon" viewBox="0 0 24 24"><path d="m8 9-4 3 4 3M16 9l4 3-4 3M14 5l-4 14"></path></svg><span>{{RR_BLOCK51}}</span></a>
<a class="button secondary" href="{{RR_LINK2}}"><svg aria-hidden="true" class="tech-icon" viewBox="0 0 24 24"><rect height="5" rx="1" width="6" x="9" y="2"></rect><rect height="5" rx="1" width="6" x="2" y="17"></rect><rect height="5" rx="1" width="6" x="16" y="17"></rect><path d="M12 7v5M5 17v-3h14v3"></path></svg><span>{{RR_BLOCK52}}</span></a>
</div>
</div>
<aside class="product-visual">
<div aria-label="LOUP ESP32-S3 Connected Voice Device system visual" class="visual-blueprint">
<div class="visual-blueprint-head"><span>{{RR_BLOCK53}}</span><b>Built / prototype</b></div>
<div class="visual-core">LOUP ESP32-S3 Connected Voice Device</div>
<div class="visual-orbit">
<span>{{RR_BLOCK54}}</span><span>{{RR_BLOCK55}}</span><span>{{RR_BLOCK56}}</span><span>{{RR_BLOCK57}}</span><span>{{RR_BLOCK58}}</span><span>{{RR_BLOCK59}}</span>
</div>
<div class="visual-flow-mini">
<i>Microphones</i><em>→</em><i>ES7210 / I2S</i><em>→</em><i>ESP32-S3 audio pipeline</i><em>→</em><i>SIP + RTP over Wi-Fi</i>
</div>
</div>
<p>{{RR_BLOCK3}}</p>
</aside>
</div>
</header><nav aria-label="Project engineering record" class="project-record-bar"><span>{{RR_BLOCK60}}</span><a href="{{RR_LINK3}}">Architecture</a><a href="{{RR_LINK4}}">Signal / request path</a><a href="{{RR_LINK5}}">Verification</a><a href="{{RR_LINK6}}">Evidence</a></nav>
<section class="dossier-facts">
<div><span class="fact-label"><svg aria-hidden="true" class="tech-icon" viewBox="0 0 24 24"><path d="M3 12h4l2.2-6 4.2 12 2.2-6H21"></path></svg><span>{{RR_BLOCK61}}</span></span><strong>{{RR_BLOCK62}}</strong></div>
<div><span class="fact-label"><svg aria-hidden="true" class="tech-icon" viewBox="0 0 24 24"><path d="m12 3 9 5-9 5-9-5z"></path><path d="m3 12 9 5 9-5M3 16l9 5 9-5"></path></svg><span>{{RR_BLOCK63}}</span></span><strong>{{RR_BLOCK64}}</strong></div>
<div><span class="fact-label"><svg aria-hidden="true" class="tech-icon" viewBox="0 0 24 24"><rect height="16" rx="2" width="18" x="3" y="4"></rect><path d="m7 9 3 3-3 3M13 15h4"></path></svg><span>{{RR_BLOCK65}}</span></span><strong>{{RR_BLOCK66}}</strong></div>
<div><span class="fact-label"><svg aria-hidden="true" class="tech-icon" viewBox="0 0 24 24"><rect height="5" rx="1" width="6" x="9" y="2"></rect><rect height="5" rx="1" width="6" x="2" y="17"></rect><rect height="5" rx="1" width="6" x="16" y="17"></rect><path d="M12 7v5M5 17v-3h14v3"></path></svg><span>{{RR_BLOCK67}}</span></span><strong>{{RR_BLOCK68}}</strong></div>
</section>
<div class="dossier-layout">
<aside aria-label="Project documentation" class="dossier-toc">
<span>{{RR_BLOCK69}}</span>
<a href="{{RR_LINK7}}">01 / Overview</a>
<a href="{{RR_LINK8}}">02 / Architecture</a>
<a href="{{RR_LINK9}}">03 / Network &amp; data flow</a>
<a href="{{RR_LINK10}}">04 / Stack</a>
<a href="{{RR_LINK11}}">05 / How I built it</a>
<a href="{{RR_LINK12}}">06 / Testing</a>
<a href="{{RR_LINK13}}">07 / Integrations</a>
<a href="{{RR_LINK14}}">08 / Evidence</a>
<a href="{{RR_LINK15}}">09 / Constraints</a>
<a href="{{RR_LINK16}}">10 / Result</a>
</aside>
<div class="dossier-main">
<section class="dossier-section" id="overview">
<div class="section-heading"><span>{{RR_BLOCK70}}</span><div><p class="eyebrow">{{RR_BLOCK4}}</p><h2>{{RR_BLOCK5}}</h2></div></div>
<p class="large-copy">{{RR_BLOCK6}}</p>
<div class="scope-grid">
<article><span>{{RR_BLOCK71}}</span><p>{{RR_BLOCK7}}</p><section class="project-related"><p class="eyebrow">{{RR_BLOCK8}}</p><div class="related-list"><a href="{{RR_LINK17}}"><strong>{{RR_BLOCK72}}</strong><span>{{RR_BLOCK73}}</span></a><a href="{{RR_LINK18}}"><strong>{{RR_BLOCK74}}</strong><span>{{RR_BLOCK75}}</span></a><a href="{{RR_LINK19}}"><strong>{{RR_BLOCK76}}</strong><span>{{RR_BLOCK77}}</span></a></div></section></article>
<article><span>{{RR_BLOCK78}}</span><p>{{RR_BLOCK9}}</p></article>
<article><span>{{RR_BLOCK79}}</span><p>{{RR_BLOCK10}}</p></article>
</div>
</section>
<section class="dossier-section" id="architecture">
<div class="section-heading"><span>{{RR_BLOCK80}}</span><div><p class="eyebrow">{{RR_BLOCK11}}</p><h2>{{RR_BLOCK12}}</h2></div></div>
<div class="architecture-map">
<article>
<div class="arch-node-index">01</div>
<strong>{{RR_BLOCK81}}</strong>
<p>{{RR_BLOCK13}}</p>
</article>
<article>
<div class="arch-node-index">02</div>
<strong>{{RR_BLOCK82}}</strong>
<p>{{RR_BLOCK14}}</p>
</article>
<article>
<div class="arch-node-index">03</div>
<strong>{{RR_BLOCK83}}</strong>
<p>{{RR_BLOCK15}}</p>
</article>
</div>
</section>
<section class="dossier-section" id="network">
<div class="section-heading"><span>{{RR_BLOCK84}}</span><div><p class="eyebrow">{{RR_BLOCK16}}</p><h2>{{RR_BLOCK17}}</h2></div></div>
<div class="trace-hint"><span>{{RR_BLOCK85}}</span><span>{{RR_BLOCK86}}</span><button class="trace-clear" hidden="" type="button">Clear</button></div><div aria-label="LOUP ESP32-S3 Connected Voice Device network and data flow" class="network-diagram" role="img">
<div aria-pressed="false" class="network-node" data-trace-index="1" role="button" tabindex="0"><small>01</small><strong>{{RR_BLOCK87}}</strong></div>
<div class="network-arrow"><span>{{RR_BLOCK88}}</span><i>data / control</i></div>
<div aria-pressed="false" class="network-node" data-trace-index="2" role="button" tabindex="0"><small>02</small><strong>{{RR_BLOCK89}}</strong></div>
<div class="network-arrow"><span>{{RR_BLOCK90}}</span><i>data / control</i></div>
<div aria-pressed="false" class="network-node" data-trace-index="3" role="button" tabindex="0"><small>03</small><strong>{{RR_BLOCK91}}</strong></div>
<div class="network-arrow"><span>{{RR_BLOCK92}}</span><i>data / control</i></div>
<div aria-pressed="false" class="network-node" data-trace-index="4" role="button" tabindex="0"><small>04</small><strong>{{RR_BLOCK93}}</strong></div>
<div class="network-arrow"><span>{{RR_BLOCK94}}</span><i>data / control</i></div>
<div aria-pressed="false" class="network-node" data-trace-index="5" role="button" tabindex="0"><small>05</small><strong>{{RR_BLOCK95}}</strong></div>
<div class="network-arrow"><span>{{RR_BLOCK96}}</span><i>data / control</i></div>
<div aria-pressed="false" class="network-node" data-trace-index="6" role="button" tabindex="0"><small>06</small><strong>{{RR_BLOCK97}}</strong></div>
</div>
</section>
<section class="dossier-section" id="stack">
<div class="section-heading"><span>{{RR_BLOCK98}}</span><div><p class="eyebrow">{{RR_BLOCK18}}</p><h2>{{RR_BLOCK19}}</h2></div></div>
<div class="stack-board">
<div><span>{{RR_BLOCK99}}</span><strong>{{RR_BLOCK100}}</strong></div>
<div><span>{{RR_BLOCK101}}</span><strong>{{RR_BLOCK102}}</strong></div>
<div><span>{{RR_BLOCK103}}</span><strong>{{RR_BLOCK104}}</strong></div>
<div><span>{{RR_BLOCK105}}</span><strong>{{RR_BLOCK106}}</strong></div>
<div><span>{{RR_BLOCK107}}</span><strong>{{RR_BLOCK108}}</strong></div>
<div><span>{{RR_BLOCK109}}</span><strong>{{RR_BLOCK110}}</strong></div>
</div>
</section>
<section class="dossier-section" id="implementation">
<div class="section-heading"><span>{{RR_BLOCK111}}</span><div><p class="eyebrow">{{RR_BLOCK20}}</p><h2>{{RR_BLOCK21}}</h2></div></div>
<ol class="implementation-list">
<li>{{RR_BLOCK22}}</li>
<li>{{RR_BLOCK24}}</li>
<li>{{RR_BLOCK26}}</li>
</ol>
</section>
<section class="dossier-section" id="testing">
<div class="section-heading"><span>{{RR_BLOCK112}}</span><div><p class="eyebrow">{{RR_BLOCK28}}</p><h2>{{RR_BLOCK29}}</h2></div></div>
<div class="validation-grid">
<article><span>{{RR_BLOCK113}}</span><p>{{RR_BLOCK30}}</p></article>
<article><span>{{RR_BLOCK114}}</span><p>{{RR_BLOCK31}}</p></article>
<article><span>{{RR_BLOCK115}}</span><p>{{RR_BLOCK32}}</p></article>
<article><span>{{RR_BLOCK116}}</span><p>{{RR_BLOCK33}}</p></article>
<article><span>{{RR_BLOCK117}}</span><p>{{RR_BLOCK34}}</p></article>
</div>
</section>
<section class="dossier-section" id="integrations">
<div class="section-heading"><span>{{RR_BLOCK118}}</span><div><p class="eyebrow">{{RR_BLOCK35}}</p><h2>{{RR_BLOCK36}}</h2></div></div>
<div class="integration-board">
<div class="integration-core"><small>CORE</small><strong>{{RR_BLOCK119}}</strong></div>
<div class="integration-links">
<div><span>{{RR_BLOCK120}}</span><strong>{{RR_BLOCK121}}</strong></div>
<div><span>{{RR_BLOCK122}}</span><strong>{{RR_BLOCK123}}</strong></div>
<div><span>{{RR_BLOCK124}}</span><strong>{{RR_BLOCK125}}</strong></div>
<div><span>{{RR_BLOCK126}}</span><strong>{{RR_BLOCK127}}</strong></div>
</div>
</div>
</section>
<section class="dossier-section" id="evidence">
<div class="section-heading"><span>{{RR_BLOCK128}}</span><div><p class="eyebrow">{{RR_BLOCK37}}</p><h2>{{RR_BLOCK38}}</h2></div></div>
<div class="evidence-board">
<div class="evidence-item" id="evidence-01"><span>{{RR_BLOCK129}}</span><span class="evidence-type">{{RR_BLOCK130}}</span><strong>{{RR_BLOCK131}}</strong></div>
<div class="evidence-item" id="evidence-02"><span>{{RR_BLOCK132}}</span><span class="evidence-type">{{RR_BLOCK133}}</span><strong>{{RR_BLOCK134}}</strong></div>
<div class="evidence-item" id="evidence-03"><span>{{RR_BLOCK135}}</span><span class="evidence-type">{{RR_BLOCK136}}</span><strong>{{RR_BLOCK137}}</strong></div>
<div class="evidence-item" id="evidence-04"><span>{{RR_BLOCK138}}</span><span class="evidence-type">{{RR_BLOCK139}}</span><strong>{{RR_BLOCK140}}</strong></div>
<div class="evidence-item" id="evidence-05"><span>{{RR_BLOCK141}}</span><span class="evidence-type">{{RR_BLOCK142}}</span><strong>{{RR_BLOCK143}}</strong></div>
<div class="evidence-item" id="evidence-06"><span>{{RR_BLOCK144}}</span><span class="evidence-type">{{RR_BLOCK145}}</span><strong>{{RR_BLOCK146}}</strong></div>
</div>
</section>
<section class="dossier-section" id="constraints">
<div class="section-heading"><span>{{RR_BLOCK147}}</span><div><p class="eyebrow">{{RR_BLOCK39}}</p><h2>{{RR_BLOCK40}}</h2></div></div>
<div class="constraint-list">
<p>{{RR_BLOCK41}}</p>
<p>{{RR_BLOCK42}}</p>
<p>{{RR_BLOCK43}}</p>
<p>{{RR_BLOCK44}}</p>
</div>
</section>
<section class="dossier-section dossier-result" id="result">
<div class="section-heading"><span>{{RR_BLOCK148}}</span><div><p class="eyebrow">{{RR_BLOCK45}}</p><h2>{{RR_BLOCK46}}</h2></div></div>
<p class="result-copy">{{RR_BLOCK47}}</p>
<div class="case-bridge">
<div><p class="eyebrow">{{RR_BLOCK48}}</p><h3>{{RR_BLOCK49}}</h3></div>
<a class="button" href="{{RR_LINK20}}">Open full case study →</a>
</div>
</section>
</div>
</div>
<nav aria-label="Project navigation" class="project-pagination">
<span></span>
<a class="next" href="{{RR_LINK21}}"><span>{{RR_BLOCK149}}</span><strong>{{RR_BLOCK150}}</strong></a>
</nav>
</article>
</main>
<footer class="shell site-footer">
<div>
<span class="status-dot"></span>
<strong>Reaz Romen — independent systems engineer.</strong>
</div>
<p>Firmware, real-time communications, infrastructure and field notes. First-party HTML/CSS, no analytics, no third-party scripts.</p>
<nav aria-label="Footer">
<a href="../../topics.html">Topics</a>
<a href="../../systems.html">Systems</a>
<a href="../../archive.html">Archive</a>
<a href="../../author/reaz-romen.html">Author record</a>
</nav>
</footer>
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