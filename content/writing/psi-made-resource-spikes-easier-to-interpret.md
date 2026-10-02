---
title: PSI Made Short Resource Spikes Easier to Interpret
url: /posts/psi-made-resource-spikes-easier-to-interpret.html
date: '2026-09-14'
read_time: 1
excerpt: Some periods looked acceptable in average CPU and RAM graphs while interactive
  services still felt slow.
topic: observability-monitoring
tags:
- psi
- linux
- saturation
- grafana
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Host & Resource Signals · advanced'
outputs:
- url: /posts/psi-made-resource-spikes-easier-to-interpret.html
  template: cms/templates/posts/posts--psi-made-resource-spikes-easier-to-interpret.tpl
  source: cms/templates/posts/posts--psi-made-resource-spikes-easier-to-interpret.json
---

Some periods looked acceptable in average CPU and RAM graphs while interactive services still felt slow. On the finished hserver stack, `CPU, memory and I/O pressure stall information` is the signal that makes the difference visible. Pressure Stall Information records time tasks are delayed waiting for a resource, exposing contention that percentage utilization can miss.

The engineering pattern here is saturation monitoring with Linux PSI. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Graph PSI next to CPU, memory, disk latency and container pressure and alert only on sustained contention that can affect service latency. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `218300b`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
