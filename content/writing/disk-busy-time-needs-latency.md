---
title: Disk Busy Time Needs Latency Beside It
url: /posts/disk-busy-time-needs-latency.html
date: '2026-09-14'
read_time: 1
excerpt: A device at high utilization can be handling work efficiently, while a lower-utilization
  device can still be returning slow requests.
topic: observability-monitoring
tags:
- disk-busy
- latency
- saturation
- linux
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Storage & I/O · advanced'
outputs:
- url: /posts/disk-busy-time-needs-latency.html
  template: cms/templates/posts/posts--disk-busy-time-needs-latency.tpl
  source: cms/templates/posts/posts--disk-busy-time-needs-latency.json
---

A device at high utilization can be handling work efficiently, while a lower-utilization device can still be returning slow requests. On the finished hserver stack, `block-device busy time with read/write latency` is the signal that makes the difference visible. Utilization alone does not prove saturation because queueing, request merging and device parallelism change how busy time translates to response time.

The engineering pattern here is correlated saturation monitoring. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Treat busy time as supporting evidence and require latency or pressure signals before calling storage the bottleneck. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
