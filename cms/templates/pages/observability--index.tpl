<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="How I operate and observe a multi-service Linux platform: metrics, logs, probes, dashboards, alert validation, network visibility, secure access and recovery engineering.">
<meta name="author" content="Reaz Romen">
<title>Observability &amp; Infrastructure — Reaz Romen</title>
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/sitewide-v2.css">
<link rel="stylesheet" href="/assets/phase1.css">
<link rel="stylesheet" href="/assets/phase2.css">
<link rel="stylesheet" href="/assets/responsive-v3.css">
<style>
.obs-hero{padding:clamp(3rem,7vw,6rem) 0 3rem;border-bottom:1px solid var(--line)}.obs-hero h1{max-width:950px}.obs-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.obs-card{padding:1.3rem;border:1px solid var(--line);border-radius:12px;background:var(--surface,transparent)}.obs-card h3{margin:.2rem 0 .7rem}.obs-card p{line-height:1.65;color:var(--muted)}.obs-card a{font-weight:700}.obs-section{padding:2.8rem 0;border-bottom:1px solid var(--line)}.obs-section>p{max-width:850px;line-height:1.75}.obs-section h2{margin:.3rem 0 1rem}.obs-flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:1.5rem 0}.obs-flow div{padding:1rem;border:1px solid var(--line);border-radius:10px}.obs-flow b{display:block;margin-bottom:.45rem}.obs-flow span{font-size:.88rem;color:var(--muted);line-height:1.5}.obs-articles{padding:2.5rem 0;border-bottom:1px solid var(--line)}.obs-articles .post-list{display:grid;gap:12px}.obs-articles .post-card{padding:1.1rem;border:1px solid var(--line);border-radius:10px}.obs-articles .post-card h3{margin:.4rem 0}.obs-articles .post-card p{line-height:1.6}.obs-articles .post-card .tags{display:flex;gap:.5rem;flex-wrap:wrap}.obs-articles .post-card .tags a{font-size:.8rem}
@media(max-width:850px){.obs-grid{grid-template-columns:1fr}.obs-flow{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.obs-flow{grid-template-columns:1fr}}
</style>
</head>
<body class="rr-themed">
<a class="skip-link" href="#rr-main">Skip to content</a>
<main class="shell site-main" id="rr-main" data-pagefind-body>
<section class="obs-hero">
<p class="eyebrow">{{RR_BLOCK0}}</p>
<h1>{{RR_BLOCK1}}</h1>
<p class="lede">{{RR_BLOCK2}}</p>
</section>
<section class="obs-section">
<p class="eyebrow">THE PLATFORM</p><h2>{{RR_BLOCK3}}</h2><p>{{RR_BLOCK4}}</p>
<div class="obs-flow" aria-label="Observability flow">
<div><b>Collect</b><span>Host, container, service and endpoint signals</span></div>
<div><b>Correlate</b><span>Metrics, logs, probes and dependency state</span></div>
<div><b>Respond</b><span>Rules, alert routing, runbooks and operator controls</span></div>
<div><b>Verify</b><span>Controlled failures, recovery drills and evidence</span></div>
</div>
</section>
<section class="obs-section">
<p class="eyebrow">IMPLEMENTATION</p><h2>{{RR_BLOCK5}}</h2><p>{{RR_BLOCK6}}</p>
<div class="obs-grid">
<article class="obs-card"><h3>Metrics &amp; dashboards</h3><p>Prometheus, PromQL, node_exporter, cAdvisor, service exporters and Grafana. Dashboards are split between quick triage and deeper investigation.</p></article>
<article class="obs-card"><h3>Logs &amp; probes</h3><p>Loki and Alloy, external Blackbox-style checks, DNS/TLS/HTTPS probes, database checks and log-derived signals for failures that metrics alone cannot explain.</p></article>
<article class="obs-card"><h3>Alerts &amp; recovery</h3><p>Alertmanager, freshness guards, warning/critical bands, notification-path checks, backup integrity, restore verification and documented operational procedures.</p></article>
</div>
</section>
<section class="obs-section">
<p class="eyebrow">VALIDATION</p><h2>{{RR_BLOCK7}}</h2><p>{{RR_BLOCK8}}</p>
</section>
<section class="obs-section">
<p class="eyebrow">OPERATIONS</p><h2>{{RR_BLOCK9}}</h2><p>{{RR_BLOCK10}}</p>
<div class="obs-grid">
<article class="obs-card"><h3><a href="/portfolio/projects/infrastructure-operations-platform.html">Infrastructure Operations Platform ↗</a></h3><p>Service inventory, lifecycle controls, secure access, dependency state, logs, topology and recovery workflows.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/production-observability-alert-validation.html">Production Observability &amp; Alert Validation ↗</a></h3><p>Controlled failure, PromQL diagnosis and end-to-end alert-path validation.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/disaster-recovery-restore-verification.html">Disaster Recovery &amp; Restore Verification ↗</a></h3><p>Backup freshness and integrity are not treated as proof that data can be restored.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/network-flow-visualization.html">Network Flow Visualization ↗</a></h3><p>Trace dependencies and packet paths rather than troubleshooting each service in isolation.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/network-payload-capture-pipeline.html">Network Payload Capture Pipeline ↗</a></h3><p>Repeatable capture and investigation workflows for network-level evidence.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/central-secret-lifecycle-openbao.html">Central Secret Lifecycle ↗</a></h3><p>Secret handling and operational state are part of reliability and recovery.</p></article>
</div>
</section>
<section class="obs-articles">
<p class="eyebrow">FIELD NOTES / COLLECTION 01</p><h2>{{RR_BLOCK13}}</h2>
<div class="post-list editorial-list">{{RR_LIST0}}</div>
</section>
<section class="obs-articles">
<p class="eyebrow">FIELD NOTES / COLLECTION 02</p><h2>Monitoring &amp; Alert Engineering</h2>
<div class="post-list editorial-list">{{RR_LIST1}}</div>
</section>
<section class="obs-articles">
<p class="eyebrow">FIELD NOTES / COLLECTION 03</p><h2>Backup, Recovery &amp; Continuity</h2>
<div class="post-list editorial-list">{{RR_LIST2}}</div>
</section>
</main>
<script src="/assets/site.js"></script><script src="/assets/sitewide.js"></script><script src="/assets/phase1.js"></script><script src="/assets/responsive-v3.js"></script>
</body></html>