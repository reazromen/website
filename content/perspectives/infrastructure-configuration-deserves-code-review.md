---
title: Infrastructure Configuration Deserves Code Review
url: /posts/infrastructure-configuration-deserves-code-review.html
date: '2026-09-18'
read_time: 3
excerpt: Why a one-line port, image, or sync-policy change can have production impact.
topic: voiceware-engineering
tags:
- voiceware
- code-review
- devops
- gitops
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Operations & Lessons · deep-dive'
outputs:
- url: /posts/infrastructure-configuration-deserves-code-review.html
  template: cms/templates/posts/posts--infrastructure-configuration-deserves-code-review.tpl
  source: cms/templates/posts/posts--infrastructure-configuration-deserves-code-review.json
---

This is the decision I am examining: **why a one-line port, image, or sync-policy change can have production impact**.

## Context

During the migration I fixed Helm nil-pointer rendering, the Nginx deployment, Celery configuration, containerd image paths, NodePort exposure, and the celery-low values and command.

The decision mattered because Small YAML diffs can change exposure, delete resources through pruning, or route workers to the wrong queue.

## Options I consider

**Option A — keep the simplest current behavior.** This minimizes moving parts and is often the right choice while proving a migration path.

**Option B — introduce a stronger abstraction immediately.** This can improve long-term consistency, but it also adds another system to debug before the underlying workload contract is stable.

**Option C — keep the simple implementation, but make the boundary explicit and define the trigger for revisiting it.** This is often my preferred migration posture.

## Decision criteria

```
change -> review -> deploy -> observe -> diagnose -> recover -> document
```

## Why the Voiceware implementation is useful signal

I traced this as **change -> review -> deploy -> observe -> diagnose -> recover -> document** and checked change diff, deployment status, product behavior, recovery time, repeatability from clean state at each handoff. That kept the debugging path concrete.

The repository tells me what was actually chosen at that point in the project. It does not force me to argue that the choice is universal. Infrastructure decisions are contextual: an early test cluster, a production environment, and a multi-team platform may reasonably choose different levels of abstraction.

## Trade-offs I would write into the ADR

The primary downside is the failure mode already identified: Small YAML diffs can change exposure, delete resources through pruning, or route workers to the wrong queue. The primary reason to keep the decision is the lesson: Review infrastructure by blast radius and semantics, not by line count.

I would also record what would make me revisit the decision: traffic growth, stronger availability targets, additional environments, security constraints, release complexity, or operational pain that the current model can no longer absorb cheaply.

## Revisit triggers

- Change one layer at a time during migration.
- Review infrastructure by blast radius, not line count.
- Define rollback before the risky change.
- Keep secrets out of plaintext Git.
- Document what is implemented versus what remains a hardening next step.

A good infrastructure decision is not one that never changes. It is one whose assumptions are visible enough that the team knows when it should change. Once the boundary is explicit, both automation and debugging get simpler.
