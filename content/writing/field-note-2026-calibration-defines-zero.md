---
title: Calibration Defines Zero; Detection Measures Deviation
url: /posts/field-note-2026-calibration-defines-zero.html
date: '2026-09-18'
read_time: 2
excerpt: The useful baseline is the room's normal operating condition, not an imaginary
  perfectly quiet environment.
topic: observability-monitoring
tags:
- calibration
- sensors
- baseline
- presence
draft: false
featured: false
language: en
eyebrow: Observability Field Notes · intermediate
outputs:
- url: /posts/field-note-2026-calibration-defines-zero.html
  template: cms/templates/posts/posts--field-note-2026-calibration-defines-zero.tpl
  source: cms/templates/posts/posts--field-note-2026-calibration-defines-zero.json
---

# Calibration Defines Zero; Detection Measures Deviation

The useful baseline is the room's normal operating condition, not an imaginary perfectly quiet environment.

I keep this as a field note because the failure mode is easy to misclassify: steady fans, monitors or background conditions are treated as permanent events. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Define zero from the environment, then measure deviation from zero.**

## Implementation pattern

Persist baseline statistics from the normal room and compare live windows against that local reference.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- baseline values are visible
- steady normal equipment does not trigger
- movement produces measurable deviation

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Define zero from the environment, then measure deviation from zero. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
