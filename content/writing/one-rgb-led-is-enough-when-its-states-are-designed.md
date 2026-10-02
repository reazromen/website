---
title: One RGB LED Is Enough When Its States Are Designed
url: /posts/one-rgb-led-is-enough-when-its-states-are-designed.html
date: '2026-09-14'
read_time: 1
excerpt: A single status light can become confusing if color, blink and priority are
  not treated as a protocol.
topic: loup-engineering
tags:
- rgb-led
- status
- ux
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: E-Paper UI & Controls · advanced'
outputs:
- url: /posts/one-rgb-led-is-enough-when-its-states-are-designed.html
  template: cms/templates/posts/posts--one-rgb-led-is-enough-when-its-states-are-designed.tpl
  source: cms/templates/posts/posts--one-rgb-led-is-enough-when-its-states-are-designed.json
---

The bench evidence for One RGB LED Is Enough When Its States Are Designed forced a narrower explanation than the original assumption. LOUP deliberately uses one top-front RGB status LED instead of a cluster of unrelated indicators.

The firmware needs a priority table so pairing, ringing, mute, error, charging or OTA states do not fight for the LED. Color and blink patterns should be few, documented and aligned with what the e-paper says rather than creating a second independent UI.

Verification included both the happy path and the failure path because a feature that works once is not yet a production contract. Evidence marker: `single-rgb-led`.

Indicator simplicity comes from state design, not from having fewer LEDs alone. For a voice product, that kind of boundary discipline matters because audio, signalling and hardware symptoms often look deceptively similar.

## Project evidence

LOUP engineering marker: `single-rgb-led`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
