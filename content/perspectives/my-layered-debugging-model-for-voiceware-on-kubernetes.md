---
title: My Layered Debugging Model for Voiceware on Kubernetes
url: /posts/my-layered-debugging-model-for-voiceware-on-kubernetes.html
date: '2026-09-18'
read_time: 3
excerpt: A repeatable order for diagnosing delivery, scheduling, networking, dependencies,
  and application behavior.
topic: voiceware-engineering
tags:
- voiceware
- debugging
- kubernetes
- runbook
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Observability · deep-dive'
outputs:
- url: /posts/my-layered-debugging-model-for-voiceware-on-kubernetes.html
  template: cms/templates/posts/posts--my-layered-debugging-model-for-voiceware-on-kubernetes.tpl
  source: cms/templates/posts/posts--my-layered-debugging-model-for-voiceware-on-kubernetes.json
---

This is the debugging order I used for **a repeatable order for diagnosing delivery, scheduling, networking, dependencies, and application behavior** in a Voiceware-like deployment.

## Goal

The goal is not to prove that one Kubernetes object exists. The goal is to prove the whole relevant contract from source definition to runtime behavior, while changing as little state as possible during diagnosis.

During the migration I fixed Helm nil-pointer rendering, the Nginx deployment, Celery configuration, containerd image paths, NodePort exposure, and the celery-low values and command.

## Expected flow

```
controller state -> Kubernetes state -> process state -> dependency state -> product outcome
```

## Pre-checks

Before touching the system, capture the current Git revision, ArgoCD state, relevant Kubernetes events, pod status, endpoints, and recent logs. If the incident is intermittent, this snapshot may be the only useful state that survives a restart.

The primary signals for this runbook are ArgoCD diff/sync, Kubernetes events, pod logs, Service endpoints, workload-specific latency or backlog.

## Procedure

1. Classify the failing layer before changing anything.
2. Capture events and logs before restarting.
3. Keep deployment health separate from product health.
4. Use commit history to preserve incident context.
5. Instrument the workload-specific failure mode, not just CPU and memory.

## Branch: the failure occurs before Kubernetes

If the Helm chart cannot render or ArgoCD cannot find the repository/path, stay in the delivery layer. Do not spend time on Services or application logs. Validate values, templates, repository routing, and the revision ArgoCD is reading.

## Branch: the pod never starts

Check scheduling events, image resolution, pull errors, container command, and required configuration. An application cannot be debugged if its process never executes.

## Branch: the pod runs but traffic/work does not arrive

Inspect labels, selectors, endpoints, ports, queue routing, or dependency connectivity depending on the workload. This is where an apparently healthy pod can coexist with a broken product path.

## Exit criteria

The issue was this: Randomly restarting components hides signal and mixes independent failure domains. After that, I treated this as a rule: Use a fixed ladder: Git/ArgoCD, Helm render, Kubernetes resource, pod process, Service endpoints, dependency path, application semantics.

I consider the incident closed only when the fix is represented in the correct source layer, the controller has converged, the runtime path is verified, and the root cause is documented. the repository represents a real implementation stage, not every possible production control. When I mention probes, immutable releases, resource policy, environment separation, secrets, autoscaling, backups, or richer telemetry, I am treating them as hardening layers. I do not want to rewrite the history and pretend they were all present in the early manifests. The useful story is how a working deployment model becomes progressively safer without losing clarity.

**Runbook rule:** Use a fixed ladder: Git/ArgoCD, Helm render, Kubernetes resource, pod process, Service endpoints, dependency path, application semantics. The goal is not more Kubernetes. The goal is less ambiguity.
