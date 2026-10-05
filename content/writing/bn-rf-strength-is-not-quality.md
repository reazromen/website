---
title: A Strong Radio Signal Does Not Guarantee Good Communication
date: '2026-10-03'
draft: false
language: en
url: /posts/bn-rf-strength-is-not-quality.html
topic: radio-iot
tags:
- radio
- measurement
featured: false
read_time: 2
excerpt: >-
  Signal strength can help estimate link conditions, but it is not the whole quality story.
  A strong desired signal can still be difficult to decode in a noisy or interfering
  environment. Strength and intelligibility answer different questions.
editorial_batch: 20261003-100-niches
---

Signal strength can help estimate link conditions, but it is not the whole quality story. A strong desired signal can still be difficult to decode in a noisy or interfering environment. The receiver has to distinguish the desired information from everything else around it. Strength and intelligibility answer different questions.

Suppose one location shows stronger signal but repeatedly loses packets. Another shows slightly weaker signal while delivering data consistently. Choosing from the first number alone hides the usefulness of the second path. Packet success rate, retries, and timing variation matter too.

Before changing an antenna, record the test environment. Device orientation, distance, walls, time, and surrounding traffic all affect comparison. If conditions change between measurements, it becomes difficult to attribute the result to the antenna alone.

A radio dashboard should not imply certainty through one large number. The number matters, but so does the outcome of the communication. The goal is not the highest signal reading; it is reliable delivery of the required data.

Source: [official reference](https://lora-alliance.org/resource_hub/what-is-lorawan/).
