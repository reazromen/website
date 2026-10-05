---
title: Label Freedom Comes With a Time-Series Cost
date: '2026-08-01'
draft: false
language: en
url: /posts/bn-metric-label-cardinality.html
topic: observability-monitoring
tags:
- metrics
- capacity
featured: false
read_time: 2
excerpt: >-
  Metric labels let us divide one measurement in many useful ways, but every new combination
  of label values can create another time series. Greater detail also carries collection,
  storage, and query cost.
editorial_batch: 20261003-100-niches
---

Metric labels let us divide one measurement in many useful ways, but every new combination of label values can create another time series. Greater detail also carries collection, storage, and query cost.

If every request ID becomes a label value, the number of series can grow extremely quickly. Grouping by route pattern is not the same cost as grouping by every complete URL. Some information belongs in metrics; some is better kept in logs or traces.

During design, estimate how many possible values a label can have. After a change, measure the actual series count and collection cost. Preserve useful dimensions without turning accidental uniqueness into permanent metric state.

Observability is itself a system. If its limits are ignored, it can place pressure on both the monitored workload and on itself. Finer-grained data is not automatically better understanding.

Source: [official reference](https://prometheus.io/docs/practices/naming/).
