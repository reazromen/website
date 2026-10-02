---
title: Background Dispatch Needs Reconciliation After Restart
url: /posts/background-dispatch-needs-reconciliation-after-restart.html
date: '2026-09-14'
read_time: 1
excerpt: A scheduler can enqueue work before crashing; recovery logic must discover
  incomplete deliveries after the process returns.
topic: production-engineering
tags:
- scheduler
- reconciliation
- publisher
- recovery
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Data Integrity and Publishing · advanced'
outputs:
- url: /posts/background-dispatch-needs-reconciliation-after-restart.html
  template: cms/templates/posts/posts--background-dispatch-needs-reconciliation-after-restart.tpl
  source: cms/templates/posts/posts--background-dispatch-needs-reconciliation-after-restart.json
---

Automated publishing introduced a new failure window between selecting due content, creating remote work and recording the final result. A process restart inside that window could leave local and remote state out of sync.

Dispatch was an ongoing workflow, not an atomic database transaction across both systems. Exactly-once execution could not be assumed. The publisher now combines scheduled dispatch with idempotent reconciliation so incomplete or uncertain deliveries can be revisited safely after restart.

Distributed job systems should assume at-least-once execution and design handlers to be idempotent or reconcilable. Crash recovery is part of the normal control flow. Persist checkpoints around external side effects, expose stuck-delivery age, and test process termination at each step of the workflow. The concrete hserver evidence is commit 999d414, so this note is tied to an actual production change rather than a hypothetical failure.
