---
title: Journal Cursor Persistence Prevented Duplicate Log Ingestion
url: /posts/journal-cursor-persistence-prevented-duplicate-log-ingestion.html
date: '2024-02-07'
read_time: 1
excerpt: Restarting a log collector can replay old journal entries or skip new ones
  if it does not persist its position correctly.
topic: observability-monitoring
tags:
- grafana-alloy
- journald
- cursor
- loki
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Logs & Security · advanced'
outputs:
- url: /posts/journal-cursor-persistence-prevented-duplicate-log-ingestion.html
  template: cms/templates/posts/posts--journal-cursor-persistence-prevented-duplicate-log-ingestion.tpl
  source: cms/templates/posts/posts--journal-cursor-persistence-prevented-duplicate-log-ingestion.json
---

Restarting a log collector can replay old journal entries or skip new ones if it does not persist its position correctly. On hserver the first signal I use for this question is `Alloy journal cursor state tested before and after restart`. The acceptance test proved the cursor survived restart, which made log continuity a verified behavior instead of an assumption.

The important part is interpretation rather than collecting another graph. stateful log-ingestion verification. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Persist collector state, restart it deliberately during acceptance, and compare cursor progress so upgrades do not silently duplicate or lose journal data. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
