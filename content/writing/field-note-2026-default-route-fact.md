---
title: The Default Route Is a Fact, Not a UI Guess
url: /posts/field-note-2026-default-route-fact.html
date: '2026-06-21'
read_time: 2
excerpt: A topology view should consume routing state rather than infer a gateway
  from labels or layout.
topic: networking
tags:
- routing
- default-route
- linux
- topology
draft: false
featured: false
language: en
eyebrow: Network Reliability Field Notes · advanced
outputs:
- url: /posts/field-note-2026-default-route-fact.html
  template: cms/templates/posts/posts--field-note-2026-default-route-fact.tpl
  source: cms/templates/posts/posts--field-note-2026-default-route-fact.json
---

# The Default Route Is a Fact, Not a UI Guess

A topology view should consume routing state rather than infer a gateway from labels or layout.

I keep this as a field note because the failure mode is easy to misclassify: presentation logic invents routing semantics. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Routing facts should enter through telemetry, not drawing heuristics.**

## Implementation pattern

Carry next hop, interface and route identity from the kernel or collector into the normalized topology model.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- next hop is observed
- overlay routes are separate
- moving a node cannot change semantics

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Routing facts should enter through telemetry, not drawing heuristics. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
