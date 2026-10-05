---
title: No Data Is Not Zero
date: '2024-09-09'
draft: false
language: en
url: /posts/bn-no-data-not-zero.html
topic: observability-monitoring
tags:
- metrics
- data-quality
featured: false
read_time: 2
excerpt: >-
  Replacing missing data with zero can make a graph look cleaner while changing its meaning.
  Zero says a measurement was made and the result was zero. No data says the result is unknown.
editorial_batch: 20261003-100-niches
---

Replacing missing data with zero can make a graph look cleaner while changing its meaning. Zero says a measurement was made and the result was zero. No data says the result is unknown. A known state and an unknown state are not interchangeable.

Suppose a river gauge stops reporting. Displaying zero can make it look as if there is no water. Or if a failed-call metric disappears, filling the gap with zero can make the phone system look healthy. The reason for the absence matters.

An interface can expose data age and source status to make the difference visible. It can also show the last known value, but that value should be labeled with its age rather than presented as current.

For me, saying *unknown* is not weakness. It is information integrity. Turning unknown into zero does not remove uncertainty; it merely hides the uncertainty from the person making the decision.

Source: [official reference](https://prometheus.io/docs/prometheus/latest/querying/basics/).
