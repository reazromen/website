---
title: Backup Age Is a Freshness Signal, Not a Recovery Guarantee
url: /posts/backup-age-freshness-not-recovery-guarantee.html
date: '2026-09-14'
read_time: 1
excerpt: A recent backup timestamp can look reassuring even when the archive is incomplete,
  corrupt or impossible to restore.
topic: observability-monitoring
tags:
- backup
- freshness
- dr
- prometheus
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Backup & DR · advanced'
outputs:
- url: /posts/backup-age-freshness-not-recovery-guarantee.html
  template: cms/templates/posts/posts--backup-age-freshness-not-recovery-guarantee.tpl
  source: cms/templates/posts/posts--backup-age-freshness-not-recovery-guarantee.json
---

A recent backup timestamp can look reassuring even when the archive is incomplete, corrupt or impossible to restore. On hserver the first signal I use for this question is `hserver_backup_last_success_unixtime`. Freshness answers when a backup last completed, while integrity and restore verification answer whether that backup is actually useful.

The important part is interpretation rather than collecting another graph. multi-signal backup monitoring. That gives the metric a specific operational job instead of making it another number on a dashboard.

The practical control is straightforward: Alert on stale age, but keep checksum and restore-verification state beside it so operators never equate recency with recoverability. This also gives me a repeatable check after deployments, exporter changes, or capacity tuning.

Repository evidence for this monitoring behavior is commit `f10f5c7`. I keep that reference with the note because a monitoring conclusion is stronger when the configuration and runtime decision that produced it can be inspected later.
