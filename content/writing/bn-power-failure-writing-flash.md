---
title: What Happens if Power Fails While Writing Flash?
date: '2024-10-30'
draft: false
language: en
url: /posts/bn-power-failure-writing-flash.html
topic: embedded-firmware
tags:
- storage
- reliability
featured: false
read_time: 2
excerpt: >-
  It is easy to think of saving data as one indivisible event: write it and it is done.
  In reality, power can disappear in the middle of a write. The next boot then has to
  distinguish complete, incomplete, and usable state.
editorial_batch: 20261003-100-niches
---

It is easy to think of saving data as one indivisible event: write it and it is done. In reality, power can disappear in the middle of a write. The next boot then has to distinguish complete, incomplete, and usable state.

Suppose several related configuration values are written in separate steps. A restart between those steps can leave a mixed state. Storage-library guarantees matter, but the application also has to reason about relationships across multiple values. Safely writing one value is not the same claim as atomically accepting an entire configuration.

Testing should include more than the successful save path. In an authorized test setup, remove power at different stages and observe what the next boot does. Preserving known-good data, detecting incomplete changes, and defining a retry path are all parts of recovery design.

Reliability in small devices often comes from handling these inconvenient middle states. The normal path is easy to make look clean. A product becomes more trustworthy when it has explicit rules for recovering correct meaning after incomplete work.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/storage/nvs_flash.html).
