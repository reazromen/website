---
title: One ArgoCD Application per Voiceware Service
url: /posts/one-argocd-application-per-voiceware-service.html
date: '2024-05-19'
read_time: 2
excerpt: The benefits and costs of independently reconciling each major workload.
topic: voiceware-engineering
tags:
- voiceware
- argocd
- architecture
- gitops
draft: false
featured: false
language: en
eyebrow: 'Voiceware: ArgoCD & GitOps · deep-dive'
outputs:
- url: /posts/one-argocd-application-per-voiceware-service.html
  template: cms/templates/posts/posts--one-argocd-application-per-voiceware-service.tpl
  source: cms/templates/posts/posts--one-argocd-application-per-voiceware-service.json
---

The architecture question is **the benefits and costs of independently reconciling each major workload**.

## Start with the boundary, not the tool

I created matching ArgoCD Applications for the web app, audio-fork, Celery Beat, high/standard/low workers, ESL, Filebeat, Nginx, and Redis.

## Runtime view

```
Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state
```

## Responsibilities

For this topic, the relevant responsibility is the benefits and costs of independently reconciling each major workload. The boundary is good when each side can be described without hand-waving: what it receives, what it produces, what it depends on, and what happens if it disappears.

## Interfaces and failure isolation

I traced this as **Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state** and checked repository revision and path, render status, desired/live diff, sync status, live resource health at each handoff. That kept the debugging path concrete.

The failure I explicitly design against is: A single giant application is easy to create but can make ownership, sync failures, and rollout scope less obvious. That is why I care about the interface, not only whether both pods are currently green.

## Scaling implications

The signals I would attach to this boundary are repository revision and path, render status, desired/live diff, sync status, live resource health.

## Architecture review questions

- Verify repoURL, targetRevision, and path first.
- Inspect the desired/live diff before forcing a sync.
- Distinguish sync health from application health.
- Convert emergency manual changes back into Git.
- Make release identity deterministic before relying on Git rollback.

The design rule I keep is **Per-service applications improve isolation when service boundaries are real, though they increase object count and coordination needs.** That is the kind of boring infrastructure I want: easy to explain, easy to inspect, and hard to misunderstand during an incident.
