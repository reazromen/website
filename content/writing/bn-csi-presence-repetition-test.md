---
title: Presence Detection Needs Repetition, Not Just a Good Demo
date: '2026-05-09'
draft: false
language: en
url: /posts/bn-csi-presence-repetition-test.html
topic: radio-iot
tags:
- sensing
- testing
featured: false
read_time: 2
excerpt: >-
  Someone enters a room and the graph changes. It is a compelling demo, but it is not yet
  evidence of reliable presence detection. Signals can change for reasons other than a
  person entering the space.
editorial_batch: 20261003-100-niches
---

Someone enters a room and the graph changes. It is a compelling demo, but it is not yet evidence of reliable presence detection. Signals can change for reasons other than a person entering the space. One coincidence is not a complete causal proof.

A better test includes empty-room behavior. What happens when a door moves, a fan turns on, a device is relocated, or the network changes? If data is collected only while a person is present, the conditions that create false alarms remain invisible.

Questions such as how often detection is correct, how often it is wrong, and how long detection takes require comparison against a known ground truth. The environment used for training should also be separated from an environment used for independent evaluation.

For me, the strength of a presence system is not the beauty of its graph but the repeatability of its tests. The interface should also expose cases where the system cannot be confident. Hiding uncertainty does not turn uncertain sensing into certain detection.

Source: [official reference](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/wifi.html).
