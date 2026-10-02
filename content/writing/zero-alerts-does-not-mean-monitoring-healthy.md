---
title: Zero Firing Alerts Does Not Mean Monitoring Is Healthy
url: /posts/zero-alerts-does-not-mean-monitoring-healthy.html
date: '2026-09-14'
read_time: 1
excerpt: A broken rule evaluator or missing target can produce a beautifully quiet
  alert dashboard while the system is blind.
topic: observability-monitoring
tags:
- meta-monitoring
- prometheus
- rule-evaluation
- blind-spots
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Alerting & Notification · advanced'
outputs:
- url: /posts/zero-alerts-does-not-mean-monitoring-healthy.html
  template: cms/templates/posts/posts--zero-alerts-does-not-mean-monitoring-healthy.tpl
  source: cms/templates/posts/posts--zero-alerts-does-not-mean-monitoring-healthy.json
---

A broken rule evaluator or missing target can produce a beautifully quiet alert dashboard while the system is blind. On the finished hserver stack, `rule evaluation failures, target availability and alert counts together` is the signal that makes the difference visible. Silence is trustworthy only when the monitoring machinery itself is healthy and collecting the expected data.

The engineering pattern here is monitoring the monitoring system. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Alert on rule-evaluation failures, target loss, log drops and notification failures so an empty alert list has evidential value. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
