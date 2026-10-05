---
title: Database Size Growth Is a Capacity Trend, Not an Emergency Metric
url: /posts/database-size-growth-capacity-trend.html
date: '2025-02-01'
read_time: 1
excerpt: A database normally grows, so alerting on size alone would create noise while
  ignoring the important question of growth rate and disk headroom.
topic: observability-monitoring
tags:
- database-size
- capacity-planning
- postgresql
- storage
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Databases · advanced'
outputs:
- url: /posts/database-size-growth-capacity-trend.html
  template: cms/templates/posts/posts--database-size-growth-capacity-trend.tpl
  source: cms/templates/posts/posts--database-size-growth-capacity-trend.json
---

A database normally grows, so alerting on size alone would create noise while ignoring the important question of growth rate and disk headroom. On the finished hserver stack, `database size bytes over time` is the signal that makes the difference visible. Size history becomes useful when compared with retention, backup size, root filesystem capacity and the expected workload growth curve.

The engineering pattern here is trend-based capacity planning. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Graph size by database, review unusual slope changes after releases, and project headroom before storage reaches a hard threshold. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
