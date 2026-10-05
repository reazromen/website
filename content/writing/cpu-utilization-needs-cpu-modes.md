---
title: CPU Utilization Without CPU Modes Hides the Bottleneck
url: /posts/cpu-utilization-needs-cpu-modes.html
date: '2022-07-03'
read_time: 1
excerpt: The host can report high CPU usage even when the useful question is whether
  time is going to user work, system work, steal, or I/O wait.
topic: observability-monitoring
tags:
- cpu
- iowait
- linux
- grafana
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Host & Resource Signals · advanced'
outputs:
- url: /posts/cpu-utilization-needs-cpu-modes.html
  template: cms/templates/posts/posts--cpu-utilization-needs-cpu-modes.tpl
  source: cms/templates/posts/posts--cpu-utilization-needs-cpu-modes.json
---

The host can report high CPU usage even when the useful question is whether time is going to user work, system work, steal, or I/O wait. What made the issue measurable was `node_cpu_seconds_total by mode`. Mode breakdown separates compute saturation from kernel overhead and storage-induced waiting, which lead to completely different fixes.

I classify this as resource saturation decomposition. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Keep CPU mode panels beside load and PSI so an operator can move from symptom to constrained subsystem without guessing. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `b65d5d4` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
