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
<p class="eyebrow">PRODUCTION COVERAGE</p><h2>What the production server monitors</h2>
<p>Monitoring is organized around failure domains, not just a list of running processes. The goal is to spot resource pressure, broken dependencies, unreachable services, silent alert failures and backups that cannot be restored.</p>
<div class="obs-grid">
<article class="obs-card"><h3>Host health &amp; capacity</h3><p>CPU utilization and load averages, memory and swap pressure, Linux Pressure Stall Information (PSI), disk capacity, inode exhaustion, disk I/O, SMART drive health, and TCP retransmissions. Capacity alerts help catch a server running out of headroom before services fail.</p></article>
<article class="obs-card"><h3>Docker &amp; service lifecycle</h3><p>Container CPU and memory, restarts, OOM events, health-check state, expected-versus-running services, Docker storage usage and inventory freshness. Resource collection is tuned so the monitoring stack does not consume excessive RAM on a modest machine.</p></article>
<article class="obs-card"><h3>Public endpoints &amp; network edge</h3><p>External reachability and response status for public HTTPS endpoints, DNS resolution, TLS certificate validity/expiry, redirects and latency. Checks also cover the reverse proxy, secure access gateway and tunnel path, helping separate an application failure from an ingress or authentication problem.</p></article>
<article class="obs-card"><h3>Databases &amp; application dependencies</h3><p>Availability and deep health checks for database services, connection and query responsiveness, service-specific metrics, and dependency failures. A running database process is not enough if the application cannot connect or complete a useful check.</p></article>
<article class="obs-card"><h3>VoIP &amp; real-time communications</h3><p>Health and reachability of SIP/voice components, including FreeSWITCH, OpenSIPS, drachtio and RTPengine where deployed. Service checks and logs help investigate signaling failures, media-path problems and unhealthy dependencies rather than relying on process state alone.</p></article>
<article class="obs-card"><h3>Logs &amp; telemetry pipeline</h3><p>System journal and application logs through Loki/Alloy, ingestion errors and dropped-log signals, stale telemetry, Prometheus target/scrape health, time-series database growth and metric cardinality. The monitoring system is monitored as a production dependency itself.</p></article>
<article class="obs-card"><h3>Backups &amp; disaster recovery</h3><p>Scheduled-job success, backup freshness, artifact presence, checksum/integrity evidence, retention and storage headroom, plus restore verification. A green backup job is not considered proof of recoverability until restoration has been checked.</p></article>
<article class="obs-card"><h3>Security &amp; access controls</h3><p>TLS and trusted-certificate health, authentication and protected admin-route behavior, secret-service health, sensitive configuration/permission review, audit events and unexpected service-state changes. Access failures are distinguished from application downtime.</p></article>
<article class="obs-card"><h3>OTA, jobs &amp; operational automation</h3><p>Scheduled runner freshness, failed systemd units, time synchronization, backup/OTA job outcomes, deployment provenance and drift, signed-update verification and rollout/rollback gates where those workflows are in use.</p></article>
</div>
</section>
<section class="obs-section">
<p class="eyebrow">ALERTING / RESPONSE</p><h2>From a metric to a verified notification</h2>
<p>Prometheus evaluates PromQL alert rules and Alertmanager routes matching alerts to the configured notification channel. A rule is not considered complete until its labels match real metrics, its pending/firing/resolved transitions behave as expected, and delivery is verified end to end.</p>
<div class="obs-flow" aria-label="Alert response path">
<div><b>1. Detect</b><span>Thresholds, sustained load, unavailable probes, stale telemetry or failed jobs</span></div>
<div><b>2. Evaluate</b><span>PromQL conditions, labels, severity and pending duration</span></div>
<div><b>3. Notify</b><span>Alertmanager routing and ntfy delivery checks</span></div>
<div><b>4. Verify</b><span>Controlled test, notification receipt, recovery and resolved state</span></div>
</div>
<div class="obs-grid">
<article class="obs-card"><h3>Capacity &amp; availability</h3><p>High sustained load, memory pressure, low disk space, inode exhaustion, unhealthy containers, failed public probes, TLS/DNS problems and critical dependencies.</p></article>
<article class="obs-card"><h3>Data &amp; automation</h3><p>Stale or failed backups, failed restore checks, missing scheduled-runner heartbeats, failed jobs, and service or update workflows that stop reporting expected state.</p></article>
<article class="obs-card"><h3>Observability failures</h3><p>Missing Prometheus targets, stale samples, alert-rule label mismatches, dropped logs, notification delivery failures and telemetry storage/cardinality growth.</p></article>
</div>
<p>For alert testing, I use a controlled failure, verify the source metric, inspect the exact PromQL expression and label matching, observe the alert transition, confirm delivery, then restore the service and verify resolution. This tests the whole chain—not only whether a rule file parses.</p>
</section>
<section class="obs-section">
<p class="eyebrow">TOOLS / ARCHITECTURE</p><h2>The tools behind the monitoring</h2>
<div class="obs-grid">
<article class="obs-card"><h3>Metrics &amp; rules</h3><p><strong>Prometheus</strong> for scraping and time-series storage; <strong>node_exporter</strong> for host metrics; <strong>cAdvisor</strong> for container metrics; purpose-built inventory and service exporters; <strong>PromQL</strong> and <strong>promtool</strong> for alert logic and validation.</p></article>
<article class="obs-card"><h3>Dashboards &amp; alert routing</h3><p><strong>Grafana</strong> for operational dashboards and drill-down; <strong>Alertmanager</strong> for grouping, routing and lifecycle; <strong>ntfy</strong> for push notifications; external scheduled dead-man checks for independent heartbeat verification.</p></article>
<article class="obs-card"><h3>Logs &amp; probes</h3><p><strong>Loki</strong> and <strong>Grafana Alloy</strong> for log collection and correlation; <strong>Blackbox Exporter</strong> and targeted probes for endpoint, DNS, TLS and availability checks; system journal and service logs for incident context.</p></article>
<article class="obs-card"><h3>Production operations</h3><p><strong>Docker</strong>, Linux systemd and storage/SMART utilities; <strong>Caddy</strong>, <strong>Cloudflare Tunnel</strong> and <strong>Authelia</strong> in the ingress/authentication path; database and VoIP-specific health checks; checksum and restore tests for recovery evidence.</p></article>
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
<p class="eyebrow">RELATED WORK</p><h2>Implementation notes</h2>
<div class="obs-grid">
<article class="obs-card"><h3><a href="/portfolio/projects/production-observability-alert-validation.html">Production Observability &amp; Alert Validation ↗</a></h3><p>Testing metrics, alert rules, label matching and the complete notification path.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/infrastructure-operations-platform.html">Infrastructure Operations Platform ↗</a></h3><p>Service inventory, lifecycle controls, secure access, dependency state and recovery workflows.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/disaster-recovery-restore-verification.html">Disaster Recovery &amp; Restore Verification ↗</a></h3><p>Backup freshness and integrity checks followed by evidence-based restore verification.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/network-flow-visualization.html">Network Flow Visualization ↗</a></h3><p>Trace dependencies and packet paths to investigate cross-service failures.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/network-payload-capture-pipeline.html">Network Payload Capture Pipeline ↗</a></h3><p>Repeatable capture and investigation workflows for network-level evidence.</p></article>
<article class="obs-card"><h3><a href="/portfolio/projects/central-secret-lifecycle-openbao.html">Central Secret Lifecycle ↗</a></h3><p>Secret handling, access boundaries and operational health as part of reliability.</p></article>
</div>
</section>
</main>
<script src="/assets/site.js"></script><script src="/assets/sitewide.js"></script><script src="/assets/phase1.js"></script><script src="/assets/responsive-v3.js"></script>
</body></html>