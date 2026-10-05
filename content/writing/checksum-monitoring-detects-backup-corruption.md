---
title: Checksum Monitoring Detects Silent Backup Corruption
url: /posts/checksum-monitoring-detects-backup-corruption.html
date: '2022-12-09'
read_time: 1
excerpt: A backup directory can exist with the expected filenames while one archive
  is truncated or modified after creation.
topic: observability-monitoring
tags:
- checksum
- backup-integrity
- dr
- monitoring
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Backup & DR · advanced'
outputs:
- url: /posts/checksum-monitoring-detects-backup-corruption.html
  template: cms/templates/posts/posts--checksum-monitoring-detects-backup-corruption.tpl
  source: cms/templates/posts/posts--checksum-monitoring-detects-backup-corruption.json
---

A backup directory can exist with the expected filenames while one archive is truncated or modified after creation. I ended up treating `hserver_backup_checksum_ok and checksum verification age` as the useful observation point rather than relying on a generic service-up indicator. Verifying the recorded manifest catches integrity failures that timestamp and file-size checks cannot reliably detect.

This is a good example of integrity monitoring. The purpose is to reduce ambiguity during an incident: a signal should tell me which layer to inspect next, not simply confirm that something somewhere looks unusual.

For production I use the following guardrail: Record the last successful checksum verification time, alert on failure, and treat unreadable evidence differently from a known-bad checksum. The same rule keeps the dashboard useful when the system grows and more targets are added.

The implementation is traceable to `f10f5c7` in the hserver repository. That commit is the concrete reference for the collector, alert, dashboard, or runtime change behind this article.
