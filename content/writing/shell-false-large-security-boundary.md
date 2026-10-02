---
title: shell=False Is a Small Setting with a Large Security Boundary
url: /posts/shell-false-large-security-boundary.html
date: '2026-09-14'
read_time: 1
excerpt: Passing an argument array directly to exec avoids an entire class of shell
  expansion and injection behavior.
topic: security-secrets
tags:
- python
- subprocess
- command-injection
- runner
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · advanced'
outputs:
- url: /posts/shell-false-large-security-boundary.html
  template: cms/templates/posts/posts--shell-false-large-security-boundary.tpl
  source: cms/templates/posts/posts--shell-false-large-security-boundary.json
---

Avoiding unnecessary interpreters is a classic secure-execution principle. Data should remain data instead of being re-parsed as code by an extra language layer. The dedicated ops runner executes approved host commands with parameters supplied through controlled portal requests. Introducing a shell between the runner and command would make quoting rules and metacharacters part of the security model.

A shell interprets strings; an exec-style process launch passes arguments. The former expands the space of possible behavior far beyond the reviewed command structure.

The runner uses `shell=False`, validates parameters and restricts executable interpreters to reviewed paths. Represent commands as arrays, validate every parameter against the job schema and reject any feature that requires concatenating untrusted input into a shell command line. The concrete hserver evidence is commit 9e6f8a5, so this note is tied to an actual production change rather than a hypothetical failure.
