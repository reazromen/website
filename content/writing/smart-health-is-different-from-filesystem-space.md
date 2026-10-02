---
title: SMART Health Is Different from Filesystem Free Space
url: /posts/smart-health-is-different-from-filesystem-space.html
date: '2026-09-14'
read_time: 1
excerpt: A disk can have plenty of free capacity while the underlying SSD is reporting
  temperature or device-health problems.
topic: observability-monitoring
tags:
- smart
- ssd
- storage
- hardware
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Host & Resource Signals · advanced'
outputs:
- url: /posts/smart-health-is-different-from-filesystem-space.html
  template: cms/templates/posts/posts--smart-health-is-different-from-filesystem-space.tpl
  source: cms/templates/posts/posts--smart-health-is-different-from-filesystem-space.json
---

A disk can have plenty of free capacity while the underlying SSD is reporting temperature or device-health problems. On the finished hserver stack, `smartctl_exporter device-health and temperature metrics` is the signal that makes the difference visible. Capacity, filesystem integrity and physical-device health are independent layers, so one green disk panel cannot stand in for the others.

The engineering pattern here is layered storage health monitoring. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Keep SMART status, filesystem usage, inode usage, latency and backup state visible as separate signals with separate failure semantics. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
