---
title: A Single Redis Replica Is a Design Choice, Not a Default Truth
url: /posts/a-single-redis-replica-is-a-design-choice-not-a-default-truth.html
date: '2024-10-04'
read_time: 2
excerpt: How I interpret the current one-replica values and what changes when availability
  requirements grow.
topic: voiceware-engineering
tags:
- voiceware
- redis
- availability
- kubernetes
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Data & Edge · deep-dive'
outputs:
- url: /posts/a-single-redis-replica-is-a-design-choice-not-a-default-truth.html
  template: cms/templates/posts/posts--a-single-redis-replica-is-a-design-choice-not-a-default-truth.tpl
  source: cms/templates/posts/posts--a-single-redis-replica-is-a-design-choice-not-a-default-truth.json
---

This is the decision I am examining: **how I interpret the current one-replica values and what changes when availability requirements grow**.

## Context

I started Redis as a single replica in this deployment.

The decision mattered because One replica is simple and often appropriate for early deployment, but it does not provide datastore high availability by itself.

## Options I consider

**Option A — keep the simplest current behavior.** This minimizes moving parts and is often the right choice while proving a migration path.

**Option B — introduce a stronger abstraction immediately.** This can improve long-term consistency, but it also adds another system to debug before the underlying workload contract is stable.

**Option C — keep the simple implementation, but make the boundary explicit and define the trigger for revisiting it.** This is often my preferred migration posture.

## Decision criteria

```
external or internal client -> edge/service -> application -> shared dependency
```

## Why the Voiceware implementation is useful signal

The repository tells me what was actually chosen at that point in the project. It does not force me to argue that the choice is universal. Infrastructure decisions are contextual: an early test cluster, a production environment, and a multi-team platform may reasonably choose different levels of abstraction.

## Trade-offs I would write into the ADR

The primary downside is the failure mode already identified: One replica is simple and often appropriate for early deployment, but it does not provide datastore high availability by itself. The primary reason to keep the decision is the lesson: Availability design should follow data criticality, persistence requirements, recovery objectives, and operational budget.

I would also record what would make me revisit the decision: traffic growth, stronger availability targets, additional environments, security constraints, release complexity, or operational pain that the current model can no longer absorb cheaply.

## Revisit triggers

- Do not restart callers when the shared dependency is the failing layer.
- Choose NodePort/Ingress/LoadBalancer from requirements, not habit.
- Map who depends on the shared service.
- Keep private dependencies private by default.
- Test from the same network context as the caller.

A good infrastructure decision is not one that never changes. It is one whose assumptions are visible enough that the team knows when it should change. Once the boundary is explicit, both automation and debugging get simpler.
