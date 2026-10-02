---
title: Remote Terminal States Should Stop Re-Publishing Logic
url: /posts/remote-terminal-states-stop-republishing-logic.html
date: '2026-09-14'
read_time: 1
excerpt: If the provider already reports scheduled, publishing or published, the reconciler
  should observe rather than repeat the side effect.
topic: production-engineering
tags:
- publisher
- terminal-state
- idempotency
- api
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Data Integrity and Publishing · advanced'
outputs:
- url: /posts/remote-terminal-states-stop-republishing-logic.html
  template: cms/templates/posts/posts--remote-terminal-states-stop-republishing-logic.tpl
  source: cms/templates/posts/posts--remote-terminal-states-stop-republishing-logic.json
---

A reconciler that finds an existing remote object still needs to decide whether to schedule, publish or do nothing. Reissuing a publish operation against an object already in flight can create confusing or provider-specific behavior. Discovery alone did not make the workflow idempotent; state-aware action selection was still required.

The publisher treats `scheduled`, `publishing`, `published` and `partial` as states where the existing remote object should be returned rather than re-triggered.

Mirror the provider state machine explicitly and write tests for every remote state your reconciler can observe, including unknown or newly introduced values. Idempotent workflows combine object identity with transition semantics. The same command can be safe in one state and wrong in another. The concrete hserver evidence is commit 9118e08, so this note is tied to an actual production change rather than a hypothetical failure.
