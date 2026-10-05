---
title: Prometheus Labels Are Part of the API
url: /posts/field-note-2026-prometheus-labels-api.html
date: '2026-04-02'
read_time: 2
excerpt: Label names and cardinality are query contracts for dashboards, recording
  rules and alerts.
topic: observability-monitoring
tags:
- prometheus
- metrics
- labels
- grafana
draft: false
featured: false
language: en
eyebrow: Observability Field Notes · intermediate
outputs:
- url: /posts/field-note-2026-prometheus-labels-api.html
  template: cms/templates/posts/posts--field-note-2026-prometheus-labels-api.tpl
  source: cms/templates/posts/posts--field-note-2026-prometheus-labels-api.json
---

# Prometheus Labels Are Part of the API

Label names and cardinality are query contracts for dashboards, recording rules and alerts.

I keep this as a field note because the failure mode is easy to misclassify: labels are changed casually because the metric base name remains the same. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Design labels as a stable, bounded contract.**

## Implementation pattern

Use small categorical dimensions, avoid arbitrary user values and coordinate label changes with consumers.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- cardinality is bounded
- key selectors have smoke queries
- renames update consumers together

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Design labels as a stable, bounded contract. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
