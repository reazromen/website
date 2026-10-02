---
title: A One-Line COPY Permission Bug Can Make an Image Non-Reproducible
url: /posts/copy-permission-bug-can-make-image-non-reproducible.html
date: '2026-09-14'
read_time: 1
excerpt: A configuration file copied with the wrong mode can behave differently depending
  on the build context and base image defaults.
topic: production-engineering
tags:
- dockerfile
- permissions
- supervisor
- ci
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Reproducibility · intermediate'
outputs:
- url: /posts/copy-permission-bug-can-make-image-non-reproducible.html
  template: cms/templates/posts/posts--copy-permission-bug-can-make-image-non-reproducible.tpl
  source: cms/templates/posts/posts--copy-permission-bug-can-make-image-non-reproducible.json
---

Build definitions should encode runtime invariants, not just file content. This fits the Twelve-Factor build/release/run separation: the build stage should create a release artifact with predictable metadata. The social publisher build had a supervisor configuration whose runtime readability depended on the mode produced by the build context. That kind of permission can vary after source extraction, packaging or a different developer workstation.

The Dockerfile described which file to copy but not the permission invariant required by the process consuming it. Reproducibility was therefore relying on metadata outside the Dockerfile.

The build now uses `COPY --chmod=644` for the supervisor configuration. The image itself establishes the intended permission instead of inheriting whatever mode happened to be present on the source filesystem. Files that have execution or readability requirements should declare them in the image build. A clean-build CI test can then verify behavior independently of the workstation that produced the source archive. The concrete hserver evidence is commit 484b33d, so this note is tied to an actual production change rather than a hypothetical failure.
