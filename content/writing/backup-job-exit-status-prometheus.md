---
title: Backup Job Exit Status Belongs in Prometheus
url: /posts/backup-job-exit-status-prometheus.html
date: '2026-09-14'
read_time: 1
excerpt: A systemd timer can fire on schedule while the backup service itself fails,
  times out or exits before producing a valid set.
topic: observability-monitoring
tags:
- systemd
- backup-jobs
- prometheus
- outcomes
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Backup & DR · advanced'
outputs:
- url: /posts/backup-job-exit-status-prometheus.html
  template: cms/templates/posts/posts--backup-job-exit-status-prometheus.tpl
  source: cms/templates/posts/posts--backup-job-exit-status-prometheus.json
---

A systemd timer can fire on schedule while the backup service itself fails, times out or exits before producing a valid set. What made the issue measurable was `hserver_systemd_service_result_success for managed backup units`. Scheduling evidence and completion evidence are separate; monitoring only the timer would report success for a failed backup execution.

I classify this as job-outcome monitoring. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Export the last service result, alert on failure, and correlate it with backup age so a failed run cannot remain hidden until the next day. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `11ff139` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
