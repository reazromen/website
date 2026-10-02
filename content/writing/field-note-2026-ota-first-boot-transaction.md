---
title: First Boot After OTA Is Still a Transaction
url: /posts/field-note-2026-ota-first-boot-transaction.html
date: '2026-09-18'
read_time: 2
excerpt: A successful flash write does not prove the new image can initialize hardware,
  load state and stay healthy.
topic: production-ota-fleet
tags:
- ota
- bootloader
- rollback
- firmware
draft: false
featured: false
language: en
eyebrow: OTA Field Notes · advanced
outputs:
- url: /posts/field-note-2026-ota-first-boot-transaction.html
  template: cms/templates/posts/posts--field-note-2026-ota-first-boot-transaction.tpl
  source: cms/templates/posts/posts--field-note-2026-ota-first-boot-transaction.json
---

# First Boot After OTA Is Still a Transaction

A successful flash write does not prove the new image can initialize hardware, load state and stay healthy.

I keep this as a field note because the failure mode is easy to misclassify: update success is declared before the new image has run. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Do not commit the update until the new image proves it can run.**

## Implementation pattern

Boot the inactive slot as pending, run bounded local validation, then accept or roll back.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- previous image remains bootable
- failure has deterministic rollback
- fleet distinguishes installed, booted and accepted

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Do not commit the update until the new image proves it can run. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
