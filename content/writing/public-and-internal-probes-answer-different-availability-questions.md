---
title: Public and Internal Probes Answer Different Availability Questions
url: /posts/public-and-internal-probes-answer-different-availability-questions.html
date: '2026-09-14'
read_time: 1
excerpt: A service can be healthy on the LAN and unreachable through Cloudflare, TLS,
  DNS or authentication at the public edge.
topic: observability-monitoring
tags:
- blackbox-exporter
- availability
- cloudflare
- synthetic-monitoring
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/public-and-internal-probes-answer-different-availability-questions.html
  template: cms/templates/posts/posts--public-and-internal-probes-answer-different-availability-questions.tpl
  source: cms/templates/posts/posts--public-and-internal-probes-answer-different-availability-questions.json
---

A service can be healthy on the LAN and unreachable through Cloudflare, TLS, DNS or authentication at the public edge. On hserver the first signal I use for this question is `separate blackbox-http and blackbox-public probe jobs`. Internal probing isolates service health while public probing tests the user-visible chain, so disagreement between them immediately narrows the failure domain.

The important part is interpretation rather than collecting another graph. layered synthetic monitoring. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Keep separate labels and dashboards for internal and public probes and avoid collapsing them into one availability percentage. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
