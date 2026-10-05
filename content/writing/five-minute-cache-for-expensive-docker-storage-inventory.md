---
title: A Five-Minute Cache Was the Right Place for Expensive Docker Storage Inventory
url: /posts/five-minute-cache-for-expensive-docker-storage-inventory.html
date: '2025-03-16'
read_time: 1
excerpt: Not every metric needs to be collected at the same cadence; expensive inventory
  can be cached without weakening real-time health signals.
topic: observability
tags:
- docker
- cache
- prometheus
- inventory
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Observability · advanced'
outputs:
- url: /posts/five-minute-cache-for-expensive-docker-storage-inventory.html
  template: cms/templates/posts/posts--five-minute-cache-for-expensive-docker-storage-inventory.tpl
  source: cms/templates/posts/posts--five-minute-cache-for-expensive-docker-storage-inventory.json
---

Monitoring systems work better when data cadence matches decision latency. Fast-changing failure signals deserve frequent collection; slow inventory data can be cached and its freshness exposed as a first-class metric. Writable-layer, image and volume size information was useful for capacity planning but expensive to derive continuously. Collecting it at cAdvisor cadence consumed resources without providing equally time-sensitive operational value.

The data had inventory semantics but was being treated like a real-time signal. Storage size usually changes slowly compared with CPU, packet rate or container liveness.

We moved Docker storage inspection to a background `/system/df` cache refreshed every five minutes. Prometheus scrapes the lightweight exporter every minute and also records cache age and refresh success. For each expensive measurement, define how stale it may be before it stops being useful. Then expose cache age so operators can distinguish an old but valid value from a collector that silently stopped refreshing. The concrete hserver evidence is commit 218300b, so this note is tied to an actual production change rather than a hypothetical failure.
