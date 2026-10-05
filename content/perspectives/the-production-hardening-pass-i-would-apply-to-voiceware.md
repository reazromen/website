---
title: The Production Hardening Pass I Would Apply to Voiceware
url: /posts/the-production-hardening-pass-i-would-apply-to-voiceware.html
date: '2026-01-06'
read_time: 3
excerpt: A prioritized list of reliability controls to layer onto the validated deployment
  foundation.
topic: voiceware-engineering
tags:
- voiceware
- production-readiness
- reliability
- kubernetes
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Operations & Lessons · deep-dive'
outputs:
- url: /posts/the-production-hardening-pass-i-would-apply-to-voiceware.html
  template: cms/templates/posts/posts--the-production-hardening-pass-i-would-apply-to-voiceware.tpl
  source: cms/templates/posts/posts--the-production-hardening-pass-i-would-apply-to-voiceware.json
---

This is the debugging order I used for **a prioritized list of reliability controls to layer onto the validated deployment foundation** in a Voiceware-like deployment.

## Goal

The goal is not to prove that one Kubernetes object exists. The goal is to prove the whole relevant contract from source definition to runtime behavior, while changing as little state as possible during diagnosis.

By that point I had the base in place: service separation, Helm packaging, and ArgoCD GitOps.

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

The problem came down to this: A functional deployment can still be fragile without health probes, resource policy, immutable releases, secret management, backups, and workload-specific telemetry. What I carried forward was this: Harden in risk order after the deployment model is understood; do not bury fundamental architecture problems under operational tooling.

I consider the incident closed only when the fix is represented in the correct source layer, the controller has converged, the runtime path is verified, and the root cause is documented. the repository represents a real implementation stage, not every possible production control. When I mention probes, immutable releases, resource policy, environment separation, secrets, autoscaling, backups, or richer telemetry, I am treating them as hardening layers. I do not want to rewrite the history and pretend they were all present in the early manifests. The useful story is how a working deployment model becomes progressively safer without losing clarity.

**Runbook rule:** Harden in risk order after the deployment model is understood; do not bury fundamental architecture problems under operational tooling. That is the kind of boring infrastructure I want: easy to explain, easy to inspect, and hard to misunderstand during an incident.
