---
title: Migration Tests Catch a Different Class of Failure Than Unit Tests
url: /posts/migration-tests-catch-different-failures-than-unit-tests.html
date: '2026-09-14'
read_time: 1
excerpt: An application can pass isolated logic tests while its database schema still
  fails to create, upgrade or enforce the intended constraint.
topic: production-engineering
tags:
- database-migration
- postgresql
- ci
- testing
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Data Integrity and Publishing · advanced'
outputs:
- url: /posts/migration-tests-catch-different-failures-than-unit-tests.html
  template: cms/templates/posts/posts--migration-tests-catch-different-failures-than-unit-tests.tpl
  source: cms/templates/posts/posts--migration-tests-catch-different-failures-than-unit-tests.json
---

Recent hserver applications depend heavily on PostgreSQL migrations, constraints and state transitions. A model-level fix is not sufficient if the actual migration path from existing production state is untested. Unit tests typically exercise logic against a prepared schema, while deployment failures often occur while creating or changing that schema. Validation workflows include transactional migrations and smoke tests against real PostgreSQL services where the application depends on migration behavior.

Maintain representative upgrade fixtures, run migrations in CI, and test rollback or forward-fix strategy for changes that cannot be reversed safely. Database migration testing is a form of compatibility testing. The deployment path should be exercised from the previous accepted schema to the proposed schema, not only from an empty database. The concrete hserver evidence is commit 9e6f8a5, so this note is tied to an actual production change rather than a hypothetical failure.
