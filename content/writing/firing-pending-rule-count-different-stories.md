---
title: Firing, Pending and Rule Count Tell Different Alerting Stories
url: /posts/firing-pending-rule-count-different-stories.html
date: '2026-09-14'
read_time: 1
excerpt: A dashboard that only shows firing alerts hides whether conditions are approaching
  thresholds or whether the expected rule set is even loaded.
topic: observability-monitoring
tags:
- prometheus-alerts
- pending
- rules
- grafana
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Alerting & Notification · advanced'
outputs:
- url: /posts/firing-pending-rule-count-different-stories.html
  template: cms/templates/posts/posts--firing-pending-rule-count-different-stories.tpl
  source: cms/templates/posts/posts--firing-pending-rule-count-different-stories.json
---

A dashboard that only shows firing alerts hides whether conditions are approaching thresholds or whether the expected rule set is even loaded. On hserver the first signal I use for this question is `Prometheus alert states plus total rule count`. Pending alerts show sustained-condition evaluation in progress, while rule count acts as a configuration sanity check for the monitoring control plane.

The important part is interpretation rather than collecting another graph. alert-pipeline observability. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Display firing, pending and loaded-rule totals together and investigate sudden rule-count changes after configuration deployment. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `b65d5d4`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
