---
title: A SIP Endpoint on an Embedded Device Changed My Definition of 'Small'
url: /posts/a-sip-endpoint-on-an-embedded-device-changed-my-definition-of-small.html
date: '2026-09-14'
read_time: 1
excerpt: Once SIP, RTP, codecs, Wi-Fi and a UI share one MCU, memory and timing decisions
  stop being implementation details.
topic: embedded-firmware
tags:
- sip
- rtp
- esp32
- embedded-voice
draft: false
featured: false
language: en
eyebrow: 2024 Telecom and Embedded Notes · advanced
outputs:
- url: /posts/a-sip-endpoint-on-an-embedded-device-changed-my-definition-of-small.html
  template: cms/templates/posts/posts--a-sip-endpoint-on-an-embedded-device-changed-my-definition-of-small.tpl
  source: cms/templates/posts/posts--a-sip-endpoint-on-an-embedded-device-changed-my-definition-of-small.json
---

A SIP softphone on a desktop can assume memory, threads and network buffers are plentiful. On an embedded device every subsystem competes for the same limited CPU and RAM.

The signalling side was not the expensive part by itself. RTP buffering, codec state, audio DMA, Wi-Fi retries, UI updates and TLS could all overlap. A harmless allocation spike during call setup could become a stability problem if audio buffers were already near their limit.

I started budgeting memory by subsystem and measuring high-water marks during calls instead of trusting idle-state numbers. Timing received the same treatment: network callbacks should not block audio, UI work should not delay packet handling, and reconnect logic should not run inside a critical path.

That exercise changed the architecture. The device had to be designed as a real-time networked system, not a collection of features squeezed onto a board. The smaller the hardware, the more explicit those boundaries had to become.
