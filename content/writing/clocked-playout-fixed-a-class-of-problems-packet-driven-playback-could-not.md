---
title: Clocked Playout Fixed a Class of Problems Packet-Driven Playback Could Not
url: /posts/clocked-playout-fixed-a-class-of-problems-packet-driven-playback-could-not.html
date: '2026-09-14'
read_time: 1
excerpt: RTP arrival time should not directly schedule the speaker.
topic: loup-engineering
tags:
- rtp
- playout
- clock
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Audio Pipeline · advanced'
outputs:
- url: /posts/clocked-playout-fixed-a-class-of-problems-packet-driven-playback-could-not.html
  template: cms/templates/posts/posts--clocked-playout-fixed-a-class-of-problems-packet-driven-playback-could-not.tpl
  source: cms/templates/posts/posts--clocked-playout-fixed-a-class-of-problems-packet-driven-playback-could-not.json
---

Clocked Playout Fixed a Class of Problems Packet-Driven Playback Could Not became a separate note because the failure crossed more than one subsystem. V116 moved the receive path toward clocked playout so network burstiness stopped dictating I2S timing.

Packets can arrive early, late or in small bursts even on a healthy network. The speaker still needs a steady sample cadence. Decoupling arrival from consumption lets the jitter buffer absorb network timing while the local audio clock controls output. That also makes drift visible as queue growth or depletion instead of random crackle.

The fix came from assigning one owner to the behaviour and refusing to hide a hardware or network fault with an unrelated firmware workaround. Evidence marker: `clocked-playout`.

Transport timing and playback timing are different clocks. A robust endpoint has to bridge them deliberately. The value is not only the fix itself; it is having a repeatable way to prove the same class of failure has not returned.

## Project evidence

LOUP engineering marker: `clocked-playout`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
