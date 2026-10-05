---
title: An RTP Timestamp Is Not Wall-Clock Time
date: '2023-12-25'
draft: false
language: en
url: /posts/bn-rtp-timestamp-not-wall-clock.html
topic: telecom-voip
tags:
- rtp
- time
featured: false
read_time: 2
excerpt: >-
  A timestamp inside a packet can look like a clock reading, but RTP timestamps primarily
  describe position in the media clock. Wall-clock time, media time, and packet arrival
  time are different concepts.
editorial_batch: 20261003-100-niches
---

A timestamp inside a packet can look like a clock reading, but RTP timestamps primarily describe position in the media clock. They help reconstruct the timing of audio samples; they do not directly tell you the current time of day. Wall-clock time, media time, and packet arrival time need to remain distinct when reading a trace.

Imagine equal-duration audio frames generated at regular intervals but delivered by the network at irregular times. Their media timestamps still describe the regular media timeline. Arrival times describe network behavior. Comparing the two is useful, but subtracting them as if they were the same kind of clock requires careful interpretation.

Sequence numbers answer another question. They help track packet order; timestamps describe temporal position in the media stream. Loss, reordering, and playback timing should not be collapsed into one symptom. Before interpreting any protocol field, understand what that field was designed to represent.

This distinction extends beyond telephony. Sensor data, video, and logs can all carry several meanings of time: creation, collection, arrival, and display. A timestamp becomes much more useful when its semantics are explicit. A precise number attached to the wrong event still tells the wrong story.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc3550.html).
