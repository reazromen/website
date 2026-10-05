---
title: UNKNOWN Is Better Than a False FAIL When Metadata Is Restricted
url: /posts/unknown-better-than-false-fail-restricted-metadata.html
date: '2024-09-21'
read_time: 1
excerpt: A posture check should distinguish evidence it cannot read from evidence
  that proves the system is wrong.
topic: production-engineering
tags:
- observability
- git
- unknown
- sre
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · advanced'
outputs:
- url: /posts/unknown-better-than-false-fail-restricted-metadata.html
  template: cms/templates/posts/posts--unknown-better-than-false-fail-restricted-metadata.tpl
  source: cms/templates/posts/posts--unknown-better-than-false-fail-restricted-metadata.json
---

The first provenance checker could turn an inability to read worktree status into an apparent deployment failure. That made least-privilege execution look like configuration drift. The check had only pass/fail semantics even though its evidence sources could be unavailable independently. Missing evidence and negative evidence are not the same condition.

The script now tracks revision, branch, cleanliness and upstream comparison separately. If cleanliness cannot be inspected, it reports UNKNOWN while preserving any revision evidence that remains readable.

Define the semantics of every posture state in documentation and UI. Operators should know whether a result means safe, unsafe or not currently provable. Three-valued operational logic matters: PASS, FAIL and UNKNOWN carry different actions. SRE tooling should not manufacture certainty when permissions, telemetry or dependencies prevent observation. The concrete hserver evidence is commit e7b87ff, so this note is tied to an actual production change rather than a hypothetical failure.
