---
title: Disk Latency Explains More Than Disk Throughput
url: /posts/disk-latency-explains-more-than-throughput.html
date: '2022-07-27'
read_time: 1
excerpt: The host can show modest megabytes per second while applications still wait
  because each storage request takes too long.
topic: observability-monitoring
tags:
- disk-latency
- i-o
- linux
- grafana
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Storage & I/O · advanced'
outputs:
- url: /posts/disk-latency-explains-more-than-throughput.html
  template: cms/templates/posts/posts--disk-latency-explains-more-than-throughput.tpl
  source: cms/templates/posts/posts--disk-latency-explains-more-than-throughput.json
---

The host can show modest megabytes per second while applications still wait because each storage request takes too long. The monitoring mistake would be to read one metric in isolation. `read/write latency derived from block-device timing counters` is useful because it narrows the question, and throughput describes volume; latency describes service time. low throughput with high latency often points to storage contention or device trouble.

In software operations this falls under latency-first storage diagnosis. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Graph latency beside IOPS, throughput, disk busy time and PSI so slow storage is not mistaken for an application CPU problem. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
