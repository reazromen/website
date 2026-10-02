---
title: A Sticky Heartbeat Result Almost Became a False OTA Rollback
url: /posts/sticky-heartbeat-result-false-ota-rollback.html
date: '2026-09-14'
read_time: 1
excerpt: Telemetry from a previous release must not be allowed to mutate the state
  of a newly assigned release.
topic: ota-fleet
tags:
- ota
- state-machine
- heartbeat
- rollback
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/sticky-heartbeat-result-false-ota-rollback.html
  template: cms/templates/posts/posts--sticky-heartbeat-result-false-ota-rollback.tpl
  source: cms/templates/posts/posts--sticky-heartbeat-result-false-ota-rollback.json
---

The OTA heartbeat carried a `last_ota_result` string that could persist across release assignments. If the previous result said rollback or validation failure, the server could incorrectly apply that terminal meaning to the current assignment.

The event lacked a strong causal key. Human-readable result text was sticky state, while the database transition being attempted belonged to a specific release assignment. Terminal rollback and validation-failure transitions were removed from the heartbeat path. Only the release-scoped events endpoint can report those outcomes, while heartbeat may confirm ACTIVE only when the running release ID matches the assigned release.

Distributed state machines need correlation identifiers. An observation should mutate state only when it proves it belongs to the same entity and version whose state is being changed. Keep telemetry and authoritative events separate, carry release IDs through every terminal transition, and test reassignment scenarios where old device state survives into a new rollout. The concrete hserver evidence is commit a736702, so this note is tied to an actual production change rather than a hypothetical failure.
