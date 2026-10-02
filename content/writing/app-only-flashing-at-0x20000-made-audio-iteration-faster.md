---
title: App-Only Flashing at 0x20000 Made Audio Iteration Faster
url: /posts/app-only-flashing-at-0x20000-made-audio-iteration-faster.html
date: '2026-09-14'
read_time: 1
excerpt: Updating only the application partition avoids rewriting unrelated state
  during tight firmware experiments.
topic: loup-engineering
tags:
- esp32-s3
- flash
- app-partition
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: OTA & Release Engineering · advanced'
outputs:
- url: /posts/app-only-flashing-at-0x20000-made-audio-iteration-faster.html
  template: cms/templates/posts/posts--app-only-flashing-at-0x20000-made-audio-iteration-faster.tpl
  source: cms/templates/posts/posts--app-only-flashing-at-0x20000-made-audio-iteration-faster.json
---

The useful question in App-Only Flashing at 0x20000 Made Audio Iteration Faster was where the behaviour actually originated. LOUP used app-only images flashed at offset `0x20000` for rapid audio and SIP iteration on EVT hardware.

That path reduced turnaround and preserved bootloader, partition table and other device state while the application changed frequently. It also required discipline: the artifact had to match the installed partition layout, and production OTA cannot assume a lab flash command is its release mechanism.

I treated the known-good configuration as a control sample, changed only the layer under investigation, and recorded the regression or improvement before the next experiment. Evidence marker: `app-only-0x20000`.

Fast developer flashing and production update policy can share artifacts without sharing the same delivery process. Keeping the rule explicit means the same decision can be checked again on the next board revision or firmware branch.

## Project evidence

LOUP engineering marker: `app-only-0x20000`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
