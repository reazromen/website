---
title: Automated Sync Changed the Way I Thought About Deployment
url: /posts/automated-sync-changed-the-way-i-thought-about-deployment.html
date: '2022-08-04'
read_time: 2
excerpt: Moving from imperative deploy commands to controller-driven convergence.
topic: voiceware-engineering
tags:
- voiceware
- argocd
- automation
- gitops
draft: false
featured: false
language: en
eyebrow: 'Voiceware: ArgoCD & GitOps · deep-dive'
outputs:
- url: /posts/automated-sync-changed-the-way-i-thought-about-deployment.html
  template: cms/templates/posts/posts--automated-sync-changed-the-way-i-thought-about-deployment.tpl
  source: cms/templates/posts/posts--automated-sync-changed-the-way-i-thought-about-deployment.json
---

Looking back, the part I would preserve from the Voiceware work is **moving from imperative deploy commands to controller-driven convergence**.

## Before

The early mental model was naturally simpler: get the workload running, expose the right port, and keep moving. That is a reasonable way to start, but it leaves many contracts implicit until the first failure makes them visible.

## What happened

I created per-service ArgoCD Applications, pointed them at the Helm chart paths, and enabled automated sync, pruning, and self-healing.

## What changed

When a human is the only reconciler, the running cluster accumulates hidden differences from source control.

I traced this as **Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state** and checked repository revision and path, render status, desired/live diff, sync status, live resource health at each handoff. That kept the debugging path concrete.

Once I started treating the deployment as a series of boundaries instead of a pile of objects, the debugging process became much more deterministic. I could ask which layer introduced the wrong assumption and fix it there.

## What worked

The problem came down to this: When a human is the only reconciler, the running cluster accumulates hidden differences from source control. What I carried forward was this: Automated sync works best when Git changes are carefully because merge becomes part of the deployment path.

I would also keep the incremental nature of the work. The initial implementation does not need every production control. It needs enough structure that the next hardening step can be added without rewriting the system around undocumented state.

## What I learned to change earlier

I would add validation around the fragile contracts earlier: rendered Helm checks, explicit required values, immutable release identity, clearer environment strategy, and workload-specific health signals. Those controls are cheap compared with debugging the same category of mismatch repeatedly.

## Lessons I would reuse

- Inspect the desired/live diff before forcing a sync.
- Distinguish sync health from application health.
- Convert emergency manual changes back into Git.
- Make release identity deterministic before relying on Git rollback.
- Verify repoURL, targetRevision, and path first.

The retrospective lesson is **Automated sync works best when Git changes are carefully because merge becomes part of the deployment path.** That is the kind of boring infrastructure I want: easy to explain, easy to inspect, and hard to misunderstand during an incident.
