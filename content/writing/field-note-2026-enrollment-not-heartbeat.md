---
title: Device Enrollment and Heartbeat Are Different Events
url: /posts/field-note-2026-enrollment-not-heartbeat.html
date: '2026-09-18'
read_time: 2
excerpt: Enrollment establishes trusted identity; heartbeat reports what an already
  known device is doing.
topic: production-ota-fleet
tags:
- enrollment
- heartbeat
- identity
- fleet
draft: false
featured: false
language: en
eyebrow: OTA Field Notes · advanced
outputs:
- url: /posts/field-note-2026-enrollment-not-heartbeat.html
  template: cms/templates/posts/posts--field-note-2026-enrollment-not-heartbeat.tpl
  source: cms/templates/posts/posts--field-note-2026-enrollment-not-heartbeat.json
---

# Device Enrollment and Heartbeat Are Different Events

Enrollment establishes trusted identity; heartbeat reports what an already known device is doing.

I keep this as a field note because the failure mode is easy to misclassify: the backend implicitly creates identity from the first heartbeat. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Enrollment creates trust; heartbeat uses trust.**

## Implementation pattern

Require an explicit enrollment transition and make unknown or retired identities fail closed at heartbeat.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- unknown devices cannot self-create
- retired state survives reconnects
- enrollment is separately auditable

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Enrollment creates trust; heartbeat uses trust. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
