---
title: Where Should a Message Wait for an Offline Node?
date: '2020-08-12'
draft: false
language: en
url: /posts/bn-radio-offline-store-forward.html
topic: lora-reticulum
tags:
- mesh
- storage
featured: false
read_time: 2
excerpt: >-
  Communication is simpler if every node is assumed to be continuously available. Real
  nodes disappear because of power, radio conditions, or the environment. Then the design
  has to decide where a message waits and how long it remains relevant.
editorial_batch: 20261003-100-niches
---

Communication is simpler if every node is assumed to be continuously available. Real nodes disappear because of power, radio conditions, or the environment. Then the design has to decide where a message waits and how long it remains relevant.

Suppose an old sensor observation arrives much later. The observation may still be historically true while no longer representing the current state. Creation time and delivery time have to remain separate, and decisions need limits on how stale a delayed message may be.

The place holding messages has finite storage. Which messages should be retained? Can a newer state replace an older one? How are duplicates recognized? Simply having a queue does not complete the offline behavior design.

What I like about disconnected networks is that they force us to think about time as part of the message. A message has a lifetime as well as a route. *Who will receive it?* and *when will they receive it?* are equally important questions.

Source: [official reference](https://reticulum.network/manual/networks.html).
