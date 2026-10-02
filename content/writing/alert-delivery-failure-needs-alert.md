---
title: Alert Delivery Failure Needs an Alert of Its Own
url: /posts/alert-delivery-failure-needs-alert.html
date: '2026-09-14'
read_time: 1
excerpt: A monitoring system that detects failures but cannot notify anyone is partially
  failed even if every Prometheus target remains green.
topic: observability-monitoring
tags:
- meta-monitoring
- alertmanager
- notification-failure
- sre
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Alerting & Notification · advanced'
outputs:
- url: /posts/alert-delivery-failure-needs-alert.html
  template: cms/templates/posts/posts--alert-delivery-failure-needs-alert.tpl
  source: cms/templates/posts/posts--alert-delivery-failure-needs-alert.json
---

A monitoring system that detects failures but cannot notify anyone is partially failed even if every Prometheus target remains green. On hserver the first signal I use for this question is `HserverExternalNotificationDeliveryFailed from alert-sink failure counters`. The notification path is a production dependency and must be monitored from inside the observability system rather than assumed to work forever.

The important part is interpretation rather than collecting another graph. meta-monitoring of paging infrastructure. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Page or surface notification failures through an alternate visible channel and regularly test delivery with controlled synthetic alerts. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `49ec1dd`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
