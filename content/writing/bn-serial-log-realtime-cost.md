---
title: Serial Logging Is Work for the Processor Too
date: '2024-12-19'
draft: false
language: en
url: /posts/bn-serial-log-realtime-cost.html
topic: embedded-audio-voice
tags:
- audio
- debugging
featured: false
read_time: 2
excerpt: >-
  Logs help us observe a system, but producing them also consumes time. Heavy logging
  inside a real-time audio path can change the behavior being measured.
editorial_batch: 20261003-100-niches
---

Logs help us observe a system, but producing them also consumes time. Heavy logging inside a real-time audio path can change the behavior being measured. The act of observing the problem can add new pressure to it.

Suppose an audio frame has a tight deadline. Now add string construction, formatting, and serial output to that same path. Each operation may look small in isolation, but the cost accumulates across continuous frames. This can create the confusing situation where the bug appears in debug mode but not in the release build.

Decide which logs are necessary in the time-critical path and which can be processed later. Counters, limited sampling, or compact events passed to another task may help, although every queue and handoff has a cost of its own.

Observation is never completely invisible. Good debugging acknowledges that influence and compares against a known normal baseline. Treating logs as perfectly neutral evidence can make instrumentation-induced behavior look like a product defect.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/log.html).
