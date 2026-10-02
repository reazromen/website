---
title: Unused AXP2101 Rails Should Be Explicitly Disabled
url: /posts/unused-axp2101-rails-should-be-explicitly-disabled.html
date: '2026-09-14'
read_time: 1
excerpt: Power rails that are not part of the design should not be left in an accidental
  state.
topic: loup-engineering
tags:
- axp2101
- pmic
- power
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Hardware Bring-Up · advanced'
outputs:
- url: /posts/unused-axp2101-rails-should-be-explicitly-disabled.html
  template: cms/templates/posts/posts--unused-axp2101-rails-should-be-explicitly-disabled.tpl
  source: cms/templates/posts/posts--unused-axp2101-rails-should-be-explicitly-disabled.json
---

Unused AXP2101 Rails Should Be Explicitly Disabled became a separate note because the failure crossed more than one subsystem. The LOUP PMIC plan calls for unused BLDO, ALDO and DLDO outputs to be disabled rather than ignored.

Unused regulators can consume power, create unexpected voltages on disconnected nets or complicate sleep-current measurements. A deterministic PMIC initialization sequence makes the intended power tree visible and gives factory tests a known rail state after boot.

The fix came from assigning one owner to the behaviour and refusing to hide a hardware or network fault with an unrelated firmware workaround. Evidence marker: `disable-unused-ldos`.

Power configuration is firmware-visible hardware state. Leaving an unused rail to reset defaults is still a design decision, just an undocumented one. The value is not only the fix itself; it is having a repeatable way to prove the same class of failure has not returned.

## Project evidence

LOUP engineering marker: `disable-unused-ldos`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
