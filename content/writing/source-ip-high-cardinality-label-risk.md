---
title: Do Not Turn Source IP into a High-Cardinality Metric Label
url: /posts/source-ip-high-cardinality-label-risk.html
date: '2023-01-12'
read_time: 1
excerpt: Security logs contain useful source addresses, but promoting every IP to
  a Prometheus or Loki index label would create unbounded cardinality on an Internet-facing
  service.
topic: observability-monitoring
tags:
- loki
- cardinality
- labels
- security
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Logs & Security · advanced'
outputs:
- url: /posts/source-ip-high-cardinality-label-risk.html
  template: cms/templates/posts/posts--source-ip-high-cardinality-label-risk.tpl
  source: cms/templates/posts/posts--source-ip-high-cardinality-label-risk.json
---

Security logs contain useful source addresses, but promoting every IP to a Prometheus or Loki index label would create unbounded cardinality on an Internet-facing service. On the finished hserver stack, `bounded journal labels with source IP kept in log content` is the signal that makes the difference visible. The hserver design indexes stable fields such as unit, priority and identifier while leaving volatile addresses for query-time parsing.

The engineering pattern here is cardinality-aware log design. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Choose labels from bounded operational dimensions and keep unbounded request attributes in the log body where they can still be searched during investigation. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
