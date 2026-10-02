---
title: Normalize Load Average by CPU Count
url: /posts/normalize-load-average-by-cpu-count.html
date: '2026-09-14'
read_time: 1
excerpt: A load average of four means something very different on a two-core system
  than on an eight-core system.
topic: observability-monitoring
tags:
- load-average
- cpu
- prometheus
- linux
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Host & Resource Signals · advanced'
outputs:
- url: /posts/normalize-load-average-by-cpu-count.html
  template: cms/templates/posts/posts--normalize-load-average-by-cpu-count.tpl
  source: cms/templates/posts/posts--normalize-load-average-by-cpu-count.json
---

A load average of four means something very different on a two-core system than on an eight-core system. The monitoring mistake would be to read one metric in isolation. `node_load5 divided by discovered CPU count` is useful because it narrows the question, and raw load has no built-in normalization, so the dashboard and alert need to relate runnable work to available cpu capacity.

In software operations this falls under capacity-normalized alerting. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Use sustained normalized load and then inspect CPU mode, I/O wait and pressure before deciding whether compute is the bottleneck. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
