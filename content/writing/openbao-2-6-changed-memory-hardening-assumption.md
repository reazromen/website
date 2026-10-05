---
title: OpenBao 2.6 Changed the Memory-Hardening Assumption
url: /posts/openbao-2-6-changed-memory-hardening-assumption.html
date: '2025-03-16'
read_time: 1
excerpt: Version-aware hardening matters because a security control can disappear
  or change semantics between releases.
topic: security-secrets
tags:
- openbao
- mlock
- containers
- hardening
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Permissions and Secrets · advanced'
outputs:
- url: /posts/openbao-2-6-changed-memory-hardening-assumption.html
  template: cms/templates/posts/posts--openbao-2-6-changed-memory-hardening-assumption.tpl
  source: cms/templates/posts/posts--openbao-2-6-changed-memory-hardening-assumption.json
---

The first OpenBao hardening model assumed an mlock-based configuration and container capability pattern that no longer matched OpenBao 2.6.x behavior. Carrying the old control forward produced a configuration that looked hardened but was based on an outdated runtime model.

The failure was an assumption drift between software version and operational policy. Security guidance is part of the software interface and must be revalidated when the version changes, especially around memory, privileges and kernel capabilities. We removed the obsolete mlock configuration and IPC\_LOCK capability, then set the container memory-swap limit equal to the memory limit with swappiness disabled. The replacement addressed the actual exposure model supported by the current release.

This is configuration compatibility testing: pin the exact version, read version-specific documentation, and validate the hardening model against the binary being deployed instead of copying controls from an older release. Image digests, documented version assumptions and CI config validation make this review repeatable. Security controls should have a rationale so an upgrade reviewer knows which behavior must be preserved even if the mechanism changes. The concrete hserver evidence is commit 47464d4, so this note is tied to an actual production change rather than a hypothetical failure.
