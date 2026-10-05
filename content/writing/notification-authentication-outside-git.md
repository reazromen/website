---
title: Notification Authentication Belongs Outside Git
url: /posts/notification-authentication-outside-git.html
date: '2024-02-17'
read_time: 1
excerpt: Moving alert delivery to authenticated self-hosted ntfy introduced a publisher
  token that the alert-sink needs at runtime.
topic: observability-monitoring
tags:
- ntfy
- secrets
- alertmanager
- security
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Alerting & Notification · advanced'
outputs:
- url: /posts/notification-authentication-outside-git.html
  template: cms/templates/posts/posts--notification-authentication-outside-git.tpl
  source: cms/templates/posts/posts--notification-authentication-outside-git.json
---

Moving alert delivery to authenticated self-hosted ntfy introduced a publisher token that the alert-sink needs at runtime. On the finished hserver stack, `mode-0600 token file mounted read-only into alert-sink` is the signal that makes the difference visible. The delivery credential is operationally necessary but should not become configuration data or a Git secret simply because monitoring uses it.

The engineering pattern here is secret-managed observability. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Mount the token from a protected file, keep topic and endpoint configuration separate, and rotate the credential without rebuilding the application image. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `49ec1dd`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
