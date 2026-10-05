---
title: Swap Usage Needs Duration and Context
url: /posts/swap-usage-needs-duration-and-context.html
date: '2025-05-11'
read_time: 1
excerpt: A few megabytes of swap on an old Linux host did not automatically mean an
  incident, especially after long uptime.
topic: observability-monitoring
tags:
- swap
- linux
- prometheus
- capacity
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Host & Resource Signals · advanced'
outputs:
- url: /posts/swap-usage-needs-duration-and-context.html
  template: cms/templates/posts/posts--swap-usage-needs-duration-and-context.tpl
  source: cms/templates/posts/posts--swap-usage-needs-duration-and-context.json
---

A few megabytes of swap on an old Linux host did not automatically mean an incident, especially after long uptime. I ended up treating `node_memory_SwapFree_bytes with a 15-minute alert window` as the useful observation point rather than relying on a generic service-up indicator. Swap becomes operationally interesting when usage is sustained, growing, and paired with memory pressure or latency rather than merely nonzero.

This is a good example of symptom correlation instead of threshold-only diagnosis. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Track swap trend, PSI and OOM counters together and keep the alert delayed enough to ignore harmless historical pages. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
