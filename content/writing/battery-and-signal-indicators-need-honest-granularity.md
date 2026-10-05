---
title: Battery and Signal Indicators Need Honest Granularity
url: /posts/battery-and-signal-indicators-need-honest-granularity.html
date: '2024-10-02'
read_time: 1
excerpt: Tiny icons can imply precision the underlying measurements do not actually
  support.
topic: loup-engineering
tags:
- battery
- wi-fi-signal
- ui
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: E-Paper UI & Controls · advanced'
outputs:
- url: /posts/battery-and-signal-indicators-need-honest-granularity.html
  template: cms/templates/posts/posts--battery-and-signal-indicators-need-honest-granularity.tpl
  source: cms/templates/posts/posts--battery-and-signal-indicators-need-honest-granularity.json
---

The lab result behind Battery and Signal Indicators Need Honest Granularity changed the implementation more than the first hypothesis did. LOUP plans to show battery and network status on a small monochrome display, but those values arrive from noisy physical measurements.

Battery percentage should be filtered and mapped to a sensible number of display states rather than jumping with instantaneous voltage. Wi-Fi bars should represent a stable RSSI policy and avoid flapping at thresholds.

Reversibility stayed part of the experiment: preserve the previous artifact, make the change, then prove the new path before promoting it. Evidence marker: `battery-signal`.

A compact UI should simplify noisy telemetry without pretending the simplification is exact. Preserving that distinction is what lets the project increase complexity without losing the ability to explain a regression.

## Project evidence

LOUP engineering marker: `battery-signal`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
