---
title: Deployment Records Without Commit SHAs Are Operational Debt
url: /posts/deployment-records-without-commit-shas-operational-debt.html
date: '2024-11-04'
read_time: 1
excerpt: When a deployment fails later, the first forensic question is which reviewed
  source revision actually produced it.
topic: production-engineering
tags:
- git
- audit
- deployment
- ops-portal
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Git and Provenance · intermediate'
outputs:
- url: /posts/deployment-records-without-commit-shas-operational-debt.html
  template: cms/templates/posts/posts--deployment-records-without-commit-shas-operational-debt.tpl
  source: cms/templates/posts/posts--deployment-records-without-commit-shas-operational-debt.json
---

The Command Center had deployment records whose operational status could be visible even when commit provenance was absent. That made the dashboard useful for timing but weak for reconstruction.

Traceability links requirement, change, artifact and runtime evidence. In infrastructure work, the commit hash is one of the simplest durable correlation keys available. A deployment event without a revision connects runtime change to a service but not to the exact desired-state definition that authorized the change.

The operator UX now calls out running, rollout, canary or succeeded deployments that lack a commit SHA, and production handoff requires the accepted Git revision to be recorded.

Make revision identity mandatory in deployment APIs and automation rather than an optional text field that operators must remember to fill in. The concrete hserver evidence is commit 3387a0e, so this note is tied to an actual production change rather than a hypothetical failure.
