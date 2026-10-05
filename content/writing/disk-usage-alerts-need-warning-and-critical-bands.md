---
title: Disk Usage Alerts Need Warning and Critical Bands
url: /posts/disk-usage-alerts-need-warning-and-critical-bands.html
date: '2026-09-19'
read_time: 1
excerpt: A single disk threshold gives operators no distinction between early cleanup
  work and a filesystem that is close to stopping writes.
topic: observability-monitoring
tags:
- disk
- capacity
- alerts
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Storage & I/O · advanced'
outputs:
- url: /posts/disk-usage-alerts-need-warning-and-critical-bands.html
  template: cms/templates/posts/posts--disk-usage-alerts-need-warning-and-critical-bands.tpl
  source: cms/templates/posts/posts--disk-usage-alerts-need-warning-and-critical-bands.json
---

A single disk threshold gives operators no distinction between early cleanup work and a filesystem that is close to stopping writes. On hserver the first signal I use for this question is `root filesystem usage with 85% warning and 93% critical thresholds`. Two severity bands support different response urgency and reduce the temptation to set one noisy threshold that everyone learns to ignore.

The important part is interpretation rather than collecting another graph. graduated capacity alerting. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Use warning for planned remediation, critical for immediate action, and keep growth trend visible so capacity work happens before either threshold. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
