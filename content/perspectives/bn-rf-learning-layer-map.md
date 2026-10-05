---
title: Keep a Layer Map While Learning RF
date: '2025-05-28'
draft: false
language: en
url: /posts/bn-rf-learning-layer-map.html
topic: radio-iot
tags:
- radio
- learning
featured: false
read_time: 2
excerpt: >-
  RF introduces many concepts at once: frequency, modulation, antennas, packets, routing,
  and applications. A layer map helps separate physical-signal questions from protocol
  and application questions.
editorial_batch: 20261003-100-niches
---

RF introduces many concepts at once: frequency, modulation, antennas, packets, routing, and applications. The vocabulary can become heavy very quickly. I like to keep a layer map that separates questions about the physical signal from questions about communication rules and application behavior.

Suppose a message did not arrive. Maybe the signal never reached the receiver. Maybe the receiver saw energy but could not decode the packet. Maybe the route was unknown. Maybe the packet arrived but the application ignored it. Those are different failures, and layer names stop them from collapsing into one vague problem.

Learning experiments benefit from the same separation. First send one known message. Then change distance. Later introduce multiple nodes. If everything changes at once, it becomes difficult to know which concept the experiment actually tested.

The purpose of the map is not to pretend RF is simple. It is to show where we are standing inside the complexity. Once that location is clear, the next useful question usually becomes smaller.

Source: [official reference](https://lora-alliance.org/resource_hub/what-is-lorawan/).
