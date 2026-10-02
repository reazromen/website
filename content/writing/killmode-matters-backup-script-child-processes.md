---
title: KillMode Matters When a Backup Script Spawns Child Processes
url: /posts/killmode-matters-backup-script-child-processes.html
date: '2026-09-14'
read_time: 1
excerpt: Stopping only the shell does not necessarily stop pg_dump, tar or helper
  processes that the shell launched.
topic: disaster-recovery
tags:
- systemd
- process-tree
- backup
- linux
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Reproducibility · advanced'
outputs:
- url: /posts/killmode-matters-backup-script-child-processes.html
  template: cms/templates/posts/posts--killmode-matters-backup-script-child-processes.tpl
  source: cms/templates/posts/posts--killmode-matters-backup-script-child-processes.json
---

Bounding a backup service with a timeout raised a second question: what happens to subprocesses when the main shell exceeds the deadline? A timed-out parent is not enough if archive or database child processes remain alive.

This is process-lifecycle ownership. A supervisor should own and bound the complete work unit so cancellation has deterministic semantics. Process supervision had to cover the unit's process tree, not only the initial `ExecStart` PID. Otherwise a failed job could continue consuming I/O and writing partial artifacts after systemd reported it stopped.

The backup units use `KillMode=mixed`, allowing systemd to terminate the main process and then clean up remaining processes in the control group according to the service stop policy.

Test timeout behavior deliberately with a controlled long-running child process. Failure-path tests are the only reliable way to know whether cleanup semantics match the design. The concrete hserver evidence is commit 11ff139, so this note is tied to an actual production change rather than a hypothetical failure.
