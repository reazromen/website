---
title: Retention Needs Both Time and Size Limits
url: /posts/retention-needs-time-and-size-limits.html
date: '2026-09-14'
read_time: 1
excerpt: Keeping thirty days of Prometheus data is useful until series growth causes
  the TSDB to consume more disk than the host can safely spare.
topic: observability-monitoring
tags:
- retention
- prometheus
- loki
- storage
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Observability Architecture · advanced'
outputs:
- url: /posts/retention-needs-time-and-size-limits.html
  template: cms/templates/posts/posts--retention-needs-time-and-size-limits.tpl
  source: cms/templates/posts/posts--retention-needs-time-and-size-limits.json
---

Keeping thirty days of Prometheus data is useful until series growth causes the TSDB to consume more disk than the host can safely spare. On the finished hserver stack, `Prometheus 30-day retention plus 15 GB size cap and Loki seven-day retention` is the signal that makes the difference visible. Time and size constraints protect different failure modes: history growth over time and sudden cardinality or ingestion expansion.

The engineering pattern here is bounded telemetry retention. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Set retention from incident-investigation needs and host capacity, then monitor actual storage so limits remain appropriate as the system grows. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
