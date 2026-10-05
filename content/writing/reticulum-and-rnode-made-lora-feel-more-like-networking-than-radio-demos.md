---
title: Reticulum and RNode Made LoRa Feel More Like Networking Than Radio Demos
url: /posts/reticulum-and-rnode-made-lora-feel-more-like-networking-than-radio-demos.html
date: '2022-10-20'
read_time: 1
excerpt: Once identity, addressing and transport were layered over LoRa, the experiment
  stopped being just two radios sending bytes.
topic: radio-iot
tags:
- reticulum
- rnode
- lora
- lr1121
draft: false
featured: false
language: en
eyebrow: 2026 Production Voice Systems · advanced
outputs:
- url: /posts/reticulum-and-rnode-made-lora-feel-more-like-networking-than-radio-demos.html
  template: cms/templates/posts/posts--reticulum-and-rnode-made-lora-feel-more-like-networking-than-radio-demos.tpl
  source: cms/templates/posts/posts--reticulum-and-rnode-made-lora-feel-more-like-networking-than-radio-demos.json
---

A raw LoRa link is easy to demonstrate: configure frequency and spreading factor, send bytes, receive bytes. Reticulum made the experiment more interesting because the radio became one interface inside a larger networking model.

The RNode handles the physical radio side while Reticulum deals with identities, destinations and transport. That separation is useful because the application does not need to know every modem command. A LoRa interface, TCP interface or another bearer can participate in the same higher-level system.

The lab also forced RF basics back into the discussion. Frequency, bandwidth, spreading factor, coding rate and antenna choice still determine whether packets make it across the link. A clever network layer cannot rescue a badly matched antenna or an illegal regional configuration.

What I liked most was the layering. The radio remained simple, while the network above it could route and identify endpoints in a way that felt much closer to real systems engineering than a serial echo test.
