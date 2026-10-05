---
title: Backup Monitoring Needs UNKNOWN as a Real State
url: /posts/backup-monitoring-needs-unknown-state.html
date: '2025-07-20'
read_time: 1
excerpt: Least-privilege monitoring sometimes cannot read protected backup evidence,
  and treating that access failure as healthy would be dangerous.
topic: observability-monitoring
tags:
- backup-posture
- unknown
- least-privilege
- monitoring
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Backup & DR · advanced'
outputs:
- url: /posts/backup-monitoring-needs-unknown-state.html
  template: cms/templates/posts/posts--backup-monitoring-needs-unknown-state.tpl
  source: cms/templates/posts/posts--backup-monitoring-needs-unknown-state.json
---

Least-privilege monitoring sometimes cannot read protected backup evidence, and treating that access failure as healthy would be dangerous. On the finished hserver stack, `backup posture states PASS, FAIL and UNKNOWN` is the signal that makes the difference visible. UNKNOWN preserves epistemic honesty: the monitor lacks enough evidence to claim health, but it also has not proven corruption or failure.

The engineering pattern here is three-state operational monitoring. Good monitoring should shorten diagnosis, so I prefer a small number of signals with clear semantics over a larger collection whose meaning is unclear during a failure.

Operationally I keep this constraint: Expose unavailable evidence explicitly, alert it at the appropriate severity, and fix the observation path without fabricating success. It gives the dashboard, alert, and runbook the same interpretation instead of letting each layer invent its own definition of healthy.

The implementation can be traced to hserver commit `f199743`. That provenance is part of the article because these notes document an actual production observability system, not a hypothetical monitoring design.
