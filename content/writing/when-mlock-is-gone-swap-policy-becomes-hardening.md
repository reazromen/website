---
title: When mlock Is Gone, Swap Policy Becomes Part of Secret-Server Hardening
url: /posts/when-mlock-is-gone-swap-policy-becomes-hardening.html
date: '2025-03-04'
read_time: 1
excerpt: If the application cannot pin sensitive memory, the container and host memory
  policy becomes part of the threat model.
topic: security-secrets
tags:
- openbao
- swap
- memory
- docker
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · advanced'
outputs:
- url: /posts/when-mlock-is-gone-swap-policy-becomes-hardening.html
  template: cms/templates/posts/posts--when-mlock-is-gone-swap-policy-becomes-hardening.tpl
  source: cms/templates/posts/posts--when-mlock-is-gone-swap-policy-becomes-hardening.json
---

After adapting to the OpenBao 2.6 memory model, the next question was what replaced the protection we expected from mlock. Simply deleting an unsupported option would have fixed validation without preserving the security objective. The objective was preventing sensitive pages from being casually swapped out, while the previous mechanism was only one implementation of that objective. Treating mechanism and requirement as the same thing would have left a silent gap.

The container received equal memory and memory-swap limits plus zero swappiness, and the unnecessary IPC\_LOCK capability was removed. That reduced both swap exposure and privilege surface.

The service documentation now states the memory-model rationale alongside the Compose settings. Future upgrades can test the invariant directly instead of assuming the old directive must remain forever. Good hardening starts from invariants: define the property you need, then select controls supported by the current platform. This avoids cargo-cult security configuration that survives long after the underlying behavior changes. The concrete hserver evidence is commit 47464d4, so this note is tied to an actual production change rather than a hypothetical failure.
