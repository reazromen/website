---
title: Build Once, Promote the Same Image
url: /posts/build-once-promote-the-same-image.html
date: '2023-07-18'
read_time: 2
excerpt: Why I prefer environment configuration to change without rebuilding application
  bytes.
topic: voiceware-engineering
tags:
- voiceware
- ci-cd
- containers
- releases
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Containers · deep-dive'
outputs:
- url: /posts/build-once-promote-the-same-image.html
  template: cms/templates/posts/posts--build-once-promote-the-same-image.tpl
  source: cms/templates/posts/posts--build-once-promote-the-same-image.json
---

The architecture question is **why I prefer environment configuration to change without rebuilding application bytes**.

## Start with the boundary, not the tool

I kept image references in chart values so I could change release identity without rewriting the Deployment template.

## Runtime view

```
source -> image build -> registry identity -> Helm value -> node runtime pull -> container start
```

## Responsibilities

For this topic, the relevant responsibility is why I prefer environment configuration to change without rebuilding application bytes. The boundary is good when each side can be described without hand-waving: what it receives, what it produces, what it depends on, and what happens if it disappears.

## Interfaces and failure isolation

The failure I explicitly design against is: Rebuilding “the same version” for staging and production creates two artifacts that may differ despite sharing a version label. That is why I care about the interface, not only whether both pods are currently green.

## Scaling implications

The signals I would attach to this boundary are image reference, registry reachability, node pull events, image digest, running container image ID.

## Architecture review questions

- Do not pair mutable latest tags with assumptions about reproducibility.
- Promote the same built artifact across environments.
- Use an explicit registry/repository path.
- Prefer immutable tags or digests for releases.
- Verify the node can pull the artifact.

The design rule I keep is **Build once, identify immutably, and promote the exact artifact through environments.** That is the kind of boring infrastructure I want: easy to explain, easy to inspect, and hard to misunderstand during an incident.
