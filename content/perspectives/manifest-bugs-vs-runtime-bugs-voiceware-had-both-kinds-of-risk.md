---
title: 'Manifest Bugs vs Runtime Bugs: Voiceware Had Both Kinds of Risk'
url: /posts/manifest-bugs-vs-runtime-bugs-voiceware-had-both-kinds-of-risk.html
date: '2026-09-18'
read_time: 2
excerpt: Separating incorrect desired state from a correctly declared process that
  behaves badly.
topic: voiceware-engineering
tags:
- voiceware
- debugging
- platform-engineering
- operations
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Observability · deep-dive'
outputs:
- url: /posts/manifest-bugs-vs-runtime-bugs-voiceware-had-both-kinds-of-risk.html
  template: cms/templates/posts/posts--manifest-bugs-vs-runtime-bugs-voiceware-had-both-kinds-of-risk.tpl
  source: cms/templates/posts/posts--manifest-bugs-vs-runtime-bugs-voiceware-had-both-kinds-of-risk.json
---

Here is the simplest way I explain **separating incorrect desired state from a correctly declared process that behaves badly**.

## The analogy

```
controller state -> Kubernetes state -> process state -> dependency state -> product outcome
```

## How it appeared in Voiceware

During the migration I fixed Helm nil-pointer rendering, the Nginx deployment, Celery configuration, containerd image paths, NodePort exposure, and the celery-low values and command.

## Why it matters

Infrastructure teams lose time when every problem is labeled “Kubernetes” even though some failures are application commands, values, images, or dependencies.

## A concrete way to reason about it

I traced this as **controller state -> Kubernetes state -> process state -> dependency state -> product outcome** and checked ArgoCD diff/sync, Kubernetes events, pod logs, Service endpoints, workload-specific latency or backlog at each handoff. That kept the debugging path concrete.

If the signals ArgoCD diff/sync, Kubernetes events, pod logs, Service endpoints, workload-specific latency or backlog agree with the expected flow, I can move to application-specific behavior. If they disagree, I stay at the infrastructure boundary until the mismatch is understood.

## Practical test

- Keep deployment health separate from product health.
- Use commit history to preserve incident context.
- Instrument the workload-specific failure mode, not just CPU and memory.
- Classify the failing layer before changing anything.
- Capture events and logs before restarting.

The short version is **Create a vocabulary for failure stage and insist on signal before changing layers.** The tool is secondary. The contract between layers is what makes the system operable.
