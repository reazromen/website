---
title: 'Using HEAD in ArgoCD: Fast for Iteration, Risky Without Promotion Rules'
url: /posts/using-head-in-argocd-fast-for-iteration-risky-without-promotion-rules.html
date: '2023-04-19'
read_time: 3
excerpt: The trade-off of following the current branch head rather than pinning a
  release revision.
topic: voiceware-engineering
tags:
- voiceware
- argocd
- releases
- gitops
draft: false
featured: false
language: en
eyebrow: 'Voiceware: ArgoCD & GitOps · deep-dive'
outputs:
- url: /posts/using-head-in-argocd-fast-for-iteration-risky-without-promotion-rules.html
  template: cms/templates/posts/posts--using-head-in-argocd-fast-for-iteration-risky-without-promotion-rules.tpl
  source: cms/templates/posts/posts--using-head-in-argocd-fast-for-iteration-risky-without-promotion-rules.json
---

This is the decision I am examining: **the trade-off of following the current branch head rather than pinning a release revision**.

## Context

During the first iteration I used targetRevision: HEAD in ArgoCD while I was still shaping the deployment.

The decision mattered because Following HEAD makes changes flow quickly but couples deployment directly to branch movement.

## Options I consider

**Option A — keep the simplest current behavior.** This minimizes moving parts and is often the right choice while proving a migration path.

**Option B — introduce a stronger abstraction immediately.** This can improve long-term consistency, but it also adds another system to debug before the underlying workload contract is stable.

**Option C — keep the simple implementation, but make the boundary explicit and define the trigger for revisiting it.** This is often my preferred migration posture.

## Decision criteria

```
Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state
```

## Why the Voiceware implementation is useful signal

I traced this as **Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state** and checked repository revision and path, render status, desired/live diff, sync status, live resource health at each handoff. That kept the debugging path concrete.

The repository tells me what was actually chosen at that point in the project. It does not force me to argue that the choice is universal. Infrastructure decisions are contextual: an early test cluster, a production environment, and a multi-team platform may reasonably choose different levels of abstraction.

## Trade-offs I would write into the ADR

The primary downside is the failure mode already identified: Following HEAD makes changes flow quickly but couples deployment directly to branch movement. The primary reason to keep the decision is the lesson: As environments mature, define promotion and pinning rules that match the required rollback and audit guarantees.

I would also record what would make me revisit the decision: traffic growth, stronger availability targets, additional environments, security constraints, release complexity, or operational pain that the current model can no longer absorb cheaply.

## Revisit triggers

- Convert emergency manual changes back into Git.
- Make release identity deterministic before relying on Git rollback.
- Verify repoURL, targetRevision, and path first.
- Inspect the desired/live diff before forcing a sync.
- Distinguish sync health from application health.

A good infrastructure decision is not one that never changes. It is one whose assumptions are visible enough that the team knows when it should change. The tool is secondary. The contract between layers is what makes the system operable.
