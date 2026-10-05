---
title: The Device State Machine Is Part of the Product Contract
url: /posts/the-device-state-machine-is-part-of-the-product-contract.html
date: '2020-05-13'
read_time: 1
excerpt: Factory, pairing, active, blocked and retired are operational states with
  different permissions.
topic: loup-engineering
tags:
- state-machine
- pairing
- device-lifecycle
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Product Architecture · advanced'
outputs:
- url: /posts/the-device-state-machine-is-part-of-the-product-contract.html
  template: cms/templates/posts/posts--the-device-state-machine-is-part-of-the-product-contract.tpl
  source: cms/templates/posts/posts--the-device-state-machine-is-part-of-the-product-contract.json
---

The bench evidence for The Device State Machine Is Part of the Product Contract forced a narrower explanation than the original assumption. LOUP cannot treat pairing as a boolean once devices can be transferred, blocked, forced to update or retired.

The reviewed lifecycle includes factory, unpaired, pairing, paired, active, ota\_required, blocked, retired and transfer\_pending. Those states let backend policy decide whether the unit may register, call, fetch configuration or accept an ownership transition. They also give the UI a small set of explicit modes instead of inferring lifecycle from unrelated flags.

Verification included both the happy path and the failure path because a feature that works once is not yet a production contract. Evidence marker: `device-lifecycle-states`.

Explicit state machines are easier to test, recover and audit than combinations of loosely related booleans. For a voice product, that kind of boundary discipline matters because audio, signalling and hardware symptoms often look deceptively similar.

## Project evidence

LOUP engineering marker: `device-lifecycle-states`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
