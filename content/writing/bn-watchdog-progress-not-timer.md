---
title: A Watchdog Should Observe Progress, Not Just a Timer
date: '2023-08-23'
draft: false
language: en
url: /posts/bn-watchdog-progress-not-timer.html
topic: embedded-firmware
tags:
- firmware
- reliability
featured: false
read_time: 2
excerpt: >-
  A regularly fed watchdog does not prove that important work is progressing. A dedicated
  task can keep feeding the timer while an audio or network task is stuck, making the real
  failure invisible to the watchdog.
editorial_batch: 20261003-100-niches
---

A regularly fed watchdog does not prove that important work is progressing. A dedicated task can keep feeding the timer while an audio or network task is stuck, making the real failure invisible to the watchdog. Repeated execution and meaningful progress are not the same thing.

Imagine a sensor task that should produce new data every cycle. The task wakes on schedule but keeps reusing the previous sample. A heartbeat based only on loop execution will miss that stagnation. The design needs some notion of a successful stage or meaningful progress, together with a definition of when waiting is normal and when it means the system is stuck.

A timeout that is too short can also reset the device during legitimate long work. One that is too long can leave a failure in place for too much time. The watchdog interval is therefore not just a number; it belongs to the expected execution time and recovery policy.

A restart is neither the root cause nor always the solution. If the restart reason is not preserved, the same fault may return without explanation. I prefer to think of a watchdog as a final defensive layer: it may bring the system back, but it cannot explain poor design by itself.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/system/wdts.html).
