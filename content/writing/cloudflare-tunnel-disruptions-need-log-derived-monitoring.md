---
title: Cloudflare Tunnel Disruptions Need Log-Derived Monitoring
url: /posts/cloudflare-tunnel-disruptions-need-log-derived-monitoring.html
date: '2026-09-14'
read_time: 1
excerpt: An external endpoint can flap because the tunnel reconnects even when the
  local service and LAN probe remain healthy.
topic: observability-monitoring
tags:
- cloudflare-tunnel
- logs
- availability
- edge
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/cloudflare-tunnel-disruptions-need-log-derived-monitoring.html
  template: cms/templates/posts/posts--cloudflare-tunnel-disruptions-need-log-derived-monitoring.tpl
  source: cms/templates/posts/posts--cloudflare-tunnel-disruptions-need-log-derived-monitoring.json
---

An external endpoint can flap because the tunnel reconnects even when the local service and LAN probe remain healthy. The monitoring mistake would be to read one metric in isolation. `Cloudflare journal disruption counts plus public probe state` is useful because it narrows the question, and combining logs with synthetic reachability separates edge transport instability from application failure and provides evidence even after the tunnel reconnects.

In software operations this falls under event-plus-state monitoring. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Alert on disruption bursts, keep the public probe as the outcome signal, and query tunnel logs for the causal sequence. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
