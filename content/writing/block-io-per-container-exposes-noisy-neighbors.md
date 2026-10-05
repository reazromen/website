---
title: Block I/O per Container Exposes Noisy Neighbors
url: /posts/block-io-per-container-exposes-noisy-neighbors.html
date: '2026-08-05'
read_time: 1
excerpt: Host disk latency can rise because one container is performing heavy reads
  or writes while every other service only sees the consequence.
topic: observability-monitoring
tags:
- docker
- block-i-o
- storage
- noisy-neighbor
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Docker & Containers · advanced'
outputs:
- url: /posts/block-io-per-container-exposes-noisy-neighbors.html
  template: cms/templates/posts/posts--block-io-per-container-exposes-noisy-neighbors.tpl
  source: cms/templates/posts/posts--block-io-per-container-exposes-noisy-neighbors.json
---

Host disk latency can rise because one container is performing heavy reads or writes while every other service only sees the consequence. I ended up treating `container block I/O read/write counters` as the useful observation point rather than relying on a generic service-up indicator. Per-container I/O attribution helps separate a host storage problem from one workload creating excessive disk demand.

This is a good example of resource attribution. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Correlate container block throughput with host latency, disk busy time and PSI before throttling or moving a workload. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `218300b` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
