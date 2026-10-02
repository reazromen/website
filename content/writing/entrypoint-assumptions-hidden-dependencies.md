---
title: Entrypoint Assumptions Are Hidden Dependencies
url: /posts/entrypoint-assumptions-hidden-dependencies.html
date: '2026-09-14'
read_time: 1
excerpt: A container command is only reproducible when you know whether the image
  entrypoint wraps, replaces or transforms it.
topic: production-engineering
tags:
- docker
- entrypoint
- ci
- debugging
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Reproducibility · advanced'
outputs:
- url: /posts/entrypoint-assumptions-hidden-dependencies.html
  template: cms/templates/posts/posts--entrypoint-assumptions-hidden-dependencies.tpl
  source: cms/templates/posts/posts--entrypoint-assumptions-hidden-dependencies.json
---

OpenBao config validation failed for reasons unrelated to the configuration because the image entrypoint changed how the supplied command was executed. The YAML looked reasonable while the effective process tree was different from what the reviewer expected. The execution contract was split between our workflow and metadata inside the third-party image. Hidden defaults are convenient until a validation path needs exact behavior.

The CI job overrides the entrypoint and names the OpenBao CLI directly. That turns an implicit image convention into an explicit command boundary.

Tooling containers should be pinned and invoked through stable executable interfaces. If an entrypoint is part of the dependency, test it; if it is not, override it. When debugging container tooling, inspect the effective entrypoint and command before changing application arguments. Reproducible builds reduce hidden state by making interpreter, working directory and command path explicit. The concrete hserver evidence is commit 7cb23ee, so this note is tied to an actual production change rather than a hypothetical failure.
