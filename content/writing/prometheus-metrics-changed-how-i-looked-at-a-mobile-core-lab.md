---
title: Prometheus Metrics Changed How I Looked at a Mobile Core Lab
url: /posts/prometheus-metrics-changed-how-i-looked-at-a-mobile-core-lab.html
date: '2021-03-17'
read_time: 1
excerpt: Logs explain individual failures; metrics show whether the system is drifting
  before the failures become obvious.
topic: linux-homelab
tags:
- prometheus
- monitoring
- open5gs
- metrics
draft: false
featured: false
language: en
eyebrow: 2023 Mobile and 5G Notes · intermediate
outputs:
- url: /posts/prometheus-metrics-changed-how-i-looked-at-a-mobile-core-lab.html
  template: cms/templates/posts/posts--prometheus-metrics-changed-how-i-looked-at-a-mobile-core-lab.tpl
  source: cms/templates/posts/posts--prometheus-metrics-changed-how-i-looked-at-a-mobile-core-lab.json
---

Logs were my default tool for mobile-core troubleshooting because signalling failures produce useful detail. The problem is that logs are event-oriented. They tell me what happened to one transaction, but they do not immediately tell me whether latency, CPU, memory, registration failures or session counts have been drifting for an hour.

Adding Prometheus-style metrics changed the lab from something I inspected only after it broke into something I could watch over time. Basic host metrics were already useful: CPU saturation, memory pressure, disk usage and interface counters. Application metrics became more valuable when they exposed registrations, session attempts, failures or queue depth.

The important part was not building a pretty dashboard. It was choosing signals that map to system behavior. A rising authentication-failure rate is more useful than a generic container-up metric. A sudden drop in established sessions can matter even if every process still reports healthy.

I kept packet captures and logs in the workflow. Metrics tell me when and where to look; traces explain the individual protocol exchange. That combination later became the basis for how I approached production VoIP and home-server observability as well.
