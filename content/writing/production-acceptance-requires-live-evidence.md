---
title: Production Acceptance Requires Live Evidence, Not Code Review Alone
url: /posts/production-acceptance-requires-live-evidence.html
date: '2026-09-14'
read_time: 1
excerpt: A reviewed repository can still be disconnected from the state actually running
  on the host.
topic: production-engineering
tags:
- acceptance
- gitops
- runtime-evidence
- sre
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Production Acceptance · advanced'
outputs:
- url: /posts/production-acceptance-requires-live-evidence.html
  template: cms/templates/posts/posts--production-acceptance-requires-live-evidence.tpl
  source: cms/templates/posts/posts--production-acceptance-requires-live-evidence.json
---

The readiness audit explicitly rejected the idea that merged code equals production acceptance. Some services had good source definitions but missing activation steps; others were running with incomplete reproducibility evidence.

Desired state, deployed state and accepted state are three different milestones. Review proves intent; deployment proves application; acceptance proves the live result meets operational requirements. The acceptance rule requires reviewed Git revision, fresh runtime inventory, health checks, backup evidence, restore evidence appropriate to the service, secret checks and a rollback target.

Google SRE launch and troubleshooting practices emphasize evidence from the running system. GitOps also assumes continuous comparison between desired and actual state rather than equating the two. Create an explicit acceptance artifact after deployment and make production status depend on that evidence instead of the merge timestamp. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
