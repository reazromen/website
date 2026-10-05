---
title: A Counter Reset Changes the Story in the Graph
date: '2023-04-22'
draft: false
language: en
url: /posts/bn-counter-reset-rate.html
topic: observability-monitoring
tags:
- metrics
- time
featured: false
read_time: 2
excerpt: >-
  A counter accumulates events over time, but some counters start over when a process
  restarts. Subtracting the next value from the previous one can then produce an impossible
  negative event. The events did not run backward; the measurement history was reset.
editorial_batch: 20261003-100-niches
---

A counter accumulates events over time, but some counters start over when a process restarts. Subtracting the next value from the previous one can then produce an impossible negative event. The events did not run backward; the measurement history was reset.

That is why it matters to understand how a monitoring tool calculates rates from counters. Which reset patterns does it handle? What sample interval does it use? A short or long rate window can change the meaning of the graph.

Suppose a traffic graph changes suddenly after a restart. Do not assume user behavior changed. Check collection timing, process lifetime, and metric type as well.

Before telling a story with data, it helps to understand how the data remembers. A counter is a kind of memory, but that memory has a lifetime. Knowing that boundary prevents strange conclusions from otherwise clean graphs.

Source: [official reference](https://prometheus.io/docs/prometheus/latest/querying/functions/).
