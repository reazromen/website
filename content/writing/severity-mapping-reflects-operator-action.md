---
title: Severity Mapping Should Reflect Operator Action
url: /posts/severity-mapping-reflects-operator-action.html
date: '2022-06-05'
read_time: 1
excerpt: If every alert is critical, operators lose the distinction between conditions
  that require immediate intervention and those that need scheduled review.
topic: observability-monitoring
tags:
- alert-severity
- sre
- alertmanager
- operations
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Alerting & Notification · advanced'
outputs:
- url: /posts/severity-mapping-reflects-operator-action.html
  template: cms/templates/posts/posts--severity-mapping-reflects-operator-action.tpl
  source: cms/templates/posts/posts--severity-mapping-reflects-operator-action.json
---

If every alert is critical, operators lose the distinction between conditions that require immediate intervention and those that need scheduled review. I ended up treating `warning and critical labels across hserver alert rules` as the useful observation point rather than relying on a generic service-up indicator. Severity is most useful when it maps to response urgency, blast radius and available time rather than how technically interesting the metric is.

This is a good example of action-oriented alert classification. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Define severity around required human action, keep thresholds documented, and downgrade noisy alerts instead of teaching operators to ignore critical pages. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `b65d5d4` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
