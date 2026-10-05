---
title: When You Widen a Channel, Who Are You Sharing the Spectrum With?
date: '2021-12-06'
draft: false
language: en
url: /posts/bn-channel-width-shared-medium.html
topic: networking
tags:
- wifi
- capacity
featured: false
read_time: 2
excerpt: >-
  Wider channels suggest higher speed, but nearby networks still occupy the same radio
  environment. Increasing your own peak capacity and getting stable performance in that
  environment are not the same design decision.
editorial_batch: 20261003-100-niches
---

Wider channels suggest higher speed, but nearby networks still occupy the same radio environment. Increasing your own peak capacity and getting stable performance in that environment are not the same design decision. You need to know who else is sharing the space.

In a crowded location, measuring only the maximum throughput of one nearby phone does not represent real use. Distant clients, many simultaneous users, and peak-time traffic all need to be part of the test.

Before changing channel width, keep a baseline of the current channel, utilization, and retry behavior. Then repeat the same test after a controlled change. One speed-test result should not be promoted into a statement about every user's experience.

Wi-Fi design is fundamentally planning for a shared medium. More capability on your own access point does not make neighboring systems less relevant. Stable behavior is often more useful than the largest headline number.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/wifi.html).
