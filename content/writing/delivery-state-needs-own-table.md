---
title: Delivery State Needs Its Own Table
url: /posts/delivery-state-needs-own-table.html
date: '2026-09-14'
read_time: 1
excerpt: Content intent and remote-delivery progress are different state machines
  and should not be collapsed into one post status.
topic: production-engineering
tags:
- state-machine
- publisher
- database
- delivery
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Data Integrity and Publishing · advanced'
outputs:
- url: /posts/delivery-state-needs-own-table.html
  template: cms/templates/posts/posts--delivery-state-needs-own-table.tpl
  source: cms/templates/posts/posts--delivery-state-needs-own-table.json
---

A content item can exist locally while remote delivery is queued, scheduled, publishing, partially complete, failed or already published. One generic post status could not explain all of those operational states.

Model independent state machines independently, then connect them with explicit keys. This reduces overloaded enums and makes failure recovery local to the subsystem that owns the transition. The domain contained two lifecycles: editorial content and external delivery. Combining them makes retries, auditing and reconciliation ambiguous. A dedicated delivery-state table records publisher-specific progress and remote identifiers separately from the local content record.

Document allowed delivery transitions and make terminal states explicit so a background reconciler can resume work without guessing which operations remain safe. The concrete hserver evidence is commit f30248c, so this note is tied to an actual production change rather than a hypothetical failure.
