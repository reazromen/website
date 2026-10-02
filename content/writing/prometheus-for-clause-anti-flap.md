---
title: The `for` Clause Is an Anti-Flap Tool, Not Decoration
url: /posts/prometheus-for-clause-anti-flap.html
date: '2026-09-14'
read_time: 1
excerpt: CPU, packet loss and endpoint probes can cross thresholds for a few seconds
  during harmless transitions or deployment activity.
topic: observability-monitoring
tags:
- prometheus
- alerting
- flapping
- sre
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Alerting & Notification · advanced'
outputs:
- url: /posts/prometheus-for-clause-anti-flap.html
  template: cms/templates/posts/posts--prometheus-for-clause-anti-flap.tpl
  source: cms/templates/posts/posts--prometheus-for-clause-anti-flap.json
---

CPU, packet loss and endpoint probes can cross thresholds for a few seconds during harmless transitions or deployment activity. I ended up treating `Prometheus alert rules with sustained`for`windows` as the useful observation point rather than relying on a generic service-up indicator. Requiring the condition to persist filters transients without hiding real failures, but the duration must match how quickly the service can become user-impacting.

This is a good example of time-qualified alerting. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Choose `for` durations per signal, keep critical fast-failure paths shorter, and review whether long delays are masking genuine incidents. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
