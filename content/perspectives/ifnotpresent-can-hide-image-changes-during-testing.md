---
title: IfNotPresent Can Hide Image Changes During Testing
url: /posts/ifnotpresent-can-hide-image-changes-during-testing.html
date: '2026-07-05'
read_time: 2
excerpt: How pull policy interacts with mutable image tags and node caches.
topic: voiceware-engineering
tags:
- voiceware
- image-pull-policy
- containers
- kubernetes
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Containers · deep-dive'
outputs:
- url: /posts/ifnotpresent-can-hide-image-changes-during-testing.html
  template: cms/templates/posts/posts--ifnotpresent-can-hide-image-changes-during-testing.tpl
  source: cms/templates/posts/posts--ifnotpresent-can-hide-image-changes-during-testing.json
---

I want to go one layer deeper on **how pull policy interacts with mutable image tags and node caches**.

## Mental model

```
source -> image build -> registry identity -> Helm value -> node runtime pull -> container start
```

## What the repository proves

The first charts commonly used imagePullPolicy: IfNotPresent, which made image identity especially important during testing.

## Failure scenarios

The main failure I am concerned with is: A node may keep an older cached image for a mutable tag, making two pods with the same manifest run different builds across time or nodes.

## Trade-offs

At the core, the issue was this: A node may keep an older cached image for a mutable tag, making two pods with the same manifest run different builds across time or nodes. The useful lesson was simple: Pair pull policy with immutable image identity; do not use pull policy to compensate for weak release tagging.

## What I check in practice

- Do not pair mutable latest tags with assumptions about reproducibility.
- Promote the same built artifact across environments.
- Use an explicit registry/repository path.
- Prefer immutable tags or digests for releases.
- Verify the node can pull the artifact.

If I remember one thing from this deep dive, it is **Pair pull policy with immutable image identity; do not use pull policy to compensate for weak release tagging.** The tool is secondary. The contract between layers is what makes the system operable.
