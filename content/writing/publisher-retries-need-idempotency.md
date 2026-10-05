---
title: Publisher Retries Need Idempotency or They Create Duplicate Posts
url: /posts/publisher-retries-need-idempotency.html
date: '2026-01-13'
read_time: 1
excerpt: When a network response is lost, retrying a create request can duplicate
  the side effect even if the first request succeeded remotely.
topic: production-engineering
tags:
- idempotency
- publisher
- http
- retries
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Data Integrity and Publishing · advanced'
outputs:
- url: /posts/publisher-retries-need-idempotency.html
  template: cms/templates/posts/posts--publisher-retries-need-idempotency.tpl
  source: cms/templates/posts/posts--publisher-retries-need-idempotency.json
---

RFC 9110 formalizes idempotency for HTTP methods, but application workflows often need their own idempotency key or reconciliation strategy for POST-like side effects. The content publisher had to recover from uncertain delivery states. If a remote create request succeeded but the local process missed the response, blindly retrying could create the same social post twice.

The workflow had at-least-once retry behavior around a non-idempotent create operation. Communication failure made the local system unable to distinguish 'not created' from 'created but response lost'.

Reconciliation now searches for an existing remote post with matching content and destination before creating a new delivery, then resumes schedule or publish actions on the existing object. Design retries before failures occur: identify a stable business key, record remote IDs durably and make every retry path safe to execute more than once. The concrete hserver evidence is commit 9118e08, so this note is tied to an actual production change rather than a hypothetical failure.
