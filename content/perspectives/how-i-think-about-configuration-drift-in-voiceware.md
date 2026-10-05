---
title: How I Think About Configuration Drift in Voiceware
url: /posts/how-i-think-about-configuration-drift-in-voiceware.html
date: '2025-03-16'
read_time: 3
excerpt: What drift is, how reconciliation changes it, and when a manual change is
  a warning sign.
topic: voiceware-engineering
tags:
- voiceware
- argocd
- drift
- operations
draft: false
featured: false
language: en
eyebrow: 'Voiceware: ArgoCD & GitOps · deep-dive'
outputs:
- url: /posts/how-i-think-about-configuration-drift-in-voiceware.html
  template: cms/templates/posts/posts--how-i-think-about-configuration-drift-in-voiceware.tpl
  source: cms/templates/posts/posts--how-i-think-about-configuration-drift-in-voiceware.json
---

The day-two operations question is **what drift is, how reconciliation changes it, and when a manual change is a warning sign**.

## Day-two reality

I created per-service ArgoCD Applications, pointed them at the Helm chart paths, and enabled automated sync, pruning, and self-healing.

Getting the first successful deployment is only the beginning. Operations starts when the system has to survive repeated releases, dependency failures, load changes, partial outages, and engineers who were not present during the original build.

## Signals

For this workload class I care about repository revision and path, render status, desired/live diff, sync status, live resource health. I want the signal to map to the actual failure mode, not just to whatever metric is easiest to collect.

```
Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state
```

## Failure scenarios

The primary risk is: Drift creates the classic “works in the cluster but not from a clean deployment” failure mode.

I also plan for partial failure. A controller can reconcile while the product is broken. A process can run while a dependency is slow. A queue can accept jobs while completion latency grows. An internal Service can resolve while no useful endpoint answers.

## Operational response

I traced this as **Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state** and checked repository revision and path, render status, desired/live diff, sync status, live resource health at each handoff. That kept the debugging path concrete.

I make the smallest change that addresses the layer with a concrete signal. If an emergency manual change is required, I treat it as temporary state and reconcile the intended fix back into Git afterward.

## Safer defaults

The issue was this: Drift creates the classic “works in the cluster but not from a clean deployment” failure mode. After that, I treated this as a rule: Every manual mutation should either be temporary and observed or be converted into a desired-state change.

## Runbook notes

- Inspect the desired/live diff before forcing a sync.
- Distinguish sync health from application health.
- Convert emergency manual changes back into Git.
- Make release identity deterministic before relying on Git rollback.
- Verify repoURL, targetRevision, and path first.

The operational principle is **Every manual mutation should either be temporary and observed or be converted into a desired-state change.** That is the kind of boring infrastructure I want: easy to explain, easy to inspect, and hard to misunderstand during an incident.
