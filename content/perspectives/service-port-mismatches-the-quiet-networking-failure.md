---
title: 'Service Port Mismatches: The Quiet Networking Failure'
url: /posts/service-port-mismatches-the-quiet-networking-failure.html
date: '2025-08-12'
read_time: 2
excerpt: Why I verify listener, container port, Service port, and targetPort as one
  chain.
topic: voiceware-engineering
tags:
- voiceware
- ports
- kubernetes
- debugging
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Observability · deep-dive'
outputs:
- url: /posts/service-port-mismatches-the-quiet-networking-failure.html
  template: cms/templates/posts/posts--service-port-mismatches-the-quiet-networking-failure.tpl
  source: cms/templates/posts/posts--service-port-mismatches-the-quiet-networking-failure.json
---

## Symptom

I parameterized service ports and used the same values in both Deployment and Service templates.

The symptom pointed at the wrong layer. A pod can be running and DNS can resolve while traffic still fails because the transport contract is misaligned.

## My first rule: identify the stage of failure

```
controller state -> Kubernetes state -> process state -> dependency state -> product outcome
```

## What I checked

I checked ArgoCD diff/sync, Kubernetes events, pod logs, Service endpoints, workload-specific latency or backlog before changing anything.

I traced this as **controller state -> Kubernetes state -> process state -> dependency state -> product outcome** and checked ArgoCD diff/sync, Kubernetes events, pod logs, Service endpoints, workload-specific latency or backlog at each handoff. That kept the debugging path concrete.

## Where the problem actually was

The root cause was this: A pod can be running and DNS can resolve while traffic still fails because the transport contract is misaligned. The practical lesson was simple: Trace the exact port path end to end instead of assuming matching numbers.

## Prevention checklist

- Use commit history to preserve incident context.
- Instrument the workload-specific failure mode, not just CPU and memory.
- Classify the failing layer before changing anything.
- Capture events and logs before restarting.
- Keep deployment health separate from product health.
