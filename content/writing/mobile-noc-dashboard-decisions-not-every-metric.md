---
title: A Mobile NOC Dashboard Should Show Decisions, Not Every Metric
url: /posts/mobile-noc-dashboard-decisions-not-every-metric.html
date: '2026-09-14'
read_time: 1
excerpt: The phone-sized operations view cannot carry hundreds of panels without turning
  urgent information into scrolling noise.
topic: observability-monitoring
tags:
- grafana
- noc
- mobile-dashboard
- operations
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Observability Architecture · advanced'
outputs:
- url: /posts/mobile-noc-dashboard-decisions-not-every-metric.html
  template: cms/templates/posts/posts--mobile-noc-dashboard-decisions-not-every-metric.tpl
  source: cms/templates/posts/posts--mobile-noc-dashboard-decisions-not-every-metric.json
---

The phone-sized operations view cannot carry hundreds of panels without turning urgent information into scrolling noise. What made the issue measurable was `NOC Mobile summary of critical alerts, target health, host capacity, backups, VoIP workers and recent errors`. A constrained dashboard is useful when it prioritizes whether intervention is needed and provides enough context to choose the next detailed view.

I classify this as progressive disclosure in operations UI. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Keep critical state, capacity headroom and service-impact signals on the mobile page while leaving root-cause exploration to domain dashboards. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `218300b` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
