---
title: Critical Container Log Spikes Are a Triage Signal
url: /posts/critical-container-log-spikes-triage-signal.html
date: '2023-08-30'
read_time: 1
excerpt: A container can remain healthy by its HTTP probe while its logs suddenly
  fill with exceptions, retries or failed dependency calls.
topic: observability-monitoring
tags:
- container-logs
- loki
- errors
- triage
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Logs & Security · advanced'
outputs:
- url: /posts/critical-container-log-spikes-triage-signal.html
  template: cms/templates/posts/posts--critical-container-log-spikes-triage-signal.tpl
  source: cms/templates/posts/posts--critical-container-log-spikes-triage-signal.json
---

A container can remain healthy by its HTTP probe while its logs suddenly fill with exceptions, retries or failed dependency calls. The monitoring mistake would be to read one metric in isolation. `critical/error log rate by container` is useful because it narrows the question, and log-rate spikes provide an early incident clue but need service context because some applications use severe log levels more noisily than others.

In software operations this falls under log-derived anomaly triage. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Use spikes to direct investigation, then confirm with latency, error-rate, restart and dependency metrics before paging on every error line. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
