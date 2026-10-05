---
title: Laptop-to-Desktop Failover Needs Agent State, Not Hope
url: /posts/field-note-2026-failover-agent-state.html
date: '2026-05-01'
read_time: 2
excerpt: A second worker is useful only if it knows what the first worker already
  changed.
topic: linux-homelab
tags:
- failover
- automation
- state
- homelab
draft: false
featured: false
language: en
eyebrow: Home Infrastructure Field Notes · advanced
outputs:
- url: /posts/field-note-2026-failover-agent-state.html
  template: cms/templates/posts/posts--field-note-2026-failover-agent-state.tpl
  source: cms/templates/posts/posts--field-note-2026-failover-agent-state.json
---

# Laptop-to-Desktop Failover Needs Agent State, Not Hope

A second worker is useful only if it knows what the first worker already changed.

I keep this as a field note because the failure mode is easy to misclassify: automation moves between machines without shared progress, locks or target state. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Fail over execution, not memory.**

## Implementation pattern

Persist target, revision, completed steps and destructive-operation locks outside the worker process.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- completed steps survive worker loss
- destructive steps are idempotent or locked
- fallback reaches the same targets

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Fail over execution, not memory. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
