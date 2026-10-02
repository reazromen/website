---
title: How I Recognize an Image-Pull Problem Before Blaming the App
url: /posts/how-i-recognize-an-image-pull-problem-before-blaming-the-app.html
date: '2026-09-18'
read_time: 2
excerpt: Using Kubernetes events and image references to separate runtime startup
  failures from application failures.
topic: voiceware-engineering
tags:
- voiceware
- containerd
- image-pull
- debugging
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Observability · deep-dive'
outputs:
- url: /posts/how-i-recognize-an-image-pull-problem-before-blaming-the-app.html
  template: cms/templates/posts/posts--how-i-recognize-an-image-pull-problem-before-blaming-the-app.tpl
  source: cms/templates/posts/posts--how-i-recognize-an-image-pull-problem-before-blaming-the-app.json
---

## Symptom

I fixed the web-app image path after containerd failed to resolve the original reference the way I expected.

The symptom pointed at the wrong layer. If the container never starts, application logs may not exist; debugging inside the app is wasted effort.

## My first rule: identify the stage of failure

```
controller state -> Kubernetes state -> process state -> dependency state -> product outcome
```

## What I checked

I checked ArgoCD diff/sync, Kubernetes events, pod logs, Service endpoints, workload-specific latency or backlog before changing anything.

I traced this as **controller state -> Kubernetes state -> process state -> dependency state -> product outcome** and checked ArgoCD diff/sync, Kubernetes events, pod logs, Service endpoints, workload-specific latency or backlog at each handoff. That kept the debugging path concrete.

## Where the problem actually was

At the core, the issue was this: If the container never starts, application logs may not exist; debugging inside the app is wasted effort. The useful lesson was simple: Check scheduling state, image resolution, and pull events before debugging code that has not executed.

## Prevention checklist

- Keep deployment health separate from product health.
- Use commit history to preserve incident context.
- Instrument the workload-specific failure mode, not just CPU and memory.
- Classify the failing layer before changing anything.
- Capture events and logs before restarting.
