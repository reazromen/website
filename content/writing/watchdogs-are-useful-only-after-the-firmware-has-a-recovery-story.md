---
title: Watchdogs Are Useful Only After the Firmware Has a Recovery Story
url: /posts/watchdogs-are-useful-only-after-the-firmware-has-a-recovery-story.html
date: '2023-05-14'
read_time: 1
excerpt: Resetting a stuck device is not the same as fixing it; watchdog design needs
  crash evidence and bounded recovery behavior.
topic: embedded-firmware
tags:
- watchdog
- embedded
- reliability
- esp32
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · intermediate
outputs:
- url: /posts/watchdogs-are-useful-only-after-the-firmware-has-a-recovery-story.html
  template: cms/templates/posts/posts--watchdogs-are-useful-only-after-the-firmware-has-a-recovery-story.tpl
  source: cms/templates/posts/posts--watchdogs-are-useful-only-after-the-firmware-has-a-recovery-story.json
---

A watchdog timer feels like instant reliability because it can reset a firmware image that stops making progress. It can also turn a reproducible bug into an endless reboot loop that destroys the evidence.

I started using the watchdog only after deciding what the device should preserve across a reset. Reset reason, boot count and a small crash marker are more useful than a silent restart. If the same firmware crashes repeatedly, the recovery policy should eventually do something different instead of repeating the same boot forever.

Task watchdogs also forced me to define what “healthy” means. Feeding the watchdog from a timer proves almost nothing. The feed should represent forward progress in the work that matters, otherwise a dead application can keep the watchdog happy.

The best outcome was not fewer resets. It was controlled resets with enough state to understand why they happened and a path to recover without user intervention.
