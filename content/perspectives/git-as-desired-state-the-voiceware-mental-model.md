---
title: 'Git as Desired State: The Voiceware Mental Model'
url: /posts/git-as-desired-state-the-voiceware-mental-model.html
date: '2024-02-21'
read_time: 2
excerpt: Why a GitOps repo is more than a backup of manifests.
topic: voiceware-engineering
tags:
- voiceware
- gitops
- desired-state
- platform-engineering
draft: false
featured: false
language: en
eyebrow: 'Voiceware: ArgoCD & GitOps · deep-dive'
outputs:
- url: /posts/git-as-desired-state-the-voiceware-mental-model.html
  template: cms/templates/posts/posts--git-as-desired-state-the-voiceware-mental-model.tpl
  source: cms/templates/posts/posts--git-as-desired-state-the-voiceware-mental-model.json
---

Here is the simplest way I explain **why a GitOps repo is more than a backup of manifests**.

## The analogy

```
Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state
```

## How it appeared in Voiceware

I created per-service ArgoCD Applications, pointed them at the Helm chart paths, and enabled automated sync, pruning, and self-healing.

## Why it matters

If engineers regularly patch production without reconciling the patch back to Git, the supposed source of truth stops being true.

## A concrete way to reason about it

I traced this as **Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state** and checked repository revision and path, render status, desired/live diff, sync status, live resource health at each handoff. That kept the debugging path concrete.

If the repository path, rendered chart, desired/live diff, sync state, and live resources all lined up, I moved on to application behavior. If one of them did not, I stayed on that layer until I understood the mismatch.

## Practical test

- Inspect the desired/live diff before forcing a sync.
- Distinguish sync health from application health.
- Convert emergency manual changes back into Git.
- Make release identity deterministic before relying on Git rollback.
- Verify repoURL, targetRevision, and path first.

The short version is **Desired-state systems require cultural discipline as much as controller configuration.** That lesson has been more reusable for me than any particular YAML pattern.
