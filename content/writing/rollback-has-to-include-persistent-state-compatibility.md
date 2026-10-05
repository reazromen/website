---
title: Rollback Has to Include Persistent-State Compatibility
url: /posts/rollback-has-to-include-persistent-state-compatibility.html
date: '2020-11-11'
read_time: 1
excerpt: Returning to an older binary is unsafe if the newer release already changed
  data the old code cannot read.
topic: loup-engineering
tags:
- ota
- nvs
- schema-migration
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: OTA & Release Engineering · advanced'
outputs:
- url: /posts/rollback-has-to-include-persistent-state-compatibility.html
  template: cms/templates/posts/posts--rollback-has-to-include-persistent-state-compatibility.tpl
  source: cms/templates/posts/posts--rollback-has-to-include-persistent-state-compatibility.json
---

I stopped treating this part of LOUP as a black box while working on Rollback Has to Include Persistent-State Compatibility. LOUP release engineering treats NVS and persistent schema changes as part of OTA compatibility, not as an afterthought.

A new image may write fields, credentials or migration markers that survive partition rollback. Before a release is called rollback-safe, the old firmware has to tolerate the post-migration state or the migration itself has to be reversible.

Logs and measurements were used to decide whether the fault lived before or after the boundary, then the smallest falsifiable change was tested. Evidence marker: `ota-schema-rollback`.

Binary rollback without data rollback is only half a recovery design. The resulting test is small enough to rerun after later changes, which is what turns one successful experiment into engineering evidence.

## Project evidence

LOUP engineering marker: `ota-schema-rollback`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
