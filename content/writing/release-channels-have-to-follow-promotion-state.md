---
title: Release Channels Have to Follow Promotion State
url: /posts/release-channels-have-to-follow-promotion-state.html
date: '2026-09-14'
read_time: 1
excerpt: Calling a release STABLE while its channel remains canary creates two sources
  of truth.
topic: loup-engineering
tags:
- release-channel
- ota
- state-machine
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: OTA & Release Engineering · advanced'
outputs:
- url: /posts/release-channels-have-to-follow-promotion-state.html
  template: cms/templates/posts/posts--release-channels-have-to-follow-promotion-state.tpl
  source: cms/templates/posts/posts--release-channels-have-to-follow-promotion-state.json
---

The lab result behind Release Channels Have to Follow Promotion State changed the implementation more than the first hypothesis did. LOUP OTA logic was fixed so CANARY and STABLE state transitions also update the release channel consistently.

Without that invariant, devices selecting by channel could receive a different interpretation than operators looking at release state. Synchronizing the fields turns the database into one coherent release model rather than two labels that can drift.

Reversibility stayed part of the experiment: preserve the previous artifact, make the change, then prove the new path before promoting it. Evidence marker: `stable-channel-sync`.

If two fields describe the same lifecycle decision, encode the invariant where the transition happens. Preserving that distinction is what lets the project increase complexity without losing the ability to explain a regression.

## Project evidence

LOUP engineering marker: `stable-channel-sync`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
