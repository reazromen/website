---
title: Writable Layer Size Should Not Be Polled Expensively Every Scrape
url: /posts/writable-layer-size-should-not-be-polled-expensively.html
date: '2025-01-06'
read_time: 1
excerpt: Docker storage size is useful, but asking the daemon for deep filesystem
  inventory on every fast scrape consumed too much monitoring overhead.
topic: observability-monitoring
tags:
- docker-storage
- cache
- inventory-exporter
- observability-cost
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Storage & I/O · advanced'
outputs:
- url: /posts/writable-layer-size-should-not-be-polled-expensively.html
  template: cms/templates/posts/posts--writable-layer-size-should-not-be-polled-expensively.tpl
  source: cms/templates/posts/posts--writable-layer-size-should-not-be-polled-expensively.json
---

Docker storage size is useful, but asking the daemon for deep filesystem inventory on every fast scrape consumed too much monitoring overhead. On hserver the first signal I use for this question is `inventory-exporter cached writable-layer metrics`. Slow inventory data does not need the same cadence as CPU or packet counters; sampling cost should match how quickly the underlying state changes.

The important part is interpretation rather than collecting another graph. cost-aware telemetry design. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Refresh Docker storage inventory in the background every few minutes, expose cache age, and scrape the cheap cached result more frequently. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `218300b`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
