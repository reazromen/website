---
title: Local Images and Cluster Images Are Different Problems
url: /posts/local-images-and-cluster-images-are-different-problems.html
date: '2026-09-18'
read_time: 2
excerpt: Why “it exists on my machine” is irrelevant unless the node runtime can resolve
  the same artifact.
topic: voiceware-engineering
tags:
- voiceware
- containerd
- registry
- kubernetes
draft: false
featured: false
language: en
eyebrow: 'Voiceware: Containers · deep-dive'
outputs:
- url: /posts/local-images-and-cluster-images-are-different-problems.html
  template: cms/templates/posts/posts--local-images-and-cluster-images-are-different-problems.tpl
  source: cms/templates/posts/posts--local-images-and-cluster-images-are-different-problems.json
---

Here is the simplest way I explain **why “it exists on my machine” is irrelevant unless the node runtime can resolve the same artifact**.

## The analogy

```
source -> image build -> registry identity -> Helm value -> node runtime pull -> container start
```

## How it appeared in Voiceware

The containerd image-path bug made one boundary clear: an image that resolves locally is not automatically an image the cluster runtime can pull.

## Why it matters

Kubernetes schedules work onto nodes that may know nothing about a developer workstation’s local image cache.

## A concrete way to reason about it

If the signals image reference, registry reachability, node pull events, image digest, running container image ID agree with the expected flow, I can move to application-specific behavior. If they disagree, I stay at the infrastructure boundary until the mismatch is understood.

## Practical test

- Do not pair mutable latest tags with assumptions about reproducibility.
- Promote the same built artifact across environments.
- Use an explicit registry/repository path.
- Prefer immutable tags or digests for releases.
- Verify the node can pull the artifact.

The short version is **Validate the distribution path from build output to registry to node runtime explicitly.** That is the kind of boring infrastructure I want: easy to explain, easy to inspect, and hard to misunderstand during an incident.
