---
title: Backup Jobs Need a Maximum Runtime
url: /posts/backup-jobs-need-maximum-runtime.html
date: '2021-07-19'
read_time: 1
excerpt: A backup that hangs forever can block future runs and create false confidence
  without ever producing a usable recovery point.
topic: disaster-recovery
tags:
- systemd
- backup
- timeout
- operations
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Reproducibility · intermediate'
outputs:
- url: /posts/backup-jobs-need-maximum-runtime.html
  template: cms/templates/posts/posts--backup-jobs-need-maximum-runtime.tpl
  source: cms/templates/posts/posts--backup-jobs-need-maximum-runtime.json
---

The units now set a 30-minute `TimeoutStartSec` and use `KillMode=mixed` so a stuck job and its child processes are terminated as one bounded operation.

OTA and Operations backup services were one-shot jobs without an explicit production runtime bound. If a dump, archive operation or filesystem read stalled, systemd could leave the job running indefinitely. The backup policy defined when to start the work but not how long the work was allowed to remain incomplete. An unbounded maintenance task is an availability and observability problem because it can overlap schedules and never emit a clean success or failure.

systemd documents startup timeouts as a failure boundary, and production batch engineering treats completion time as part of the job contract. SRE systems need bounded failure, not infinite waiting.

Every scheduled maintenance job should have a realistic deadline, an explicit failure signal and a receipt only after durable completion. Alert on missed or overdue runs rather than merely checking that the timer fired. The concrete hserver evidence is commit 11ff139, so this note is tied to an actual production change rather than a hypothetical failure.
