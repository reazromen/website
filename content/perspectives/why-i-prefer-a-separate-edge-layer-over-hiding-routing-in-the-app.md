---
title: Why I Prefer a Separate Edge Layer Over Hiding Routing in the App
url: /posts/why-i-prefer-a-separate-edge-layer-over-hiding-routing-in-the-app.html
date: '2026-06-24'
read_time: 3
excerpt: The trade-off between fewer containers and clearer network responsibility.
topic: voiceware-engineering
tags:
- voiceware
- nginx
- edge
- architecture
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Data & Edge · deep-dive'
outputs:
- url: /posts/why-i-prefer-a-separate-edge-layer-over-hiding-routing-in-the-app.html
  template: cms/templates/posts/posts--why-i-prefer-a-separate-edge-layer-over-hiding-routing-in-the-app.tpl
  source: cms/templates/posts/posts--why-i-prefer-a-separate-edge-layer-over-hiding-routing-in-the-app.json
---

I learned more from the small Voiceware failures than from the clean architecture diagram. The final repository looks organized, but the useful engineering story is in the boundaries that had to be discovered and corrected.

This is the decision I am examining: **the trade-off between fewer containers and clearer network responsibility**.

## Context

I packaged Nginx separately using the standard Nginx image on port 80.

The decision mattered because Application frameworks can terminate HTTP directly, but combining edge policy and application behavior can complicate independent changes.

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

The primary downside is the failure mode already identified: Application frameworks can terminate HTTP directly, but combining edge policy and application behavior can complicate independent changes. The primary reason to keep the decision is the lesson: Keep routing concerns separate when they evolve differently from business logic and need their own operational controls.

I would also record what would make me revisit the decision: traffic growth, stronger availability targets, additional environments, security constraints, release complexity, or operational pain that the current model can no longer absorb cheaply.

## Revisit triggers

- Do not restart callers when the shared dependency is the failing layer.
- Choose NodePort/Ingress/LoadBalancer from requirements, not habit.
- Map who depends on the shared service.
- Keep private dependencies private by default.
- Test from the same network context as the caller.

A good infrastructure decision is not one that never changes. It is one whose assumptions are visible enough that the team knows when it should change. That lesson has been more reusable for me than any particular YAML pattern.
