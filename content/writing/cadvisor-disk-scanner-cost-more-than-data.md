---
title: The cAdvisor Disk Scanner Was More Expensive Than the Data Was Worth
url: /posts/cadvisor-disk-scanner-cost-more-than-data.html
date: '2024-06-07'
read_time: 1
excerpt: The production monitoring stack measured roughly 428 MiB of cAdvisor memory
  with filesystem disk collection enabled on a small host.
topic: observability-monitoring
tags:
- cadvisor
- memory
- optimization
- observability
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Storage & I/O · advanced'
outputs:
- url: /posts/cadvisor-disk-scanner-cost-more-than-data.html
  template: cms/templates/posts/posts--cadvisor-disk-scanner-cost-more-than-data.tpl
  source: cms/templates/posts/posts--cadvisor-disk-scanner-cost-more-than-data.json
---

The production monitoring stack measured roughly 428 MiB of cAdvisor memory with filesystem disk collection enabled on a small host. What made the issue measurable was `cAdvisor process memory compared before and after disabling filesystem disk scanning`. After keeping diskIO but disabling the expensive disk scanner, steady cAdvisor memory dropped to roughly 20–28 MiB while the important I/O signals remained.

I classify this as observability overhead budgeting. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Measure the monitor itself, remove expensive collectors whose value can be obtained elsewhere, and preserve the high-value signals with lower-cost paths. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `218300b` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
