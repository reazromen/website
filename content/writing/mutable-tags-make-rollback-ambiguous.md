---
title: Mutable Tags Make Rollback Ambiguous
url: /posts/mutable-tags-make-rollback-ambiguous.html
date: '2025-07-08'
read_time: 1
excerpt: You cannot reliably roll back to yesterday's image if the tag you used yesterday
  points somewhere else today.
topic: production-engineering
tags:
- rollback
- docker
- oci
- release-engineering
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Reproducibility · advanced'
outputs:
- url: /posts/mutable-tags-make-rollback-ambiguous.html
  template: cms/templates/posts/posts--mutable-tags-make-rollback-ambiguous.tpl
  source: cms/templates/posts/posts--mutable-tags-make-rollback-ambiguous.json
---

A production rollback plan is weak when it names a tag instead of an immutable artifact. If the registry has moved the tag, the rollback command may fetch a build that was never tested in the original environment.

The rollback target was expressed as a label rather than an identity. That makes recovery depend on registry history and timing instead of a known accepted binary. The hserver acceptance model records validated image digests and the Git commit associated with the deployment. Rollback can therefore select a concrete revision instead of hoping a mutable tag still represents the previous release.

Release engineering treats artifacts as immutable and promotion as metadata around a fixed artifact. This is the same principle behind content-addressed firmware and digest-pinned containers. Every accepted deployment should have an explicit previous-good revision and artifact set. If the rollback procedure cannot name exact bytes, it is not yet a deterministic rollback procedure. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
