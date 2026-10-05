---
title: Notification Endpoint Health Needs Direct Monitoring
url: /posts/notification-endpoint-health-direct-monitoring.html
date: '2023-10-30'
read_time: 1
excerpt: Delivery counters only change when an alert is sent, so a quiet system could
  leave a dead notification service unnoticed for hours.
topic: observability-monitoring
tags:
- ntfy
- healthcheck
- notification
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Alerting & Notification · advanced'
outputs:
- url: /posts/notification-endpoint-health-direct-monitoring.html
  template: cms/templates/posts/posts--notification-endpoint-health-direct-monitoring.tpl
  source: cms/templates/posts/posts--notification-endpoint-health-direct-monitoring.json
---

Delivery counters only change when an alert is sent, so a quiet system could leave a dead notification service unnoticed for hours. The monitoring mistake would be to read one metric in isolation. `ntfy health probe plus Prometheus scrape target` is useful because it narrows the question, and direct service health closes the silent-period gap and provides evidence that the receiver is available even when no incidents are firing.

In software operations this falls under synthetic monitoring of the paging path. A dashboard becomes much more valuable when the operator knows what a rising line can prove, what it cannot prove, and which second signal should confirm the hypothesis.

My prevention rule is: Scrape or probe the notification service continuously and still retain real delivery counters because health does not prove message acceptance end to end. That keeps false positives lower without weakening visibility into real degradation.

The hserver source evidence is `49ec1dd`. Keeping that provenance matters because monitoring logic changes over time; the article should remain connected to the exact engineering decision it describes.
