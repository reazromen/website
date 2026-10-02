---
title: A Container Entrypoint Can Break a Perfectly Valid Validation Command
url: /posts/container-entrypoint-can-break-validation-command.html
date: '2026-09-14'
read_time: 1
excerpt: CI failed because the image entrypoint changed how arguments were interpreted,
  not because the OpenBao configuration was invalid.
topic: production-engineering
tags:
- ci
- docker
- openbao
- entrypoint
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · advanced'
outputs:
- url: /posts/container-entrypoint-can-break-validation-command.html
  template: cms/templates/posts/posts--container-entrypoint-can-break-validation-command.tpl
  source: cms/templates/posts/posts--container-entrypoint-can-break-validation-command.json
---

Deterministic CI removes ambient behavior: pin images, control entrypoints, create required fixtures explicitly and make the validation command identical every run. This is closely related to Twelve-Factor dev/prod parity and reproducible builds. The OpenBao configuration validation job was nondeterministic because the container image entrypoint participated in command construction. A command that looked correct in YAML could be interpreted differently by the image wrapper.

The validation environment had an implicit dependency on image entrypoint behavior. That is exactly the kind of hidden execution context that makes CI pass or fail for reasons unrelated to the configuration being tested.

The workflow now overrides the entrypoint explicitly with the OpenBao CLI binary and passes the validation subcommand directly. The test therefore exercises one known executable path. Any container used as a CI tool should be treated like a dependency with a public interface. If the test depends on an entrypoint side effect, encode that dependency or override it so upgrades cannot silently change test semantics. The concrete hserver evidence is commit 7cb23ee, so this note is tied to an actual production change rather than a hypothetical failure.
