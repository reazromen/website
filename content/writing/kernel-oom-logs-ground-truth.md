---
title: Kernel OOM Logs Are the Ground Truth for Host Memory Kills
url: /posts/kernel-oom-logs-ground-truth.html
date: '2026-02-08'
read_time: 1
excerpt: A process disappearing can look like an application crash unless the kernel
  journal is checked for OOM-killer activity.
topic: observability-monitoring
tags:
- oom-killer
- kernel
- journald
- memory
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Logs & Security · advanced'
outputs:
- url: /posts/kernel-oom-logs-ground-truth.html
  template: cms/templates/posts/posts--kernel-oom-logs-ground-truth.tpl
  source: cms/templates/posts/posts--kernel-oom-logs-ground-truth.json
---

A process disappearing can look like an application crash unless the kernel journal is checked for OOM-killer activity. On the finished hserver stack, `kernel OOM event counters and matching journal records` is the signal that makes the difference visible. Kernel logs identify when memory pressure caused the operating system to kill a process, separating resource failure from application logic failure.

The engineering pattern here is event-source correlation. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Alert on OOM events immediately, link them with memory PSI and container OOM metrics, and preserve the surrounding journal context for postmortem analysis. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
