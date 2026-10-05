---
title: Who Monitors the Monitoring System?
date: '2023-06-26'
draft: false
language: en
url: /posts/bn-monitoring-monitor-itself.html
topic: observability-monitoring
tags:
- observability
- reliability
featured: false
read_time: 2
excerpt: >-
  If monitoring stops, evidence of failures elsewhere can disappear too. Silence can then
  look like health. The monitoring system therefore needs evidence that its own collection
  and notification paths are still working.
editorial_batch: 20261003-100-niches
---

If monitoring stops, evidence of failures elsewhere can disappear too. Silence can then look like health. The monitoring system therefore needs evidence that its own collection and notification paths are still working.

Is scraping still happening? How old is the newest data? Are notifications actually being delivered? Those are separate questions. A dashboard loading successfully does not prove the alert path works, and the presence of some metrics does not prove every target is being collected.

A known, safe test event can validate the full notification path. Follow it from collection to rule evaluation to delivery and measure where time is spent. The test signal should be clearly distinguished from a real emergency.

I do not think of monitoring as an all-knowing eye outside the system. It runs on finite resources and dependencies of its own. When those limits are visible, its claims about other systems become more trustworthy.

Source: [official reference](https://prometheus.io/docs/practices/instrumentation/).
