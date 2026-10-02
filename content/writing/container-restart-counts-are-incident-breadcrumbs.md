---
title: Container Restart Counts Are Incident Breadcrumbs
url: /posts/container-restart-counts-are-incident-breadcrumbs.html
date: '2026-09-14'
read_time: 1
excerpt: A service can look healthy now and still have restarted repeatedly overnight,
  erasing the evidence from a simple current-state view.
topic: observability-monitoring
tags:
- docker
- restarts
- incidents
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Docker & Containers · advanced'
outputs:
- url: /posts/container-restart-counts-are-incident-breadcrumbs.html
  template: cms/templates/posts/posts--container-restart-counts-are-incident-breadcrumbs.tpl
  source: cms/templates/posts/posts--container-restart-counts-are-incident-breadcrumbs.json
---

A service can look healthy now and still have restarted repeatedly overnight, erasing the evidence from a simple current-state view. I ended up treating `container restart counters and runtime state` as the useful observation point rather than relying on a generic service-up indicator. Restarts are durable clues for crash loops, OOM kills, daemon restarts and unstable dependencies even after the process comes back.

This is a good example of event-history monitoring. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Graph restart deltas and correlate them with logs, OOM events and host pressure so recovered failures still trigger investigation. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
