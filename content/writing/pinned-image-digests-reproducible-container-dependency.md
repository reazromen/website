---
title: Pinned Image Digests Turn a Container Tag into a Reproducible Dependency
url: /posts/pinned-image-digests-reproducible-container-dependency.html
date: '2026-09-19'
read_time: 1
excerpt: A mutable tag tells you what to ask for; a digest tells you what bytes you
  actually accepted.
topic: production-engineering
tags:
- docker
- oci
- supply-chain
- gitops
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Reproducibility · advanced'
outputs:
- url: /posts/pinned-image-digests-reproducible-container-dependency.html
  template: cms/templates/posts/posts--pinned-image-digests-reproducible-container-dependency.tpl
  source: cms/templates/posts/posts--pinned-image-digests-reproducible-container-dependency.json
---

Several hserver deployments initially depended on image tags that could move between pulls. The same Compose file could therefore produce a different runtime days later without any Git change. The source of truth was versioned while one of its largest dependencies was not. That breaks forensic reasoning because a commit hash cannot uniquely identify the binary set that was actually deployed.

Accepted production images were pinned to validated OCI digests and runtime documentation records image IDs or RepoDigests alongside the Git revision. Rebuilds can now request the exact artifact that passed acceptance.

Promotion should record both source revision and artifact identity. Upgrades become explicit changes with their own validation instead of invisible consequences of pulling `latest` again. This is dependency pinning and artifact immutability. GitOps requires versioned desired state, and that principle is incomplete if the desired state contains mutable external references. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
