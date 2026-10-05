---
title: Backup Size History Can Reveal Missing Data
url: /posts/backup-size-history-reveal-missing-data.html
date: '2020-12-23'
read_time: 1
excerpt: A backup that suddenly becomes much smaller may have completed successfully
  while silently omitting a database, artifact directory or other expected state.
topic: observability-monitoring
tags:
- backup-size
- anomaly-detection
- dr
- grafana
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Backup & DR · advanced'
outputs:
- url: /posts/backup-size-history-reveal-missing-data.html
  template: cms/templates/posts/posts--backup-size-history-reveal-missing-data.tpl
  source: cms/templates/posts/posts--backup-size-history-reveal-missing-data.json
---

A backup that suddenly becomes much smaller may have completed successfully while silently omitting a database, artifact directory or other expected state. On the finished hserver stack, `hserver_backup_size_bytes over time` is the signal that makes the difference visible. Size is not an integrity proof, but abrupt deviation from the historical range is a useful anomaly signal for backup completeness.

The engineering pattern here is sanity-check telemetry. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Trend backup size by set, investigate unexpected step changes, and confirm against manifests rather than automatically accepting smaller archives. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `b65d5d4`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
