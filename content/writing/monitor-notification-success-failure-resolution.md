---
title: Monitor Notification Success, Failure and Resolution Separately
url: /posts/monitor-notification-success-failure-resolution.html
date: '2026-09-14'
read_time: 1
excerpt: An alert can fire correctly and still never reach the operator if Alertmanager
  or the external delivery path fails.
topic: observability-monitoring
tags:
- alertmanager
- notification
- ntfy
- meta-monitoring
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Alerting & Notification · advanced'
outputs:
- url: /posts/monitor-notification-success-failure-resolution.html
  template: cms/templates/posts/posts--monitor-notification-success-failure-resolution.tpl
  source: cms/templates/posts/posts--monitor-notification-success-failure-resolution.json
---

An alert can fire correctly and still never reach the operator if Alertmanager or the external delivery path fails. The monitoring mistake would be to read one metric in isolation. `hserver alert-sink delivery counters by success, failure and resolved` is useful because it narrows the question, and delivery metrics close the loop between detection and human notification and also show whether resolved notifications are being sent.

In software operations this falls under end-to-end alerting observability. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Track notification outcomes as first-class metrics and alert on delivery failures using an independent enough path to avoid circular blindness. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `49ec1dd`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
