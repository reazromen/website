---
title: Canary and Stable Are Different Release States
url: /posts/canary-and-stable-are-different-release-states.html
date: '2023-09-23'
read_time: 1
excerpt: A release that works on one device should not silently become the fleet default.
topic: loup-engineering
tags:
- canary
- stable
- fleet-ota
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: OTA & Release Engineering · advanced'
outputs:
- url: /posts/canary-and-stable-are-different-release-states.html
  template: cms/templates/posts/posts--canary-and-stable-are-different-release-states.tpl
  source: cms/templates/posts/posts--canary-and-stable-are-different-release-states.json
---

The acceptance condition for Canary and Stable Are Different Release States only became clear after the system was split into boundaries. LOUP OTA infrastructure separates canary rollout from stable promotion and requires active-device evidence before promotion.

A small group receives the candidate first, reports boot and validation status, and exposes failures before the release channel expands. Failed or rolled-back assignments block stable promotion rather than being averaged away by healthy devices.

The design became clearer when configuration, runtime state and recovery behaviour were specified separately instead of being implied by implementation details. Evidence marker: `canary-stable`.

Fleet confidence should grow with evidence. Promotion is a policy decision, not a filename change. Once that contract is written down, firmware and server changes can be reviewed against the same expectation instead of relying on memory.

## Project evidence

LOUP engineering marker: `canary-stable`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
