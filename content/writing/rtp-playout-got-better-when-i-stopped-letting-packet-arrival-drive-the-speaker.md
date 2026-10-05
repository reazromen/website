---
title: RTP Playout Got Better When I Stopped Letting Packet Arrival Drive the Speaker
url: /posts/rtp-playout-got-better-when-i-stopped-letting-packet-arrival-drive-the-speaker.html
date: '2026-01-22'
read_time: 1
excerpt: Network arrival time is not an audio clock. A stable playout schedule needs
  its own timing and buffer policy.
topic: embedded-firmware
tags:
- rtp
- jitter-buffer
- esp32-s3
- audio
draft: false
featured: false
language: en
eyebrow: 2026 Production Voice Systems · advanced
outputs:
- url: /posts/rtp-playout-got-better-when-i-stopped-letting-packet-arrival-drive-the-speaker.html
  template: cms/templates/posts/posts--rtp-playout-got-better-when-i-stopped-letting-packet-arrival-drive-the-speaker.tpl
  source: cms/templates/posts/posts--rtp-playout-got-better-when-i-stopped-letting-packet-arrival-drive-the-speaker.json
---

One of the worst ways to play RTP is also one of the easiest to implement: receive a packet and immediately push its samples toward the speaker. It sounds acceptable on a perfect LAN and falls apart as soon as packet arrival starts to bunch up.

The fix was to make playout clock-driven. RTP packets enter a jitter buffer, while a separate schedule consumes one audio frame at a time at the codec rate. Network arrival can then vary without directly changing the speaker timing.

That exposed the next problem: rebuffer policy. If the buffer drains, I need a deliberate threshold for pausing, refilling and resuming. If it grows continuously, there may be clock drift rather than ordinary jitter. Logging buffer depth over a long call was more useful than listening to a thirty-second test.

The important distinction is simple. The network transports audio frames; it should not be the clock that plays them. Giving playout its own timing source made the buffer measurable and turned random crackle into a scheduling problem I could actually instrument.
