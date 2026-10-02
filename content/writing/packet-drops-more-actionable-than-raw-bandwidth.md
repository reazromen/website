---
title: Packet Drops Are More Actionable Than Raw Bandwidth
url: /posts/packet-drops-more-actionable-than-raw-bandwidth.html
date: '2026-09-14'
read_time: 1
excerpt: High interface traffic can be completely healthy, while a small but sustained
  drop rate can damage voice, APIs and tunnel reliability.
topic: observability-monitoring
tags:
- packet-drops
- networking
- node_exporter
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/packet-drops-more-actionable-than-raw-bandwidth.html
  template: cms/templates/posts/posts--packet-drops-more-actionable-than-raw-bandwidth.tpl
  source: cms/templates/posts/posts--packet-drops-more-actionable-than-raw-bandwidth.json
---

High interface traffic can be completely healthy, while a small but sustained drop rate can damage voice, APIs and tunnel reliability. On the finished hserver stack, `node_network_receive_drop_total and transmit_drop_total rates` is the signal that makes the difference visible. Drop counters measure failed delivery work rather than traffic volume, making them a better early warning for queue or interface pressure.

The engineering pattern here is error-rate monitoring. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Exclude virtual interfaces where appropriate, alert on sustained physical-interface drops, and correlate with bandwidth and retransmission signals. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
