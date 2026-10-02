---
title: Context Switches and Interrupts Explain Some Invisible CPU Cost
url: /posts/context-switches-and-interrupts-explain-cpu-cost.html
date: '2026-09-14'
read_time: 1
excerpt: CPU percentage alone did not reveal when the kernel was spending more work
  scheduling tasks or servicing device activity.
topic: observability-monitoring
tags:
- context-switches
- interrupts
- linux
- performance
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Host & Resource Signals · advanced'
outputs:
- url: /posts/context-switches-and-interrupts-explain-cpu-cost.html
  template: cms/templates/posts/posts--context-switches-and-interrupts-explain-cpu-cost.tpl
  source: cms/templates/posts/posts--context-switches-and-interrupts-explain-cpu-cost.json
---

CPU percentage alone did not reveal when the kernel was spending more work scheduling tasks or servicing device activity. The monitoring mistake would be to read one metric in isolation. `node_context_switches_total and node_intr_total` is useful because it narrows the question, and rapid growth in context switches or interrupts can explain overhead created by high process churn, networking, or i/o even when one process is not dominant.

In software operations this falls under secondary host-signal analysis. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Use rates and correlate them with process count, network traffic and disk activity before optimizing an application that may not be the source. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
