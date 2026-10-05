---
title: A Failed Canary Must Block Stable Promotion
url: /posts/failed-canary-must-block-stable-promotion.html
date: '2025-06-14'
read_time: 1
excerpt: Success evidence loses meaning if failed or rolled-back assignments are ignored
  during promotion.
topic: ota-fleet
tags:
- canary
- rollback
- ota
- release-gate
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/failed-canary-must-block-stable-promotion.html
  template: cms/templates/posts/posts--failed-canary-must-block-stable-promotion.tpl
  source: cms/templates/posts/posts--failed-canary-must-block-stable-promotion.json
---

A release can have one device active and another device failed. Looking only for one successful assignment would allow the stable gate to pass despite direct evidence of incompatibility or regression.

Release gates should encode negative evidence as well as positive evidence. In safety-oriented deployment systems, absence of failure is not equivalent to observed success, and observed success does not erase observed failure. The gate was a conjunction, not a single positive condition: there must be success evidence and there must not be unresolved bad evidence. Promotion checks both sides. STABLE requires an ACTIVE device and zero failed or rolled-back assignments for the release.

Test mixed-outcome scenarios explicitly. Canary logic should cover all-success, all-failure, partial-failure, stale-report and no-evidence cases before a rollout engine is trusted. The concrete hserver evidence is commit 4a4554c, so this note is tied to an actual production change rather than a hypothetical failure.
