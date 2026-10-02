---
title: Partial Backup Directories Should Not Win the 'Newest Backup' Contest
url: /posts/partial-backup-directories-not-newest-backup.html
date: '2026-09-14'
read_time: 1
excerpt: A failed job can leave a fresh-looking directory that should never replace
  the last known complete recovery point.
topic: disaster-recovery
tags:
- backup
- partial-files
- atomicity
- recovery
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · advanced'
outputs:
- url: /posts/partial-backup-directories-not-newest-backup.html
  template: cms/templates/posts/posts--partial-backup-directories-not-newest-backup.tpl
  source: cms/templates/posts/posts--partial-backup-directories-not-newest-backup.json
---

A backup job can create its destination directory before every dump and archive finishes. If the job dies halfway through, that directory may have the newest modification time despite being unusable. The posture algorithm originally selected by recency without enough completion semantics. Filesystem existence was being used as a commit marker.

The checker filters for timestamped backup-set directories and validates the required files before considering the set healthy. Incomplete evidence becomes FAIL rather than accidentally shadowing an older valid set.

Write backups into a temporary location, verify them, then publish or receipt the set only after completion. Consumers should read committed evidence, not infer completion from directory age. This is transactional thinking applied to files. A multi-file backup should have a completion invariant or atomic publication step so readers can distinguish committed sets from work in progress. The concrete hserver evidence is commit f10f5c7, so this note is tied to an actual production change rather than a hypothetical failure.
