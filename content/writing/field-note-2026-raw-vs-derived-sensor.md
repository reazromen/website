---
title: Separate Raw Sensor Data from Interpreted State
url: /posts/field-note-2026-raw-vs-derived-sensor.html
date: '2026-03-21'
read_time: 2
excerpt: Presence, motion and occupancy are conclusions; retain enough underlying
  evidence to debug those conclusions.
topic: observability-monitoring
tags:
- sensors
- telemetry
- presence
- signal-processing-253474
draft: false
featured: false
language: en
eyebrow: Observability Field Notes · advanced
outputs:
- url: /posts/field-note-2026-raw-vs-derived-sensor.html
  template: cms/templates/posts/posts--field-note-2026-raw-vs-derived-sensor.tpl
  source: cms/templates/posts/posts--field-note-2026-raw-vs-derived-sensor.json
---

# Separate Raw Sensor Data from Interpreted State

Presence, motion and occupancy are conclusions; retain enough underlying evidence to debug those conclusions.

I keep this as a field note because the failure mode is easy to misclassify: only the final classifier label is stored. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Persist evidence and decision as separate fields.**

## Implementation pattern

Timestamp raw or minimally processed features, derived state and calibration context so false decisions can be reconstructed.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- raw evidence aligns with state timestamps
- calibration version is known
- false transitions can be reconstructed

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Persist evidence and decision as separate fields. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
