---
title: Terminal OTA Events Need a Release ID
url: /posts/terminal-ota-events-need-release-id.html
date: '2023-06-06'
read_time: 1
excerpt: Rollback and validation failure are too important to infer from an unscoped
  status string.
topic: ota-fleet
tags:
- ota
- events
- release-id
- causality
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/terminal-ota-events-need-release-id.html
  template: cms/templates/posts/posts--terminal-ota-events-need-release-id.tpl
  source: cms/templates/posts/posts--terminal-ota-events-need-release-id.json
---

The OTA control plane originally allowed a heartbeat result such as `ROLLED_BACK` to drive a terminal assignment transition without proving which firmware release produced the result. The design conflated device-local memory with release-scoped event history. A terminal state change needs enough identity to answer: which device, which assignment and which release caused this transition?

Terminal outcomes moved to `/v1/events`, where the event includes the release identifier. The server can now reject or classify events using explicit release context instead of interpreting stale text.

Design event schemas from the audit question backward. If a future postmortem cannot determine which release generated a rollback, the event is missing required context. This is event correlation and causal consistency. Audit-worthy transitions should carry the object identity they mutate so later operators can reconstruct why the state changed. The concrete hserver evidence is commit a736702, so this note is tied to an actual production change rather than a hypothetical failure.
