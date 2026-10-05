---
title: Port 5044 and the Difference Between Log Generation and Log Transport
url: /posts/port-5044-and-the-difference-between-log-generation-and-log-transport.html
date: '2020-05-13'
read_time: 2
excerpt: Separating application logging from the system that moves or ingests those
  logs.
topic: voiceware-engineering
tags:
- voiceware
- filebeat
- logging
- operations
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Observability · deep-dive'
outputs:
- url: /posts/port-5044-and-the-difference-between-log-generation-and-log-transport.html
  template: cms/templates/posts/posts--port-5044-and-the-difference-between-log-generation-and-log-transport.tpl
  source: cms/templates/posts/posts--port-5044-and-the-difference-between-log-generation-and-log-transport.json
---

Here is the simplest way I explain **separating application logging from the system that moves or ingests those logs**.

## The analogy

```
controller state -> Kubernetes state -> process state -> dependency state -> product outcome
```

## How it appeared in Voiceware

I packaged Filebeat separately using elastic/filebeat on port 5044.

## Why it matters

An application can write excellent logs while the logging pipeline silently fails to transport them.

## A concrete way to reason about it

I traced this as **controller state -> Kubernetes state -> process state -> dependency state -> product outcome** and checked ArgoCD diff/sync, Kubernetes events, pod logs, Service endpoints, workload-specific latency or backlog at each handoff. That kept the debugging path concrete.

If the signals ArgoCD diff/sync, Kubernetes events, pod logs, Service endpoints, workload-specific latency or backlog agree with the expected flow, I can move to application-specific behavior. If they disagree, I stay at the infrastructure boundary until the mismatch is understood.

## Practical test

- Capture events and logs before restarting.
- Keep deployment health separate from product health.
- Use commit history to preserve incident context.
- Instrument the workload-specific failure mode, not just CPU and memory.
- Classify the failing layer before changing anything.

The short version is **Observe both ends: log production at the workload and delivery through the collection pipeline.** The tool is secondary. The contract between layers is what makes the system operable.
