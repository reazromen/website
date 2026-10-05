---
title: Why I Kept Audio, Workers, Redis, Nginx, and the Web App Separate
url: /posts/why-i-kept-audio-workers-redis-nginx-and-the-web-app-separate.html
date: '2025-06-27'
read_time: 2
excerpt: The operational reasons for not collapsing supporting services into one large
  deployment.
topic: voiceware-engineering
tags:
- voiceware
- architecture
- fault-isolation
- kubernetes
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Platform Architecture · deep-dive'
outputs:
- url: /posts/why-i-kept-audio-workers-redis-nginx-and-the-web-app-separate.html
  template: cms/templates/posts/posts--why-i-kept-audio-workers-redis-nginx-and-the-web-app-separate.tpl
  source: cms/templates/posts/posts--why-i-kept-audio-workers-redis-nginx-and-the-web-app-separate.json
---

## The decision

I packaged audio-fork, Redis, and Nginx separately: audio-fork on port 5001, Redis on 6379, and Nginx on 80.

## The alternatives

The problem was: A single deployment can look simpler on day one while making restarts, scaling, troubleshooting, and fault isolation harder later. In practice, that kind of mismatch often produces misleading symptoms one layer away from the root cause. A networking-looking problem may start as a selector mismatch; an application-looking problem may actually be an image-resolution failure; a Kubernetes-looking problem may be a Helm render error.

## When I would revisit it

The lesson was: Operational independence is often worth more than reducing the raw number of Kubernetes objects. If I could not check a decision from a rendered manifest, controller status, endpoint list, process command, or workload-specific signal, it was still too vague to operate.

## Decision checklist

When I work on this area, my practical checks are:

- Verify dependency reachability from the same network context as the workload.
- Use immutable release identifiers when reproducibility and rollback matter.
- Render the Helm chart and inspect the concrete manifest before syncing it.
- Check ArgoCD source revision/path and compare desired state with live state.

For Voiceware, the important lesson is not that one particular YAML shape is universally correct. It is that **Operational independence is often worth more than reducing the raw number of Kubernetes objects.** The value is not that Kubernetes can represent the object. The value is that the team can explain why the object exists and how to prove it is working.
