---
title: Status Heartbeats Need Identity, Version and Health Context
url: /posts/status-heartbeats-need-identity-version-and-health-context.html
date: '2026-09-14'
read_time: 1
excerpt: A backend cannot manage a fleet from a last-seen timestamp alone.
topic: loup-engineering
tags:
- heartbeat
- fleet
- telemetry
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Provisioning & Backend · advanced'
outputs:
- url: /posts/status-heartbeats-need-identity-version-and-health-context.html
  template: cms/templates/posts/posts--status-heartbeats-need-identity-version-and-health-context.tpl
  source: cms/templates/posts/posts--status-heartbeats-need-identity-version-and-health-context.json
---

The important detail in Status Heartbeats Need Identity, Version and Health Context was not the component name but the contract around it. LOUP device status is useful when it reports who the device is, what firmware it runs and whether core subsystems reached an accepted state.

That information lets the backend distinguish offline units from old firmware, failed trials, blocked devices or healthy active devices. Heartbeats should remain compact and should not be allowed to mutate terminal OTA state without release-scoped evidence.

The acceptance test was written around observable behaviour rather than whether a task, container or peripheral merely reported that it had started. Evidence marker: `device-heartbeat`.

Fleet telemetry should describe current evidence; it should not become an ambiguous command channel. That gives the team a concrete acceptance condition and a rollback point rather than a subjective sense that the build is probably better.

## Project evidence

LOUP engineering marker: `device-heartbeat`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
