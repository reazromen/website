---
title: FreeSWITCH Health Is a Fleet Count, Not One Boolean
url: /posts/freeswitch-health-fleet-count.html
date: '2026-09-14'
read_time: 1
excerpt: A multi-worker voice stack can keep serving calls after one FreeSWITCH node
  fails, so one global up/down flag hides degraded capacity.
topic: observability-monitoring
tags:
- freeswitch
- capacity
- voip
- health
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: VoIP · advanced'
outputs:
- url: /posts/freeswitch-health-fleet-count.html
  template: cms/templates/posts/posts--freeswitch-health-fleet-count.tpl
  source: cms/templates/posts/posts--freeswitch-health-fleet-count.json
---

A multi-worker voice stack can keep serving calls after one FreeSWITCH node fails, so one global up/down flag hides degraded capacity. I ended up treating `voip_freeswitch_nodes_healthy versus configured nodes` as the useful observation point rather than relying on a generic service-up indicator. Comparing healthy and configured worker counts shows partial degradation before the entire service becomes unavailable.

This is a good example of redundant-capacity monitoring. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Alert when healthy workers fall below configured capacity, and keep per-node session and heartbeat panels for fast isolation. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
