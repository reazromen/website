---
title: Build, Release and Run Fail Differently
url: /posts/build-release-run-fail-differently.html
date: '2025-12-12'
read_time: 1
excerpt: Separating image construction, configuration injection and runtime startup
  makes failures easier to localize.
topic: production-engineering
tags:
- twelve-factor
- deployment
- docker
- debugging
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Reproducibility · intermediate'
outputs:
- url: /posts/build-release-run-fail-differently.html
  template: cms/templates/posts/posts--build-release-run-fail-differently.tpl
  source: cms/templates/posts/posts--build-release-run-fail-differently.json
---

The Twelve-Factor methodology explicitly separates build, release and run stages. That separation is valuable operationally because each stage has different inputs, rollback methods and evidence. Recent hserver work repeatedly showed that a deployment can fail before the service code ever runs: the image may be wrong, configuration may be missing, permissions may block mounts, or the runtime dependency may be unready.

When build, release and run are treated as one opaque step, every failure looks like 'the deployment broke'. The operator loses the ability to isolate which stage produced the bad state.

The deployment workflow validates source and Compose first, builds or pulls pinned artifacts, verifies runtime secrets and files, then starts services and runs health acceptance separately. CI should prove build inputs; release tooling should record configuration and artifact identity; runtime checks should verify service behavior. Keeping those evidence streams separate makes incident diagnosis much faster. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
