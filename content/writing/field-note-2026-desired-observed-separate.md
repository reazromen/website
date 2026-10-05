---
title: Desired and Observed State Should Never Share a Field
url: /posts/field-note-2026-desired-observed-separate.html
date: '2026-03-20'
read_time: 2
excerpt: Operator intent and device-reported reality can disagree legitimately during
  rollout, reboot, outage or rollback.
topic: production-ota-fleet
tags:
- fleet
- state-model
- ota
- control-plane
draft: false
featured: false
language: en
eyebrow: OTA Field Notes · advanced
outputs:
- url: /posts/field-note-2026-desired-observed-separate.html
  template: cms/templates/posts/posts--field-note-2026-desired-observed-separate.tpl
  source: cms/templates/posts/posts--field-note-2026-desired-observed-separate.json
---

# Desired and Observed State Should Never Share a Field

Operator intent and device-reported reality can disagree legitimately during rollout, reboot, outage or rollback.

I keep this as a field note because the failure mode is easy to misclassify: assignment overwrites the same field later used for device-reported running state. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Model intent and observation separately, then reason about convergence.**

## Implementation pattern

Keep desired\_release\_id and running\_release\_id independent and derive status from their relationship.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- assignment does not alter observed state
- heartbeat cannot erase intent
- UI shows pending convergence

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Model intent and observation separately, then reason about convergence. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
