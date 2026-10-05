---
title: SIP Proxy Failure Rate Needs a Window
url: /posts/sip-proxy-failure-rate-needs-window.html
date: '2024-05-17'
read_time: 1
excerpt: A single SIP proxy error may be harmless noise, but repeated failures over
  a short interval can indicate backend, routing or dependency trouble.
topic: observability-monitoring
tags:
- sip
- error-rate
- prometheus
- voip
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: VoIP · advanced'
outputs:
- url: /posts/sip-proxy-failure-rate-needs-window.html
  template: cms/templates/posts/posts--sip-proxy-failure-rate-needs-window.tpl
  source: cms/templates/posts/posts--sip-proxy-failure-rate-needs-window.json
---

A single SIP proxy error may be harmless noise, but repeated failures over a short interval can indicate backend, routing or dependency trouble. On the finished hserver stack, `increase(voip_sip_proxy_failures_total[5m])` is the signal that makes the difference visible. Windowed counters convert cumulative totals into incident-rate signals and make alert thresholds meaningful after long process uptime.

The engineering pattern here is rate-based error monitoring. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Alert on bursts, inspect response-code and backend context, and avoid resetting counters simply to make dashboards look clean. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
