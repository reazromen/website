---
title: A Restore Drill Is Stronger Evidence Than a Successful Backup Command
url: /posts/restore-drill-stronger-than-successful-backup-command.html
date: '2022-03-19'
read_time: 1
excerpt: The backup process can exit zero while the recovery process is still incomplete,
  undocumented or impossible on another machine.
topic: disaster-recovery
tags:
- restore-drill
- rto
- dr
- verification
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · advanced'
outputs:
- url: /posts/restore-drill-stronger-than-successful-backup-command.html
  template: cms/templates/posts/posts--restore-drill-stronger-than-successful-backup-command.tpl
  source: cms/templates/posts/posts--restore-drill-stronger-than-successful-backup-command.json
---

As hserver became a real production host, backup counts stopped being a useful definition of recovery confidence. What mattered was whether a known set could be decrypted, validated and restored in the documented order. Backup creation tests the write path; disaster recovery exercises the read path, credentials, tooling, dependencies and operator procedure. Those are different systems.

The DR tooling verifies encrypted sets, dump formats and manifests, and the readiness plan calls for scheduled restore drills with recorded results and duration.

Record the recovery revision, elapsed time, missing steps and any manual intervention during each drill. Use those results to improve both RTO expectations and the runbook. NIST contingency guidance includes testing backup reliability and recovery procedures. SRE also treats failure testing as part of reliability engineering rather than documentation-only preparedness. The concrete hserver evidence is commit 4674311, so this note is tied to an actual production change rather than a hypothetical failure.
