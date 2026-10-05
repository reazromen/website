---
title: OTA Compatibility Is More Than a Version String
url: /posts/ota-compatibility-more-than-version-string.html
date: '2021-06-12'
read_time: 1
excerpt: A firmware artifact can be newer and still be unsafe for the target partition
  table, bootloader or hardware revision.
topic: ota-fleet
tags:
- firmware
- bootloader
- partition-table
- security
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/ota-compatibility-more-than-version-string.html
  template: cms/templates/posts/posts--ota-compatibility-more-than-version-string.tpl
  source: cms/templates/posts/posts--ota-compatibility-more-than-version-string.json
---

The production OTA design needed to prevent a validly signed image from reaching a device that could not safely boot or interpret it. Signature validity alone says who authorized the file; it does not say whether the file fits the target. Compatibility spans multiple contracts: model, MCU, hardware revision, partition layout, bootloader expectations, schema version and security generation. Release registration and assignment include explicit compatibility gates before a device is authorized to download or install the artifact.

Keep compatibility checks server-side and device-side where possible. A release system should fail closed when metadata is missing or ambiguous rather than treating unknown hardware as compatible. This is defense in depth around deployment compatibility. Authentication proves provenance; validation proves applicability; runtime acceptance proves behavior. The concrete hserver evidence is commit 0f7b5b9, so this note is tied to an actual production change rather than a hypothetical failure.
