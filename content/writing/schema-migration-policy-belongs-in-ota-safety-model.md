---
title: Schema Migration Policy Belongs in the OTA Safety Model
url: /posts/schema-migration-policy-belongs-in-ota-safety-model.html
date: '2026-01-14'
read_time: 1
excerpt: Rollback is only safe when persistent data remains readable by the previous
  firmware or a migration policy accounts for the change.
topic: ota-fleet
tags:
- ota
- migration
- nvs
- rollback
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/schema-migration-policy-belongs-in-ota-safety-model.html
  template: cms/templates/posts/posts--schema-migration-policy-belongs-in-ota-safety-model.tpl
  source: cms/templates/posts/posts--schema-migration-policy-belongs-in-ota-safety-model.json
---

This is forward/backward compatibility engineering. Database migrations, API schemas and embedded NVS all need an explicit compatibility window when rollback is part of the availability strategy. A/B firmware rollback can restore the previous code image while leaving persistent configuration or NVS data written by the new image. If the schema changed incompatibly, the old slot may boot into data it no longer understands. Firmware rollback and data rollback are separate mechanisms. Treating them as one capability creates a false promise of recovery.

The OTA policy tracks schema compatibility and migration rules alongside partition and bootloader constraints, so releases that require irreversible data changes cannot pretend to support simple binary rollback. Version persistent schemas, make migrations idempotent where possible, preserve downgrade readability for the rollback window, and test an actual downgrade before declaring rollback supported. The concrete hserver evidence is commit 0f7b5b9, so this note is tied to an actual production change rather than a hypothetical failure.
