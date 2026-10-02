---
title: I2S Audio Made Timing Bugs Audible
url: /posts/i2s-audio-made-timing-bugs-audible.html
date: '2026-09-14'
read_time: 1
excerpt: Digital audio bugs are often scheduling and buffer bugs that happen to come
  out of a speaker.
topic: embedded-firmware
tags:
- i2s
- audio
- esp32
- buffering
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · advanced
outputs:
- url: /posts/i2s-audio-made-timing-bugs-audible.html
  template: cms/templates/posts/posts--i2s-audio-made-timing-bugs-audible.tpl
  source: cms/templates/posts/posts--i2s-audio-made-timing-bugs-audible.json
---

I2S looked like a simple peripheral until the first crackle appeared. The codec configuration could be correct, samples could be mostly right, and the audio could still sound bad because timing was wrong.

The important parameters are connected: sample rate, word width, channel count, DMA buffer size and task scheduling. If the producer cannot feed the peripheral at a steady rate, the listener hears the underrun immediately. Audio is an unusually honest debugging interface.

I began measuring buffer occupancy and callback timing instead of changing codec registers randomly. A periodic stall in another task could line up with an audible click. Increasing a buffer might hide the symptom while adding latency, so the fix had to match the real requirement.

This was also my first strong reminder that real-time behavior is about deadlines, not average speed. A CPU can be mostly idle and still miss the one moment when the audio pipeline needs data.
