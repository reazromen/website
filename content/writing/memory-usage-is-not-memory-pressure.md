---
title: Memory Usage Is Not the Same as Memory Pressure
url: /posts/memory-usage-is-not-memory-pressure.html
date: '2024-09-07'
read_time: 1
excerpt: The host looked busy enough that a simple percentage could easily become
  the whole diagnosis, but Linux memory reclaim makes that misleading.
topic: observability-monitoring
tags:
- prometheus
- linux
- memory
- psi
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Host & Resource Signals · advanced'
outputs:
- url: /posts/memory-usage-is-not-memory-pressure.html
  template: cms/templates/posts/posts--memory-usage-is-not-memory-pressure.tpl
  source: cms/templates/posts/posts--memory-usage-is-not-memory-pressure.json
---

The host looked busy enough that a simple percentage could easily become the whole diagnosis, but Linux memory reclaim makes that misleading. On hserver the first signal I use for this question is `node_memory_MemAvailable_bytes and PSI memory pressure`. Available memory shows what the kernel can still reclaim, while pressure shows whether workloads are actually stalling for memory.

The important part is interpretation rather than collecting another graph. capacity monitoring plus pressure-based diagnosis. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Alert on sustained high utilization, then confirm with PSI, swap activity and OOM evidence before blaming a service. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
