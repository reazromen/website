---
title: Back Up and Define Rollback Before You Touch Production
url: /posts/backup-and-rollback-before-touch-production.html
date: '2026-06-19'
read_time: 1
excerpt: The safest time to decide how to recover is before the change has modified
  the evidence you depend on.
topic: production-engineering
tags:
- change-management
- rollback
- backup
- deployment
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Production Acceptance · intermediate'
outputs:
- url: /posts/backup-and-rollback-before-touch-production.html
  template: cms/templates/posts/posts--backup-and-rollback-before-touch-production.tpl
  source: cms/templates/posts/posts--backup-and-rollback-before-touch-production.json
---

This is reversible change design and change-window discipline. Google SRE postmortem data shows configuration and binary pushes are major outage triggers, so deployment planning is itself a reliability control. Recent hserver deployments routinely touched stateful databases, trust material, authentication configuration and container definitions. Starting the edit first and inventing rollback later would make recovery depend on whatever state survived the failed change.

Change planning is often biased toward the success path. Failure-path inputs—backup, previous revision, config copy and restore order—must exist before the mutation begins.

Runbooks require preflight inventory, relevant backup, exact Git revision and a known rollback target before deployment, followed by health verification and documentation. Refuse high-risk changes when rollback inputs are missing. A change that cannot be reversed should be explicitly classified and receive stronger review. The concrete hserver evidence is commit fa3c478, so this note is tied to an actual production change rather than a hypothetical failure.
