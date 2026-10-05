---
title: Temperature Monitoring Belongs Beside Load
url: /posts/temperature-monitoring-belongs-beside-load.html
date: '2023-11-13'
read_time: 1
excerpt: A small Mac mini running many containers can hit thermal constraints before
  ordinary CPU graphs explain why performance changed.
topic: observability-monitoring
tags:
- temperature
- smart
- hardware
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Host & Resource Signals · advanced'
outputs:
- url: /posts/temperature-monitoring-belongs-beside-load.html
  template: cms/templates/posts/posts--temperature-monitoring-belongs-beside-load.tpl
  source: cms/templates/posts/posts--temperature-monitoring-belongs-beside-load.json
---

A small Mac mini running many containers can hit thermal constraints before ordinary CPU graphs explain why performance changed. I ended up treating `node_thermal_zone_temp and SMART temperature` as the useful observation point rather than relying on a generic service-up indicator. Thermal data gives hardware context to throttling, fan behavior and storage health that software-only metrics cannot provide.

This is a good example of hardware telemetry correlation. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Trend CPU package and SSD temperature with load and disk activity, and alert on sustained abnormal values rather than isolated sensor noise. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
