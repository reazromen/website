---
title: A Green Badge Needs an Expiration Time
url: /posts/green-badge-needs-expiration-time.html
date: '2026-09-14'
read_time: 1
excerpt: Operational evidence should age out automatically rather than remaining green
  until someone notices it is old.
topic: web-control-plane
tags:
- freshness
- ui
- evidence
- sre
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · advanced'
outputs:
- url: /posts/green-badge-needs-expiration-time.html
  template: cms/templates/posts/posts--green-badge-needs-expiration-time.tpl
  source: cms/templates/posts/posts--green-badge-needs-expiration-time.json
---

Observability evidence has a temporal scope. Freshness budgets are similar to cache TTLs: beyond the accepted age, the consumer must refresh rather than assume validity. The Command Center could display the last successful posture job indefinitely. During a later deployment, the same success badge might refer to evidence collected before several relevant changes.

The UI represented state but not validity duration. A PASS was being treated as a permanent property instead of a time-bounded observation.

Evidence policies now define maximum ages per job and calculate CURRENT, STALE, FAILED, IN\_PROGRESS or NOT\_RUN states for operator display. Attach max-age policy to every safety signal and let the system decay stale evidence automatically. Do not rely on color without age and timestamp context. The concrete hserver evidence is commit 3387a0e, so this note is tied to an actual production change rather than a hypothetical failure.
