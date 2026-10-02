---
title: OOM Events Need Container and Host Context
url: /posts/oom-events-need-container-and-host-context.html
date: '2026-09-14'
read_time: 1
excerpt: An application disappearing under load can be either a container memory-limit
  event or a host-wide memory emergency.
topic: observability-monitoring
tags:
- oom
- cgroups
- docker
- memory
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Docker & Containers · advanced'
outputs:
- url: /posts/oom-events-need-container-and-host-context.html
  template: cms/templates/posts/posts--oom-events-need-container-and-host-context.tpl
  source: cms/templates/posts/posts--oom-events-need-container-and-host-context.json
---

An application disappearing under load can be either a container memory-limit event or a host-wide memory emergency. The monitoring mistake would be to read one metric in isolation. `container OOM events, kernel OOM logs and memory limits` is useful because it narrows the question, and the same symptom has different blast radius depending on whether cgroup enforcement or the kernel oom killer made the decision.

In software operations this falls under multi-layer memory incident analysis. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Keep container OOM, limit, working-set, host PSI and kernel OOM signals together before changing resource limits. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
