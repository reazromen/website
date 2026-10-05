---
title: Airtime Is a Budget Too
date: '2024-08-06'
draft: false
language: en
url: /posts/bn-radio-airtime-budget.html
topic: radio-iot
tags:
- radio
- capacity
featured: false
read_time: 2
excerpt: >-
  A sensor message may contain only a few bytes, but many sensors can share the same radio
  medium. The important question is not only how much data exists, but how long each
  transmission occupies that shared medium.
editorial_batch: 20261003-100-niches
---

A sensor message may contain only a few bytes, but many sensors can share the same radio medium. The important question is not only how much data exists, but how long each transmission occupies that shared medium. Ignoring airtime can turn a network of tiny messages into a congested network.

If every device reports status very frequently, much of the traffic may simply repeat the same state. Separating meaningful changes from periodic liveness reports can make the traffic easier to reason about. Sending everything less often is not automatically the answer either, because failure detection may then become too slow.

A useful plan identifies message classes, timing requirements, and retry behavior. Retries on a weak link can increase medium occupancy precisely when conditions are already poor. Normal-operation tests should therefore be complemented by stressed-condition tests.

I think of radio capacity as sharing time to speak. Every node may have something important to say, but they cannot all occupy the medium at once. Protocol discipline is an attempt to use that limited time deliberately.

Source: [official reference](https://lora-alliance.org/resource_hub/what-is-lorawan/).
