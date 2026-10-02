---
title: External Runtimes Still Need an Owner Even If They Live in Another Repository
url: /posts/external-runtimes-still-need-owner.html
date: '2026-09-14'
read_time: 1
excerpt: Repository boundaries should not become operational blind spots on a shared
  production host.
topic: production-engineering
tags:
- ownership
- voip
- inventory
- multi-repo
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · advanced'
outputs:
- url: /posts/external-runtimes-still-need-owner.html
  template: cms/templates/posts/posts--external-runtimes-still-need-owner.tpl
  source: cms/templates/posts/posts--external-runtimes-still-need-owner.json
---

Multi-repository systems need federated ownership rather than forced centralization. The operational inventory should be complete even when implementation ownership is distributed. Some hserver services are intentionally owned outside the main infrastructure subtree. The risk was that the central production documentation could omit them simply because their canonical source lived elsewhere.

Source ownership and host impact are different axes. A service can belong to another repository while still consuming host ports, storage, credentials and recovery time on hserver.

The ownership catalog includes external runtime families with their canonical source and recovery path instead of pretending every component must be copied into one repository. Require cross-repository references, health checks and backup classification for external runtimes before they are considered documented on the host. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
