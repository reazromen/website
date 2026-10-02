---
title: A Backup Timer Firing Is Not Proof That the Backup Finished
url: /posts/backup-timer-firing-not-proof-backup-finished.html
date: '2026-09-14'
read_time: 1
excerpt: Scheduling evidence and completion evidence belong to different layers of
  a batch job.
topic: disaster-recovery
tags:
- systemd-timer
- backup
- receipt
- batch-jobs
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Backup and DR · intermediate'
outputs:
- url: /posts/backup-timer-firing-not-proof-backup-finished.html
  template: cms/templates/posts/posts--backup-timer-firing-not-proof-backup-finished.tpl
  source: cms/templates/posts/posts--backup-timer-firing-not-proof-backup-finished.json
---

Backup services are bounded by timeouts and successful runs emit protected receipts or complete timestamped sets that posture checks can validate independently of the timer history.

The managed backup units made scheduling explicit, but a timer activation only proves that systemd attempted to start the service. It does not prove PostgreSQL dumped successfully, archives completed or checksums were written. Trigger state and job outcome were being conflated. Batch reliability requires a durable completion signal from the work itself.

Reliable batch systems separate scheduler health, execution health and output validity. Each stage can fail while the others look normal.

Alert on missing recent completion receipts, not just failed timers. A scheduler that runs perfectly can repeatedly launch a job that never produces a recovery point. The concrete hserver evidence is commit a4e34d2, so this note is tied to an actual production change rather than a hypothetical failure.
