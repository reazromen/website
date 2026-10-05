---
title: Observability Needs a Source of Truth and an Acceptance Artifact
url: /posts/observability-source-of-truth-acceptance-artifact.html
date: '2023-02-28'
read_time: 1
excerpt: A monitoring stack can drift through dashboard edits, local files and runtime
  tuning until nobody knows whether Git can reproduce what is currently trusted in
  production.
topic: observability-monitoring
tags:
- gitops
- observability
- acceptance
- reproducibility
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Observability Architecture · advanced'
outputs:
- url: /posts/observability-source-of-truth-acceptance-artifact.html
  template: cms/templates/posts/posts--observability-source-of-truth-acceptance-artifact.tpl
  source: cms/templates/posts/posts--observability-source-of-truth-acceptance-artifact.json
---

A monitoring stack can drift through dashboard edits, local files and runtime tuning until nobody knows whether Git can reproduce what is currently trusted in production. On the finished hserver stack, `Git-owned configuration plus acceptance.json runtime evidence` is the signal that makes the difference visible. The hserver design separates desired observability configuration from measured acceptance evidence such as targets, alert rules, retention, restore status and runtime memory.

The engineering pattern here is reproducible observability operations. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Keep dashboards, rules and configs in Git, keep secrets/runtime state out, and refresh an acceptance artifact after meaningful production changes. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
