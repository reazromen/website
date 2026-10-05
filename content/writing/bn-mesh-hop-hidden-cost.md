---
title: The Hidden Cost of One More Hop in a Mesh Network
date: '2025-04-10'
draft: false
language: en
url: /posts/bn-mesh-hop-hidden-cost.html
topic: lora-reticulum
tags:
- mesh
- latency
featured: false
read_time: 2
excerpt: >-
  An additional route in a mesh is useful, but every extra hop makes the message wait at
  another point. Receiving, processing, and retransmitting all consume time and resources.
  More links do not create free capacity.
editorial_batch: 20261003-100-niches
---

An additional route in a mesh is useful, but every extra hop makes the message wait at another point. Receiving, processing, and retransmitting all consume time and resources. More links on a topology diagram do not create free capacity.

On a low-bandwidth network, a message that crosses several hops consumes airtime at each stage. Other messages may be competing for the same radio time. The final device's experience therefore depends on more than the quality of its own link; congestion along the path matters too.

Testing should record not only whether the message arrived, but how long it took and how many attempts were required. A route change can change those numbers. Having an alternate path after failure and getting the same performance over that path are two different claims.

Mesh networking is attractive because it creates alternative paths, but those paths still have a resource cost. Making hop cost visible helps decide which traffic is urgent, which can wait, and where a new link would actually help.

Source: [official reference](https://reticulum.network/manual/understanding.html).
