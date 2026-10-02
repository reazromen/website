---
title: My GitOps Debugging Order When ArgoCD Says Something Is Wrong
url: /posts/my-gitops-debugging-order-when-argocd-says-something-is-wrong.html
date: '2026-09-18'
read_time: 3
excerpt: A deterministic path from Application source to rendered chart to Kubernetes
  object to runtime process.
topic: voiceware-engineering
tags:
- voiceware
- argocd
- debugging
- runbook
draft: false
featured: false
language: en
eyebrow: 'Voiceware: ArgoCD & GitOps · deep-dive'
outputs:
- url: /posts/my-gitops-debugging-order-when-argocd-says-something-is-wrong.html
  template: cms/templates/posts/posts--my-gitops-debugging-order-when-argocd-says-something-is-wrong.tpl
  source: cms/templates/posts/posts--my-gitops-debugging-order-when-argocd-says-something-is-wrong.json
---

This is the debugging order I used for **a deterministic path from Application source to rendered chart to Kubernetes object to runtime process** in a Voiceware-like deployment.

## Goal

The goal is not to prove that one Kubernetes object exists. The goal is to prove the whole relevant contract from source definition to runtime behavior, while changing as little state as possible during diagnosis.

I created per-service ArgoCD Applications, pointed them at the Helm chart paths, and enabled automated sync, pruning, and self-healing.

## Expected flow

```
Git revision/path -> ArgoCD Application -> render -> diff -> sync -> live Kubernetes state
```

## Pre-checks

Before touching the system, capture the current Git revision, ArgoCD state, relevant Kubernetes events, pod status, endpoints, and recent logs. If the incident is intermittent, this snapshot may be the only useful state that survives a restart.

The primary signals for this runbook are repository revision and path, render status, desired/live diff, sync status, live resource health.

## Procedure

1. Verify repoURL, targetRevision, and path first.
2. Inspect the desired/live diff before forcing a sync.
3. Distinguish sync health from application health.
4. Convert emergency manual changes back into Git.
5. Make release identity deterministic before relying on Git rollback.

## Branch: the failure occurs before Kubernetes

If the Helm chart cannot render or ArgoCD cannot find the repository/path, stay in the delivery layer. Do not spend time on Services or application logs. Validate values, templates, repository routing, and the revision ArgoCD is reading.

## Branch: the pod never starts

Check scheduling events, image resolution, pull errors, container command, and required configuration. An application cannot be debugged if its process never executes.

## Branch: the pod runs but traffic/work does not arrive

Inspect labels, selectors, endpoints, ports, queue routing, or dependency connectivity depending on the workload. This is where an apparently healthy pod can coexist with a broken product path.

## Exit criteria

At the core, the issue was this: Jumping straight into pod logs can waste time when the real failure is an incorrect path, render error, or sync policy. The useful lesson was simple: Debug the delivery chain in order: source, render, sync, resource state, endpoints, application behavior.

I consider the incident closed only when the fix is represented in the correct source layer, the controller has converged, the runtime path is verified, and the root cause is documented. the repository represents a real implementation stage, not every possible production control. When I mention probes, immutable releases, resource policy, environment separation, secrets, autoscaling, backups, or richer telemetry, I am treating them as hardening layers. I do not want to rewrite the history and pretend they were all present in the early manifests. The useful story is how a working deployment model becomes progressively safer without losing clarity.

**Runbook rule:** Debug the delivery chain in order: source, render, sync, resource state, endpoints, application behavior. The tool is secondary. The contract between layers is what makes the system operable.
