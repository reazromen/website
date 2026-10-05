---
title: Dual OTA Slots Need an Acceptance State
url: /posts/dual-ota-slots-need-an-acceptance-state.html
date: '2023-02-17'
read_time: 1
excerpt: Booting the new partition once is not enough to declare it safe.
topic: loup-engineering
tags:
- ota
- rollback
- acceptance
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: OTA & Release Engineering · advanced'
outputs:
- url: /posts/dual-ota-slots-need-an-acceptance-state.html
  template: cms/templates/posts/posts--dual-ota-slots-need-an-acceptance-state.tpl
  source: cms/templates/posts/posts--dual-ota-slots-need-an-acceptance-state.json
---

Dual OTA Slots Need an Acceptance State became a separate note because the failure crossed more than one subsystem. LOUP production OTA design uses trial boot, health validation and an explicit accepted state before a new image becomes permanent.

The candidate has to initialize core services, load persistent state, reach networking and report the expected release before the device marks it valid. If those conditions fail repeatedly, the bootloader can return to the previous accepted slot.

The fix came from assigning one owner to the behaviour and refusing to hide a hardware or network fault with an unrelated firmware workaround. Evidence marker: `dual-slot-acceptance`.

Rollback works when acceptance is a state machine, not when operators have to notice a bad release manually. The value is not only the fix itself; it is having a repeatable way to prove the same class of failure has not returned.

## Project evidence

LOUP engineering marker: `dual-slot-acceptance`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
