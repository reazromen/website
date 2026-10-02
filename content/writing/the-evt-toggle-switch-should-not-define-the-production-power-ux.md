---
title: The EVT Toggle Switch Should Not Define the Production Power UX
url: /posts/the-evt-toggle-switch-should-not-define-the-production-power-ux.html
date: '2026-09-14'
read_time: 1
excerpt: Prototype hardware can be adapted in firmware without turning the prototype
  limitation into the final product.
topic: loup-engineering
tags:
- power-button
- evt
- controls
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: E-Paper UI & Controls · advanced'
outputs:
- url: /posts/the-evt-toggle-switch-should-not-define-the-production-power-ux.html
  template: cms/templates/posts/posts--the-evt-toggle-switch-should-not-define-the-production-power-ux.tpl
  source: cms/templates/posts/posts--the-evt-toggle-switch-should-not-define-the-production-power-ux.json
---

The practical ownership question in The EVT Toggle Switch Should Not Define the Production Power UX was simple to state and harder to prove. The EVT side toggle was mapped toward soft-power behavior for testing, while production is expected to use a proper momentary power button.

Firmware can interpret the existing switch state to exercise shutdown and startup flows, but the final interaction model needs press semantics, debounce, long-press policy and PMIC coordination appropriate to a momentary control.

The debugging order stayed conservative: verify wiring and state transitions first, then tune performance only after correctness had been established. Evidence marker: `power-toggle-to-momentary`.

Prototype adaptation is useful when it preserves software progress, but production UX should still be designed for the intended hardware. The broader result is a system that can be changed incrementally because each layer has a measurable responsibility and a known recovery path.

## Project evidence

LOUP engineering marker: `power-toggle-to-momentary`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
