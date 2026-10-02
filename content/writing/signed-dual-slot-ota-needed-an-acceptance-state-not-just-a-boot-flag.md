---
title: Signed Dual-Slot OTA Needed an Acceptance State, Not Just a Boot Flag
url: /posts/signed-dual-slot-ota-needed-an-acceptance-state-not-just-a-boot-flag.html
date: '2026-09-14'
read_time: 1
excerpt: A new image should become permanent only after the device proves it can boot,
  verify, connect and report healthy.
topic: embedded-firmware
tags:
- ota
- ecdsa
- rollback
- esp32
draft: false
featured: false
language: en
eyebrow: 2026 Production Voice Systems · advanced
outputs:
- url: /posts/signed-dual-slot-ota-needed-an-acceptance-state-not-just-a-boot-flag.html
  template: cms/templates/posts/posts--signed-dual-slot-ota-needed-an-acceptance-state-not-just-a-boot-flag.tpl
  source: cms/templates/posts/posts--signed-dual-slot-ota-needed-an-acceptance-state-not-just-a-boot-flag.json
---

Dual-slot OTA solves the storage side of rollback and still leaves a policy problem: when is the new image trusted enough to keep?

I separated installation from acceptance. The device downloads the inactive slot, verifies the signed artifact, selects it for trial boot, then starts under a pending state. The new firmware has to reach defined health conditions before marking itself accepted.

Those conditions should be product-specific. Booting to `app_main` is not enough if networking is broken. For a connected voice device, I care that core services initialize, persistent state loads, networking can come up and the firmware can report its version and health.

If the trial fails repeatedly, the bootloader returns to the previous accepted slot. That turns rollback into a deterministic state transition rather than an emergency procedure.
