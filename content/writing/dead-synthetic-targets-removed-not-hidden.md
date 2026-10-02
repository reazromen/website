---
title: Dead Synthetic Targets Should Be Removed, Not Hidden
url: /posts/dead-synthetic-targets-removed-not-hidden.html
date: '2026-09-14'
read_time: 1
excerpt: Placeholder or obsolete probe targets can stay in configuration after architecture
  changes and permanently pollute availability dashboards.
topic: observability-monitoring
tags:
- blackbox-exporter
- targets
- configuration-hygiene
- ci
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Observability Architecture · advanced'
outputs:
- url: /posts/dead-synthetic-targets-removed-not-hidden.html
  template: cms/templates/posts/posts--dead-synthetic-targets-removed-not-hidden.tpl
  source: cms/templates/posts/posts--dead-synthetic-targets-removed-not-hidden.json
---

Placeholder or obsolete probe targets can stay in configuration after architecture changes and permanently pollute availability dashboards. I ended up treating `acceptance field synthetic_refs_remaining equals zero` as the useful observation point rather than relying on a generic service-up indicator. A clean target inventory means every probe represents a real service or an intentional dependency rather than historical configuration debris.

This is a good example of configuration hygiene for monitoring. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Treat target lists as reviewed production inventory, delete obsolete references, and validate probe configuration in CI before deployment. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
