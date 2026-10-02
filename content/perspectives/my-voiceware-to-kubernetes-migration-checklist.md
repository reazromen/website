---
title: My Voiceware-to-Kubernetes Migration Checklist
url: /posts/my-voiceware-to-kubernetes-migration-checklist.html
date: '2026-09-18'
read_time: 3
excerpt: A practical sequence for moving a service without losing track of runtime
  assumptions.
topic: voiceware-engineering
tags:
- voiceware
- migration
- checklist
- kubernetes
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Operations & Lessons · deep-dive'
outputs:
- url: /posts/my-voiceware-to-kubernetes-migration-checklist.html
  template: cms/templates/posts/posts--my-voiceware-to-kubernetes-migration-checklist.tpl
  source: cms/templates/posts/posts--my-voiceware-to-kubernetes-migration-checklist.json
---

This is the debugging order I used for **a practical sequence for moving a service without losing track of runtime assumptions** in a Voiceware-like deployment.

## Goal

The goal is not to prove that one Kubernetes object exists. The goal is to prove the whole relevant contract from source definition to runtime behavior, while changing as little state as possible during diagnosis.

I split the runtime into the web app, audio-fork, Celery Beat, high/standard/low workers, ESL, Filebeat, Nginx, and Redis.

## Expected flow

```
change -> review -> deploy -> observe -> diagnose -> recover -> document
```

## Pre-checks

Before touching the system, capture the current Git revision, ArgoCD state, relevant Kubernetes events, pod status, endpoints, and recent logs. If the incident is intermittent, this snapshot may be the only useful state that survives a restart.

The primary signals for this runbook are change diff, deployment status, product behavior, recovery time, repeatability from clean state.

## Procedure

1. Change one layer at a time during migration.
2. Review infrastructure by blast radius, not line count.
3. Define rollback before the risky change.
4. Keep secrets out of plaintext Git.
5. Document what is implemented versus what remains a hardening next step.

## Branch: the failure occurs before Kubernetes

If the Helm chart cannot render or ArgoCD cannot find the repository/path, stay in the delivery layer. Do not spend time on Services or application logs. Validate values, templates, repository routing, and the revision ArgoCD is reading.

## Branch: the pod never starts

Check scheduling events, image resolution, pull errors, container command, and required configuration. An application cannot be debugged if its process never executes.

## Branch: the pod runs but traffic/work does not arrive

Inspect labels, selectors, endpoints, ports, queue routing, or dependency connectivity depending on the workload. This is where an apparently healthy pod can coexist with a broken product path.

## Exit criteria

What this came down to was this: Teams often migrate manifests before documenting commands, ports, dependencies, storage, health behavior, and exposure needs. From that I kept one rule: Inventory the runtime contract first; Kubernetes objects should encode what you already understand.

I consider the incident closed only when the fix is represented in the correct source layer, the controller has converged, the runtime path is verified, and the root cause is documented. the repository represents a real implementation stage, not every possible production control. When I mention probes, immutable releases, resource policy, environment separation, secrets, autoscaling, backups, or richer telemetry, I am treating them as hardening layers. I do not want to rewrite the history and pretend they were all present in the early manifests. The useful story is how a working deployment model becomes progressively safer without losing clarity.

**Runbook rule:** Inventory the runtime contract first; Kubernetes objects should encode what you already understand. For me, that is the practical difference between deploying containers and engineering a platform.
