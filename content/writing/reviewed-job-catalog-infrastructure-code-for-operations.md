---
title: A Reviewed Job Catalog Is Infrastructure Code for Operations
url: /posts/reviewed-job-catalog-infrastructure-code-for-operations.html
date: '2021-12-03'
read_time: 1
excerpt: The safest operational button is one whose command, risk and parameters were
  already reviewed before the incident started.
topic: web-control-plane
tags:
- gitops
- job-catalog
- operations
- review
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · advanced'
outputs:
- url: /posts/reviewed-job-catalog-infrastructure-code-for-operations.html
  template: cms/templates/posts/posts--reviewed-job-catalog-infrastructure-code-for-operations.tpl
  source: cms/templates/posts/posts--reviewed-job-catalog-infrastructure-code-for-operations.json
---

Operators needed repeatable actions such as runtime summaries, posture checks and acceptance verification. Hard-coding those actions only in the web application would have made Git review and rollback weaker. Executable operational definitions are part of desired state. If they live only in a database or UI, the production control plane can drift away from the reviewed repository.

Job definitions live in Git and are synchronized into the portal, while the runner reads the reviewed definition again before execution.

Give every job a stable ID, risk classification, timeout, working directory, command array and parameter schema. Changes to operational power should require the same review discipline as application code. This combines GitOps with policy-as-code: the operation itself is versioned, reviewable and reproducible rather than being an opaque database record. The concrete hserver evidence is commit 9e6f8a5, so this note is tied to an actual production change rather than a hypothetical failure.
