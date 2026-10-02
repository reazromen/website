---
title: Audit Tables Must Be Boring and Correct
url: /posts/audit-tables-must-be-boring-and-correct.html
date: '2026-09-14'
read_time: 1
excerpt: An audit trail is only useful if its schema is simpler and more dependable
  than the systems it records.
topic: production-engineering
tags:
- audit
- database
- integrity
- operations
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Data Integrity and Publishing · intermediate'
outputs:
- url: /posts/audit-tables-must-be-boring-and-correct.html
  template: cms/templates/posts/posts--audit-tables-must-be-boring-and-correct.tpl
  source: cms/templates/posts/posts--audit-tables-must-be-boring-and-correct.json
---

A tiny ORM typo in the audit model highlighted an uncomfortable fact: the system responsible for recording operational evidence can fail before the feature being audited even starts.

Audit schemas should minimize cleverness. Stable identifiers, immutable event rows, timestamps and object references are more valuable than flexible but fragile abstractions. Audit infrastructure is often treated as secondary logging, but production controls increasingly depend on it for attribution, approval and postmortem reconstruction.

The primary-key declaration was fixed, migrations and tests were added, and append-only audit behavior is part of the control-plane design.

Test audit insertion in every smoke suite and make inability to record a required security event a visible service degradation rather than a silent exception. The concrete hserver evidence is commit 2115b8b, so this note is tied to an actual production change rather than a hypothetical failure.
