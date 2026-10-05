---
title: 'Deployment vs Service: The Two Kubernetes Objects Voiceware Needed First'
url: /posts/deployment-vs-service-the-two-kubernetes-objects-voiceware-needed-first.html
date: '2021-08-21'
read_time: 2
excerpt: The separation between process lifecycle and network reachability.
topic: voiceware-engineering
tags:
- voiceware
- kubernetes
- service
- deployment
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Kubernetes · deep-dive'
outputs:
- url: /posts/deployment-vs-service-the-two-kubernetes-objects-voiceware-needed-first.html
  template: cms/templates/posts/posts--deployment-vs-service-the-two-kubernetes-objects-voiceware-needed-first.tpl
  source: cms/templates/posts/posts--deployment-vs-service-the-two-kubernetes-objects-voiceware-needed-first.json
---

Voiceware gave me a recurring reminder that infrastructure bugs are usually contract bugs. Two layers each behave correctly according to their own assumptions, but the assumptions do not match.

## The simple model

I started with one web-app replica behind a ClusterIP Service on port 80, using the `voiceware-web-app` image.

## How it appeared in Voiceware

The practical risk was: Beginners often treat a Deployment and a Service as two versions of the same thing, which leads to confusing debugging. In practice, that kind of mismatch often produces misleading symptoms one layer away from the root cause. A networking-looking problem may start as a selector mismatch; an application-looking problem may actually be an image-resolution failure; a Kubernetes-looking problem may be a Helm render error.

Kubernetes is good at maintaining declared state, but it does not understand the intent behind that state. If I declare the wrong port, selector, image, or command, Kubernetes can faithfully keep the wrong thing running. The operational skill is learning which object owns which part of the behavior.

## Why it matters

```
Git desired state
  -> Deployment creates Pods
  -> Service selects Pods
  -> Endpoints represent reachable backends
  -> Client traffic reaches the process
```

## A concrete debugging example

What I learned was: A Deployment answers “how should this process run?” while a Service answers “how should other processes find it?” If I could not check a decision from a rendered manifest, controller status, endpoint list, process command, or workload-specific signal, it was still too vague to operate.

## The takeaway

When I work on this area, my practical checks are:

- Check ArgoCD source revision/path and compare desired state with live state.
- Verify dependency reachability from the same network context as the workload.
- Use immutable release identifiers when reproducibility and rollback matter.
- Render the Helm chart and inspect the concrete manifest before syncing it.

For Voiceware, the important lesson is not that one particular YAML shape is universally correct. It is that **A Deployment answers “how should this process run?” while a Service answers “how should other processes find it?”** For me, this is what platform engineering looks like in practice: reduce ambiguity at the boundaries and make the recovery path obvious.
