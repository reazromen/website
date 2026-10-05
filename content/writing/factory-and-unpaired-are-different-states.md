---
title: Factory and Unpaired Are Different States
url: /posts/factory-and-unpaired-are-different-states.html
date: '2022-01-21'
read_time: 1
excerpt: A board leaving production and a consumer device waiting for ownership are
  not the same operational condition.
topic: loup-engineering
tags:
- factory-state
- pairing
- lifecycle
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Provisioning & Backend · advanced'
outputs:
- url: /posts/factory-and-unpaired-are-different-states.html
  template: cms/templates/posts/posts--factory-and-unpaired-are-different-states.tpl
  source: cms/templates/posts/posts--factory-and-unpaired-are-different-states.json
---

Factory and Unpaired Are Different States became a separate note because the failure crossed more than one subsystem. LOUP lifecycle modelling distinguishes a factory state from an unpaired field state.

Factory mode can allow programming, hardware test and manufacturing metadata without assuming the product is ready for a user. Unpaired mode belongs to the consumer onboarding path and should expose only the minimum setup behaviour needed to reach pairing.

The fix came from assigning one owner to the behaviour and refusing to hide a hardware or network fault with an unrelated firmware workaround. Evidence marker: `factory-vs-unpaired`.

State names should reflect who owns the next action. Manufacturing and user onboarding are separate trust domains. The value is not only the fix itself; it is having a repeatable way to prove the same class of failure has not returned.

## Project evidence

LOUP engineering marker: `factory-vs-unpaired`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
