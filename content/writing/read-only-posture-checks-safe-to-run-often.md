---
title: Read-Only Posture Checks Are Useful Because They Are Safe to Run Often
url: /posts/read-only-posture-checks-safe-to-run-often.html
date: '2026-09-14'
read_time: 1
excerpt: Observability improves when operators can refresh evidence without opening
  a risky change window.
topic: web-control-plane
tags:
- posture-check
- read-only
- sre
- operations
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · intermediate'
outputs:
- url: /posts/read-only-posture-checks-safe-to-run-often.html
  template: cms/templates/posts/posts--read-only-posture-checks-safe-to-run-often.tpl
  source: cms/templates/posts/posts--read-only-posture-checks-safe-to-run-often.json
---

Backup, DR, endpoint and production checks were most useful when operators could run them whenever evidence became stale. If collecting evidence changed the system, every diagnostic action would carry additional risk. Observation and mutation had not always been treated as separate operational capabilities. Safe diagnostics need different privilege and approval semantics from repairs. The portal exposes fixed LOW-risk posture jobs that read state, calculate evidence and write only their execution records.

Keep observation jobs side-effect free, document their evidence sources and create separate approved repair jobs when mutation is required. SRE troubleshooting works best when gathering evidence is cheap and repeatable. Read-only diagnostics reduce the temptation to 'fix while looking' before the failure has been localized. The concrete hserver evidence is commit 3c31a91, so this note is tied to an actual production change rather than a hypothetical failure.
