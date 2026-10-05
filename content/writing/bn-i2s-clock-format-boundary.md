---
title: If I2S Is Silent, Check the Format Contract First
date: '2022-12-22'
draft: false
language: en
url: /posts/bn-i2s-clock-format-boundary.html
topic: embedded-audio-voice
tags:
- audio
- firmware
featured: false
read_time: 2
excerpt: >-
  Bytes moving over I2S do not prove that both devices interpret those bytes the same way.
  Sample width, channel layout, clock relationships, and data alignment all have to match.
  A silent speaker is not automatically an amplifier problem.
editorial_batch: 20261003-100-niches
---

Bytes moving over I2S do not prove that both devices interpret those bytes the same way. Sample width, channel layout, clock relationships, and data alignment all have to match. A silent speaker is not automatically an amplifier problem.

Suppose the samples in memory are correct but the peripheral expects a different bit layout. The same bytes may then be interpreted as completely different values. The symptom may be silence, extremely low level, or distortion. Symptoms alone do not identify the cause.

A short, known test signal is useful here. Inspect the input, the samples in memory, and the output separately to find the boundary where meaning changes. Board pin assignment and the actual physical wiring belong to the same verification path.

I think of the audio path as a sequence of translations. Numbers in memory, serialized data, and physical sound are different representations of the same intended signal. Debugging becomes smaller when we find which transition broke its interpretation.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/i2s.html).
