---
title: One Deadlock Is Worth Recording
url: /posts/one-postgres-deadlock-worth-recording.html
date: '2020-10-29'
read_time: 1
excerpt: A PostgreSQL deadlock can resolve automatically by aborting one transaction,
  leaving the service apparently healthy after the incident.
topic: observability-monitoring
tags:
- postgresql
- deadlocks
- transactions
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Databases · advanced'
outputs:
- url: /posts/one-postgres-deadlock-worth-recording.html
  template: cms/templates/posts/posts--one-postgres-deadlock-worth-recording.tpl
  source: cms/templates/posts/posts--one-postgres-deadlock-worth-recording.json
---

A PostgreSQL deadlock can resolve automatically by aborting one transaction, leaving the service apparently healthy after the incident. The monitoring mistake would be to read one metric in isolation. `increase(hserver_postgres_deadlocks_total[15m])` is useful because it narrows the question, and deadlock counters preserve evidence of a concurrency failure that application success-rate graphs may quickly forget.

In software operations this falls under event-counter monitoring. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Alert on any new deadlock, capture application context, and fix lock ordering or transaction scope instead of treating retries as the permanent solution. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `b65d5d4`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
