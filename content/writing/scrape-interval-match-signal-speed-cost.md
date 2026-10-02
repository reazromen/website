---
title: Scrape Interval Should Match Signal Speed and Collection Cost
url: /posts/scrape-interval-match-signal-speed-cost.html
date: '2026-09-14'
read_time: 1
excerpt: CPU can change meaningfully in seconds while Docker image storage or Grafana
  process memory does not need the same fifteen-second collection cadence.
topic: observability-monitoring
tags:
- prometheus
- scrape-interval
- sampling
- observability-cost
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Observability Architecture · advanced'
outputs:
- url: /posts/scrape-interval-match-signal-speed-cost.html
  template: cms/templates/posts/posts--scrape-interval-match-signal-speed-cost.tpl
  source: cms/templates/posts/posts--scrape-interval-match-signal-speed-cost.json
---

CPU can change meaningfully in seconds while Docker image storage or Grafana process memory does not need the same fifteen-second collection cadence. I ended up treating `15s global scrape with 30s and 60s overrides for selected jobs` as the useful observation point rather than relying on a generic service-up indicator. Using one cadence for every signal wastes resources and can amplify expensive collectors without improving operational decisions.

This is a good example of cost-aware sampling. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Assign scrape intervals by volatility and response requirement, then expose freshness so slower collection is never mistaken for missing telemetry. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `218300b` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
