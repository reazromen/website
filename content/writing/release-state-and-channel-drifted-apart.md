---
title: Release State and Release Channel Drifted Apart
url: /posts/release-state-and-channel-drifted-apart.html
date: '2026-09-14'
read_time: 1
excerpt: A release promoted to STABLE was still carrying old channel metadata, creating
  two competing sources of truth.
topic: ota-fleet
tags:
- ota
- promotion
- state-machine
- metadata
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/release-state-and-channel-drifted-apart.html
  template: cms/templates/posts/posts--release-state-and-channel-drifted-apart.tpl
  source: cms/templates/posts/posts--release-state-and-channel-drifted-apart.json
---

When two attributes must satisfy an invariant, enforce them at the mutation boundary rather than relying on callers to remember both updates. This is state-model normalization even when separate columns are retained for query convenience. The release lifecycle could move from CANARY to STABLE while the separate channel field retained its previous value. The UI and assignment logic could then observe a stable state with canary channel metadata.

Two fields represented one operational concept but were updated independently. That creates state divergence even inside a single database transaction model.

Promotion now updates lifecycle state and channel together: CANARY maps to the canary channel and STABLE maps to the stable channel in the same change path. Add invariant tests covering every allowed transition and assert the derived fields after mutation. State machines should be tested as transitions, not just as isolated endpoint responses. The concrete hserver evidence is commit 4a4554c, so this note is tied to an actual production change rather than a hypothetical failure.
