---
title: Jitter Buffers Are a Trade Between Missing Audio and Late Audio
url: /posts/jitter-buffers-are-a-trade-between-missing-audio-and-late-audio.html
date: '2026-09-14'
read_time: 1
excerpt: A larger jitter buffer can hide network variation while quietly making conversation
  worse through extra delay.
topic: telecom-voip
tags:
- rtp
- jitter-buffer
- latency
- audio
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · advanced
outputs:
- url: /posts/jitter-buffers-are-a-trade-between-missing-audio-and-late-audio.html
  template: cms/templates/posts/posts--jitter-buffers-are-a-trade-between-missing-audio-and-late-audio.tpl
  source: cms/templates/posts/posts--jitter-buffers-are-a-trade-between-missing-audio-and-late-audio.json
---

The first response to choppy RTP is often to increase the jitter buffer. That can work and it can also turn an interactive call into a delayed conversation.

A jitter buffer exists because packets do not arrive at perfectly regular intervals. It holds enough media to absorb variation and then releases frames on a steadier playout clock. If the buffer is too small, late packets miss their deadline. If it is too large, the call accumulates unnecessary mouth-to-ear delay.

I began looking at burst size, packet interval and late-arrival distribution instead of choosing a buffer by feel. Rebuffer events are especially important because they create audible discontinuities even if average packet loss is low.

The useful target is not maximum smoothness. It is the smallest buffer that handles the expected network variation without frequent underruns. That trade-off became central once RTP moved onto Wi-Fi and embedded hardware where both network timing and local scheduling could add jitter.
