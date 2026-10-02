---
title: Disabling One Metric Family Can Be Better Than Tuning the Whole Monitoring
  Stack
url: /posts/disable-one-expensive-metric-family-before-tuning-everything.html
date: '2026-09-14'
read_time: 1
excerpt: The fastest observability optimization came from identifying one costly collector
  instead of globally lowering fidelity.
topic: observability
tags:
- cadvisor
- profiling
- metrics
- performance
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Observability · advanced'
outputs:
- url: /posts/disable-one-expensive-metric-family-before-tuning-everything.html
  template: cms/templates/posts/posts--disable-one-expensive-metric-family-before-tuning-everything.tpl
  source: cms/templates/posts/posts--disable-one-expensive-metric-family-before-tuning-everything.json
---

When cAdvisor memory was too high, the tempting fix was to reduce scrape frequency or shorten retention across the board. That would have degraded every metric even though only part of the collection path was responsible for most of the cost. The expensive behavior was concentrated in filesystem storage scanning. Treating observability as one monolithic workload would have hidden the opportunity to remove the specific cost while keeping high-value runtime signals.

The production profile kept disk I/O and pressure data but disabled the filesystem disk scanner. Storage inventory moved to a separate cached exporter with a much slower refresh cycle.

Document which dashboards and alerts depend on each collector before changing it. That turns resource tuning into an explicit feature tradeoff rather than an accidental loss of visibility. This is profile-before-optimize applied to telemetry. Measure the expensive path, remove or redesign that path, then verify which capabilities remain instead of applying global degradation without evidence. The concrete hserver evidence is commit 218300b, so this note is tied to an actual production change rather than a hypothetical failure.
