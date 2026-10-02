---
title: Backup Freshness Is Not Backup Integrity
url: /posts/backup-freshness-is-not-backup-integrity.html
date: '2026-09-14'
read_time: 1
excerpt: A newly created directory can still be incomplete or corrupt, so age alone
  is weak recovery evidence.
topic: disaster-recovery
tags:
- backup
- integrity
- sha256
- dr
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · advanced'
outputs:
- url: /posts/backup-freshness-is-not-backup-integrity.html
  template: cms/templates/posts/posts--backup-freshness-is-not-backup-integrity.tpl
  source: cms/templates/posts/posts--backup-freshness-is-not-backup-integrity.json
---

The first backup posture check focused on whether a recent artifact existed. That could mark a backup healthy even if required files were missing or a partial directory was newer than the last complete set.

Freshness and integrity were treated as one property. A timestamp can prove recency; it cannot prove that PostgreSQL dumps, artifact archives, trust state and metadata are present and internally consistent. The checker now considers only completed timestamped backup directories, verifies required artifacts and validates SHA-256 manifests when present.

NIST and CISA recovery guidance emphasize testing backup availability and integrity, not merely creating copies. Recovery evidence should prove that the expected set exists and can be trusted. Define the contents of a valid backup set as a contract and fail the posture check when any required member is empty, missing or checksum-invalid. The concrete hserver evidence is commit f10f5c7, so this note is tied to an actual production change rather than a hypothetical failure.
