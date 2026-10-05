---
title: Find Existing Before Create Is a Practical Reconciliation Pattern
url: /posts/find-existing-before-create-reconciliation-pattern.html
date: '2025-01-23'
read_time: 1
excerpt: When the remote API lacks your preferred idempotency primitive, deterministic
  discovery can recover an uncertain previous attempt.
topic: production-engineering
tags:
- reconciliation
- api
- publisher
- idempotency
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Data Integrity and Publishing · advanced'
outputs:
- url: /posts/find-existing-before-create-reconciliation-pattern.html
  template: cms/templates/posts/posts--find-existing-before-create-reconciliation-pattern.tpl
  source: cms/templates/posts/posts--find-existing-before-create-reconciliation-pattern.json
---

The reconciliation path queries recent remote posts, compares normalized content and verifies the destination account before deciding whether a matching post already exists.

The publisher integration could not assume every remote create call exposed an application-controlled idempotency key. That left a gap after timeouts or process restarts. The local database knew the intended content and target account but might not know the remote object ID if the response was lost.

Reconciliation is a common distributed-systems recovery technique: compare desired state with observed remote state and converge without assuming the previous command's result.

Keep the match criteria narrow enough to avoid false positives, persist the remote ID as soon as it is known, and prefer native idempotency keys when the provider supports them. The concrete hserver evidence is commit 9118e08, so this note is tied to an actual production change rather than a hypothetical failure.
