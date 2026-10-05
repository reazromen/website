---
title: Rollback Is a Product Feature, Not a Bootloader Detail
url: /posts/field-note-2026-rollback-product-feature.html
date: '2026-04-25'
read_time: 2
excerpt: Recovery changes how safely a fleet can ship updates and how clearly operators
  can diagnose failures.
topic: production-ota-fleet
tags:
- rollback
- ota
- product-reliability
- esp32
draft: false
featured: false
language: en
eyebrow: OTA Field Notes · advanced
outputs:
- url: /posts/field-note-2026-rollback-product-feature.html
  template: cms/templates/posts/posts--field-note-2026-rollback-product-feature.tpl
  source: cms/templates/posts/posts--field-note-2026-rollback-product-feature.json
---

# Rollback Is a Product Feature, Not a Bootloader Detail

Recovery changes how safely a fleet can ship updates and how clearly operators can diagnose failures.

I keep this as a field note because the failure mode is easy to misclassify: bootloader recovery is invisible to the control plane. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Make rollback observable from device to operator.**

## Implementation pattern

Report the failed release and rollback event, restore service first, then preserve evidence for diagnosis.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- rollback reason is visible when possible
- failed release is not immediately forced again
- operators can identify recovered devices

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Make rollback observable from device to operator. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
