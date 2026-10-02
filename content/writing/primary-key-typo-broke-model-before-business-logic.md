---
title: A Typo in primary_key=True Broke the Model Before Any Business Logic Ran
url: /posts/primary-key-typo-broke-model-before-business-logic.html
date: '2026-09-14'
read_time: 1
excerpt: Schema declarations are executable code; a one-word typo can prevent the
  application model from initializing correctly.
topic: production-engineering
tags:
- sqlalchemy
- schema
- ci
- python
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Data Integrity and Publishing · intermediate'
outputs:
- url: /posts/primary-key-typo-broke-model-before-business-logic.html
  template: cms/templates/posts/posts--primary-key-typo-broke-model-before-business-logic.tpl
  source: cms/templates/posts/posts--primary-key-typo-broke-model-before-business-logic.json
---

The content-monetization Audit model declared `primary_key_key=True` instead of `primary_key=True`. The failure was not in publishing logic, HTTP integration or database connectivity; the model definition itself was malformed.

A declarative ORM definition can look like configuration while still being executable API usage. Static visual review missed a keyword typo that the framework could catch immediately. The declaration was corrected and the managed-app CI now compiles and runs tests for the application before deployment.

This is exactly what fast feedback loops are for. Syntax checks, model initialization and migration tests should fail in CI long before a production container is rebuilt. Keep schema tests cheap enough to run on every change, and treat ORM declarations with the same code-review discipline as ordinary functions. The concrete hserver evidence is commit 2115b8b, so this note is tied to an actual production change rather than a hypothetical failure.
