---
title: Container I/O Pressure Shows Waiting, Not Just Bytes
url: /posts/container-io-pressure-shows-waiting.html
date: '2024-11-15'
read_time: 1
excerpt: A workload can perform modest disk throughput and still suffer because requests
  are waiting behind slow storage or competing I/O.
topic: observability-monitoring
tags:
- docker
- psi
- i-o-pressure
- performance
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Docker & Containers · advanced'
outputs:
- url: /posts/container-io-pressure-shows-waiting.html
  template: cms/templates/posts/posts--container-io-pressure-shows-waiting.tpl
  source: cms/templates/posts/posts--container-io-pressure-shows-waiting.json
---

A workload can perform modest disk throughput and still suffer because requests are waiting behind slow storage or competing I/O. The monitoring mistake would be to read one metric in isolation. `container I/O pressure metrics` is useful because it narrows the question, and bytes per second measures volume, while pressure measures stalled execution; both are needed to distinguish busy from harmful contention.

In software operations this falls under saturation monitoring. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Alert on sustained pressure and validate with host latency and disk busy metrics before concluding the container itself is inefficient. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `218300b`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
