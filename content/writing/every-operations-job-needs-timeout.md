---
title: Every Operations Job Needs a Timeout
url: /posts/every-operations-job-needs-timeout.html
date: '2024-05-07'
read_time: 1
excerpt: A safe command can still become unsafe operationally if it can occupy the
  runner forever.
topic: web-control-plane
tags:
- timeout
- runner
- operations
- reliability
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Safe Automation · intermediate'
outputs:
- url: /posts/every-operations-job-needs-timeout.html
  template: cms/templates/posts/posts--every-operations-job-needs-timeout.tpl
  source: cms/templates/posts/posts--every-operations-job-needs-timeout.json
---

Job definitions include bounded `timeout_sec` values and the runner enforces them before returning result and output hashes. The portal runner can launch diagnostics and maintenance checks that depend on local services, Docker or network state. Any of those dependencies can hang even when the command is read-only. Safety classification had initially focused on what a command changes, not on how long it can consume execution capacity. Availability is part of the risk model too.

Bounded execution is a reliability primitive. Timeouts convert indefinite uncertainty into an explicit failure state that automation and operators can reason about.

Choose timeouts from measured normal duration plus margin, distinguish timeout from command failure, and alert when a previously fast diagnostic begins approaching its bound. The concrete hserver evidence is commit 9e6f8a5, so this note is tied to an actual production change rather than a hypothetical failure.
