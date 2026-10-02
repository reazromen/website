---
title: 'What selfHeal: true Buys You—and What It Does Not'
url: /posts/what-selfheal-true-buys-you-and-what-it-does-not.html
date: '2026-09-18'
read_time: 2
excerpt: The difference between correcting resource drift and fixing a broken application.
topic: voiceware-engineering
tags:
- voiceware
- argocd
- self-heal
- operations
draft: false
featured: false
language: en
eyebrow: 'Voiceware: ArgoCD & GitOps · deep-dive'
outputs:
- url: /posts/what-selfheal-true-buys-you-and-what-it-does-not.html
  template: cms/templates/posts/posts--what-selfheal-true-buys-you-and-what-it-does-not.tpl
  source: cms/templates/posts/posts--what-selfheal-true-buys-you-and-what-it-does-not.json
---

I want to go one layer deeper on **the difference between correcting resource drift and fixing a broken application**.

## Mental model

```
Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state
```

## What the repository proves

I enabled ArgoCD self-healing so declared resources reconciled back toward Git after manual drift.

## How the flow behaves

I traced this as **Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state** and checked repository revision and path, render status, desired/live diff, sync status, live resource health at each handoff. That kept the debugging path concrete.

## Failure scenarios

The main failure I am concerned with is: A controller can restore a changed Deployment spec while the application still fails because of bad code, bad data, or an unreachable dependency.

## Trade-offs

The root cause was this: A controller can restore a changed Deployment spec while the application still fails because of bad code, bad data, or an unreachable dependency. The practical lesson was simple: Self-healing protects declared state; it does not replace application health checks or operational diagnosis.

## What I check in practice

- Make release identity deterministic before relying on Git rollback.
- Verify repoURL, targetRevision, and path first.
- Inspect the desired/live diff before forcing a sync.
- Distinguish sync health from application health.
- Convert emergency manual changes back into Git.

If I remember one thing from this deep dive, it is **Self-healing protects declared state; it does not replace application health checks or operational diagnosis.** That is the kind of boring infrastructure I want: easy to explain, easy to inspect, and hard to misunderstand during an incident.
