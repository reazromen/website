---
title: TCP Retransmit Ratio Is Better Than Counting Retransmits Alone
url: /posts/tcp-retransmit-ratio-better-than-count.html
date: '2024-10-17'
read_time: 1
excerpt: A few retransmissions during heavy traffic may be normal, while the same
  count during low traffic can represent a serious quality problem.
topic: observability-monitoring
tags:
- tcp
- retransmissions
- network-quality
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/tcp-retransmit-ratio-better-than-count.html
  template: cms/templates/posts/posts--tcp-retransmit-ratio-better-than-count.tpl
  source: cms/templates/posts/posts--tcp-retransmit-ratio-better-than-count.json
---

A few retransmissions during heavy traffic may be normal, while the same count during low traffic can represent a serious quality problem. On hserver the first signal I use for this question is `TCP retransmits divided by transmitted TCP segments`. A ratio normalizes retransmission against traffic volume and makes comparison across quiet and busy periods more meaningful.

The important part is interpretation rather than collecting another graph. normalized error-rate monitoring. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Track both absolute rate and ratio, then correlate spikes with packet drops, Wi-Fi signal, tunnel logs and public latency. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
