---
title: 'What prune: true Means in a Real Repository'
url: /posts/what-prune-true-means-in-a-real-repository.html
date: '2026-09-18'
read_time: 2
excerpt: Why deleted desired-state resources should not silently live forever in the
  cluster.
topic: voiceware-engineering
tags:
- voiceware
- argocd
- prune
- gitops
draft: false
featured: false
language: en
eyebrow: 'Voiceware: ArgoCD & GitOps · deep-dive'
outputs:
- url: /posts/what-prune-true-means-in-a-real-repository.html
  template: cms/templates/posts/posts--what-prune-true-means-in-a-real-repository.tpl
  source: cms/templates/posts/posts--what-prune-true-means-in-a-real-repository.json
---

I want to go one layer deeper on **why deleted desired-state resources should not silently live forever in the cluster**.

## Mental model

```
Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state
```

## What the repository proves

I enabled automated pruning in the ArgoCD Applications.

## How the flow behaves

I traced this as **Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state** and checked repository revision and path, render status, desired/live diff, sync status, live resource health at each handoff. That kept the debugging path concrete.

## Failure scenarios

The main failure I am concerned with is: Without pruning, removing a manifest from Git may leave an orphaned runtime object that nobody remembers to manage.

## Trade-offs

At the core, the issue was this: Without pruning, removing a manifest from Git may leave an orphaned runtime object that nobody remembers to manage. The useful lesson was simple: Pruning closes the loop between “absent from desired state” and “absent from the cluster,” but it increases the need for careful review.

## What I check in practice

- Convert emergency manual changes back into Git.
- Make release identity deterministic before relying on Git rollback.
- Verify repoURL, targetRevision, and path first.
- Inspect the desired/live diff before forcing a sync.
- Distinguish sync health from application health.

If I remember one thing from this deep dive, it is **Pruning closes the loop between “absent from desired state” and “absent from the cluster,” but it increases the need for careful review.** For me, that is the practical difference between deploying containers and engineering a platform.
