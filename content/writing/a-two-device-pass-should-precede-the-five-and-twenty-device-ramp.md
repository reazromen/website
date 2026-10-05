---
title: A Two-Device Pass Should Precede the Five- and Twenty-Device Ramp
url: /posts/a-two-device-pass-should-precede-the-five-and-twenty-device-ramp.html
date: '2025-11-09'
read_time: 1
excerpt: Fleet growth should happen after the representative call path is stable on
  real hardware.
topic: loup-engineering
tags:
- fleet-ramp
- validation
- test-plan
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Factory & Production Validation · advanced'
outputs:
- url: /posts/a-two-device-pass-should-precede-the-five-and-twenty-device-ramp.html
  template: cms/templates/posts/posts--a-two-device-pass-should-precede-the-five-and-twenty-device-ramp.tpl
  source: cms/templates/posts/posts--a-two-device-pass-should-precede-the-five-and-twenty-device-ramp.json
---

The important detail in A Two-Device Pass Should Precede the Five- and Twenty-Device Ramp was not the component name but the contract around it. LOUP plans a staged progression from a local two-device call to five devices and then twenty.

The pair validates endpoint correctness; five units expose enrollment and repeated identity operations; twenty exercise fleet telemetry, simultaneous registrations, OTA targeting and operational debugging. Each stage should preserve the same known-good call test so scale does not hide a basic regression.

The acceptance test was written around observable behaviour rather than whether a task, container or peripheral merely reported that it had started. Evidence marker: `2-5-20-ramp`.

Production ramps should add one class of complexity at a time and carry forward the earlier acceptance tests. That gives the team a concrete acceptance condition and a rollback point rather than a subjective sense that the build is probably better.

## Project evidence

LOUP engineering marker: `2-5-20-ramp`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
