---
title: Firmware Compatibility Should Be Derived from the Enrolled Device
url: /posts/firmware-compatibility-derived-from-enrolled-device.html
date: '2026-09-14'
read_time: 1
excerpt: Release metadata is safer when it comes from authoritative device capabilities
  instead of copied operator input.
topic: ota-fleet
tags:
- firmware
- compatibility
- device-enrollment
- ota
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/firmware-compatibility-derived-from-enrolled-device.html
  template: cms/templates/posts/posts--firmware-compatibility-derived-from-enrolled-device.tpl
  source: cms/templates/posts/posts--firmware-compatibility-derived-from-enrolled-device.json
---

Signed release metadata included compatibility fields such as model, MCU, hardware revision and partition expectations. Manually reproducing those values during release creation creates an opportunity for a typo to authorize the wrong artifact.

The same facts existed in two places: enrolled device identity and operator-supplied release metadata. Duplicated authority invites drift. The release workflow derives compatibility requirements from the enrolled device where possible, reducing the number of safety-critical values that operators must retype.

This is single-source-of-truth design. Safety metadata should be derived from the most authoritative existing object rather than duplicated across forms and APIs. Make compatibility metadata immutable once a device identity is established, and require explicit migration procedures for legitimate hardware-profile changes. The concrete hserver evidence is commit 4b472da, so this note is tied to an actual production change rather than a hypothetical failure.
