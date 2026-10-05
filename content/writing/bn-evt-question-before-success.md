---
title: Define the Questions Before Calling EVT a Success
date: '2024-07-10'
draft: false
language: en
url: /posts/bn-evt-question-before-success.html
topic: pcb-bringup-hardware
tags:
- hardware
- testing
featured: false
read_time: 2
excerpt: >-
  Seeing a prototype power on is a major relief, but engineering validation requires knowing
  which questions the board has actually answered. One LED cannot validate power, audio,
  radio behavior, and long-duration operation at the same time.
editorial_batch: 20261003-100-niches
---

Seeing a prototype power on is a major relief, but engineering validation requires knowing which questions the board has actually answered. One LED cannot validate power, audio, radio behavior, and long-duration operation at the same time.

Suppose a board works on the bench but behaves differently with another power supply or inside the enclosure. The first test was still a valid success, but its scope was smaller than the product. Recording the test conditions keeps that limit visible instead of silently expanding the claim.

A small validation matrix is surprisingly powerful: feature, board revision, firmware build, equipment, conditions, and result. It makes comparisons possible and gives uncertain outcomes somewhere to live.

Moving from prototype to production is largely the process of widening the evidence. A successful demo is the beginning. Confidence grows when the required behavior repeats under the same conditions and then continues to hold under more demanding ones.

Source: [official reference](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/index.html).
