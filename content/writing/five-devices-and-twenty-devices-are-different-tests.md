---
title: Five Devices and Twenty Devices Are Different Tests
url: /posts/five-devices-and-twenty-devices-are-different-tests.html
date: '2026-09-14'
read_time: 1
excerpt: Fleet size introduces registration churn, simultaneous calls and operational
  visibility that a pair cannot show.
topic: loup-engineering
tags:
- fleet-test
- pbx
- scale
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: PBX & Network · advanced'
outputs:
- url: /posts/five-devices-and-twenty-devices-are-different-tests.html
  template: cms/templates/posts/posts--five-devices-and-twenty-devices-are-different-tests.tpl
  source: cms/templates/posts/posts--five-devices-and-twenty-devices-are-different-tests.json
---

The lab result behind Five Devices and Twenty Devices Are Different Tests changed the implementation more than the first hypothesis did. The LOUP ramp plan moves from two devices to five and then twenty rather than jumping directly from one successful call to a large fleet.

At five units, repeated enrollment, identity and call routing start to matter. At twenty, registration cadence, PBX resources, logs, OTA targeting and failure isolation become much more visible. Each stage should have acceptance metrics before adding the next set.

Reversibility stayed part of the experiment: preserve the previous artifact, make the change, then prove the new path before promoting it. Evidence marker: `5-device-20-device-ramp`.

Scale testing works best as a staircase. Each step should introduce a new operational question, not just more hardware. Preserving that distinction is what lets the project increase complexity without losing the ability to explain a regression.

## Project evidence

LOUP engineering marker: `5-device-20-device-ramp`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
