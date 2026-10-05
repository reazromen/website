---
title: Metric Cardinality Is a Capacity Problem Disguised as a Naming Problem
url: /posts/metric-cardinality-capacity-problem-disguised-as-naming-problem.html
date: '2025-03-04'
read_time: 1
excerpt: Labels make dashboards flexible, but uncontrolled label values multiply time
  series and memory cost quickly.
topic: observability
tags:
- prometheus
- cardinality
- metrics
- capacity
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Observability · advanced'
outputs:
- url: /posts/metric-cardinality-capacity-problem-disguised-as-naming-problem.html
  template: cms/templates/posts/posts--metric-cardinality-capacity-problem-disguised-as-naming-problem.tpl
  source: cms/templates/posts/posts--metric-cardinality-capacity-problem-disguised-as-naming-problem.json
---

The production configuration keeps container label exposure narrow and records active-series counts in acceptance evidence. High-value dimensions remain, while unbounded labels are avoided or moved to logs and inventory data.

The observability expansion added deeper container, database, network and VoIP views. With that growth, the number of active series became an operational resource worth tracking rather than an abstract Prometheus detail. Every label combination creates another time series. A metric that looks cheap in code can become expensive when labels contain container IDs, paths, users or other high-cardinality dimensions.

Prometheus explicitly recommends controlling label cardinality and keeping most metrics low-dimensional. Metrics are for aggregatable signals; detailed identities often belong in logs or queryable inventory systems.

Review label sets during code review and alert on unexpected series growth after deployment. Cardinality regressions should be treated like memory regressions because that is what they eventually become. The concrete hserver evidence is commit 218300b, so this note is tied to an actual production change rather than a hypothetical failure.
