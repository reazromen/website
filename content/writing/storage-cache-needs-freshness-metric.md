---
title: A Storage Cache Needs Its Own Freshness Metric
url: /posts/storage-cache-needs-freshness-metric.html
date: '2026-09-14'
read_time: 1
excerpt: Caching Docker storage inventory reduced overhead, but a silent refresh failure
  could otherwise leave old values looking current indefinitely.
topic: observability-monitoring
tags:
- cache-freshness
- meta-monitoring
- docker
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Storage & I/O · advanced'
outputs:
- url: /posts/storage-cache-needs-freshness-metric.html
  template: cms/templates/posts/posts--storage-cache-needs-freshness-metric.tpl
  source: cms/templates/posts/posts--storage-cache-needs-freshness-metric.json
---

Caching Docker storage inventory reduced overhead, but a silent refresh failure could otherwise leave old values looking current indefinitely. On the finished hserver stack, `hserver_docker_storage_cache_refresh_success and hserver_docker_storage_cache_age_seconds` is the signal that makes the difference visible. Every cache that supports monitoring becomes another monitored component; without freshness metadata, cached telemetry can create false confidence.

The engineering pattern here is meta-monitoring. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Expose cache success and age, alert when age exceeds the refresh contract, and show stale state clearly in Grafana. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `218300b`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
