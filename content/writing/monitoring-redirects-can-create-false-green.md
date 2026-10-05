---
title: Monitoring Redirects Can Create False Green Probes
url: /posts/monitoring-redirects-can-create-false-green.html
date: '2026-05-14'
read_time: 1
excerpt: A health probe that automatically follows redirects may end on an authentication
  page and report successful HTTP even though the original service route is wrong.
topic: observability-monitoring
tags:
- http-redirects
- health-probes
- authelia
- synthetic-monitoring
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Network & Edge · advanced'
outputs:
- url: /posts/monitoring-redirects-can-create-false-green.html
  template: cms/templates/posts/posts--monitoring-redirects-can-create-false-green.tpl
  source: cms/templates/posts/posts--monitoring-redirects-can-create-false-green.json
---

A health probe that automatically follows redirects may end on an authentication page and report successful HTTP even though the original service route is wrong. On the finished hserver stack, `runner and synthetic probes with redirect behavior controlled` is the signal that makes the difference visible. The monitoring client must preserve route semantics; otherwise an SSO redirect can look like application availability.

The engineering pattern here is contract-aware synthetic monitoring. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Disable redirect following where status codes are meaningful and assert the exact response class expected from each health endpoint. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `bdd8b2e`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
