---
title: Volume Size Monitoring Needs Ownership Context
url: /posts/volume-size-monitoring-needs-ownership-context.html
date: '2022-08-27'
read_time: 1
excerpt: A large Docker volume is not actionable if the dashboard cannot tell which
  service owns it or whether that growth is expected.
topic: observability-monitoring
tags:
- docker-volumes
- capacity
- ownership
- grafana
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Storage & I/O · advanced'
outputs:
- url: /posts/volume-size-monitoring-needs-ownership-context.html
  template: cms/templates/posts/posts--volume-size-monitoring-needs-ownership-context.tpl
  source: cms/templates/posts/posts--volume-size-monitoring-needs-ownership-context.json
---

A large Docker volume is not actionable if the dashboard cannot tell which service owns it or whether that growth is expected. I ended up treating `Docker volume byte metrics plus project and volume identity` as the useful observation point rather than relying on a generic service-up indicator. Capacity data becomes operationally useful only when an operator can connect the bytes to a service, retention policy and backup class.

This is a good example of resource ownership monitoring. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Keep volume name, Compose project and service documentation aligned so growth alerts point directly to the responsible runbook. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `218300b` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
