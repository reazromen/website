---
title: UNKNOWN and FAIL Mean Different Things in Backup Monitoring
url: /posts/unknown-and-fail-different-backup-monitoring.html
date: '2023-01-31'
read_time: 1
excerpt: Protected evidence that a low-privilege checker cannot read should not be
  reported as healthy or corrupt.
topic: disaster-recovery
tags:
- backup
- unknown
- least-privilege
- monitoring
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · advanced'
outputs:
- url: /posts/unknown-and-fail-different-backup-monitoring.html
  template: cms/templates/posts/posts--unknown-and-fail-different-backup-monitoring.tpl
  source: cms/templates/posts/posts--unknown-and-fail-different-backup-monitoring.json
---

The posture logic distinguishes PASS, FAIL and UNKNOWN. Missing or corrupt visible evidence is FAIL; protected or unavailable evidence is UNKNOWN and explicitly must not be interpreted as healthy.

The backup evidence is intentionally protected, while the operator job is intentionally low privilege. A checker can therefore encounter both real backup failures and evidence it is not authorized to inspect. Binary health semantics would force a dangerous choice: call unreadable evidence healthy or call least-privilege access a backup failure.

Three-state monitoring preserves epistemic honesty. SRE tooling should separate 'bad' from 'not observed' so access-control hardening does not create false operational claims.

UI and automation should assign different actions to UNKNOWN and FAIL. Unknown may require privileged verification; fail requires backup remediation. The concrete hserver evidence is commit 4bc538f, so this note is tied to an actual production change rather than a hypothetical failure.
