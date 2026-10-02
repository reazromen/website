---
title: AEC Startup Needs a Defined State
url: /posts/aec-startup-needs-a-defined-state.html
date: '2026-09-14'
read_time: 1
excerpt: The first seconds of a call should not depend on whatever history remains
  in DSP buffers.
topic: loup-engineering
tags:
- aec
- startup
- state
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: AEC & DSP · advanced'
outputs:
- url: /posts/aec-startup-needs-a-defined-state.html
  template: cms/templates/posts/posts--aec-startup-needs-a-defined-state.tpl
  source: cms/templates/posts/posts--aec-startup-needs-a-defined-state.json
---

The important detail in AEC Startup Needs a Defined State was not the component name but the contract around it. Call setup creates discontinuities: playback begins, microphone capture starts and the reference buffer may initially contain silence or stale samples.

Resetting filter state, reference queues and delay estimates at explicit call boundaries gives the algorithm a known starting point. Without that contract, one call can inherit state from the previous session and make failures intermittent.

The acceptance test was written around observable behaviour rather than whether a task, container or peripheral merely reported that it had started. Evidence marker: `aec-startup-state`.

Real-time DSP needs lifecycle semantics. Start, reset and stop behavior should be as deliberate as the steady-state algorithm. That gives the team a concrete acceptance condition and a rollback point rather than a subjective sense that the build is probably better.

## Project evidence

LOUP engineering marker: `aec-startup-state`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
