---
title: Sticky Heartbeat Results Must Not Rewrite a New OTA Assignment
url: /posts/sticky-heartbeat-results-must-not-rewrite-a-new-ota-assignment.html
date: '2026-09-14'
read_time: 1
excerpt: Old local status text can outlive the release that originally produced it.
topic: loup-engineering
tags:
- heartbeat
- ota-state
- release-identity
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: OTA & Release Engineering · advanced'
outputs:
- url: /posts/sticky-heartbeat-results-must-not-rewrite-a-new-ota-assignment.html
  template: cms/templates/posts/posts--sticky-heartbeat-results-must-not-rewrite-a-new-ota-assignment.tpl
  source: cms/templates/posts/posts--sticky-heartbeat-results-must-not-rewrite-a-new-ota-assignment.json
---

The important detail in Sticky Heartbeat Results Must Not Rewrite a New OTA Assignment was not the component name but the contract around it. The OTA control plane was hardened so a heartbeat cannot use a stale `ROLLED_BACK` or validation string to terminally change a different release assignment.

Terminal failure events need release-scoped identity. Heartbeat can confirm that the assigned release is actually running, but rollback or validation failure transitions are authoritative through events carrying the release identifier.

The acceptance test was written around observable behaviour rather than whether a task, container or peripheral merely reported that it had started. Evidence marker: `stale-heartbeat-result`.

State machines need causality. A status without the identity of the action that produced it should not make irreversible decisions. That gives the team a concrete acceptance condition and a rollback point rather than a subjective sense that the build is probably better.

## Project evidence

LOUP engineering marker: `stale-heartbeat-result`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
