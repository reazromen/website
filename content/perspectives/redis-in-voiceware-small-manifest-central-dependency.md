---
title: 'Redis in Voiceware: Small Manifest, Central Dependency'
url: /posts/redis-in-voiceware-small-manifest-central-dependency.html
date: '2023-12-30'
read_time: 2
excerpt: Why an internal Redis service deserves explicit operational attention.
topic: voiceware-engineering
tags:
- voiceware
- redis
- kubernetes
- architecture
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Data & Edge · deep-dive'
outputs:
- url: /posts/redis-in-voiceware-small-manifest-central-dependency.html
  template: cms/templates/posts/posts--redis-in-voiceware-small-manifest-central-dependency.tpl
  source: cms/templates/posts/posts--redis-in-voiceware-small-manifest-central-dependency.json
---

The architecture question is **why an internal Redis service deserves explicit operational attention**.

## Start with the boundary, not the tool

I packaged Redis separately using the standard Redis image on port 6379.

## Runtime view

```
external or internal client -> edge/service -> application -> shared dependency
```

## Responsibilities

For this topic, the relevant responsibility is why an internal Redis service deserves explicit operational attention. The boundary is good when each side can be described without hand-waving: what it receives, what it produces, what it depends on, and what happens if it disappears.

## Interfaces and failure isolation

The failure I explicitly design against is: A dependency can have a tiny Kubernetes manifest and still sit on the critical path for queues, caching, or coordination. That is why I care about the interface, not only whether both pods are currently green.

## Scaling implications

The signals I would attach to this boundary are dependency reachability, connection failures, Service endpoints, edge response codes, shared-service saturation.

## Architecture review questions

- Test from the same network context as the caller.
- Do not restart callers when the shared dependency is the failing layer.
- Choose NodePort/Ingress/LoadBalancer from requirements, not habit.
- Map who depends on the shared service.
- Keep private dependencies private by default.

The design rule I keep is **Judge operational importance by dependency graph and failure impact, not by YAML size.** That is the kind of boring infrastructure I want: easy to explain, easy to inspect, and hard to misunderstand during an incident.
