---
title: The Slow Users Disappear Inside the Average
date: '2024-04-15'
draft: false
language: en
url: /posts/bn-average-tail-experience.html
topic: observability-monitoring
tags:
- metrics
- latency
featured: false
read_time: 2
excerpt: >-
  A low average response time can make a system look fast even when a smaller group of
  users waits much longer. Their experience disappears into one number. To understand
  latency, we also need to understand its distribution.
editorial_batch: 20261003-100-niches
---

A low average response time can make a system look fast even when a smaller group of users waits much longer. Their experience disappears into one number. To understand latency, we also need to understand its distribution.

Suppose most requests are fast and a few are extremely slow. The average may move only slightly while the people behind those slow requests are still having a bad experience. Percentiles or an appropriate distribution can answer different questions, although their own calculation limits matter too.

Histogram buckets should come from the needs of the system and its users. If a certain amount of waiting is acceptable and another threshold is not, the measurement should have enough resolution around that boundary. Keeping only default buckets for every workload can hide what matters.

I think of metrics as a map of experience. The average is one mark on that map. If I cannot see where bad experiences are accumulating, a clean average does not finish the story of how long people are waiting.

Source: [official reference](https://prometheus.io/docs/practices/histograms/).
