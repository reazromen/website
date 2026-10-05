---
title: "Jitter Buffer: Paying With Delay for Continuous Audio"
date: '2024-11-09'
draft: false
language: en
url: /posts/bn-jitter-buffer-waiting-price.html
topic: embedded-audio-voice
tags:
- rtp
- audio
featured: false
read_time: 2
excerpt: >-
  Audio packets do not arrive at perfectly regular intervals even when they travel the
  same network path. A jitter buffer waits long enough to smooth that variation, but the
  waiting itself increases conversational latency.
editorial_batch: 20261003-100-niches
---

Audio packets do not arrive at perfectly regular intervals even when they travel the same network path. Some arrive early, some later. If every packet is played immediately on arrival, that variation can become gaps in the sound. A jitter buffer waits briefly and turns irregular arrivals into a more regular playback schedule. The interesting part is that the same waiting also increases conversational latency. The solution and part of the cost live in the same mechanism.

A small buffer can feel responsive but has less room for late packets. A large buffer can absorb more variation, but the other person hears your speech later. There is no universal rule that the biggest buffer is best. The useful setting depends on how much network delay varies, how strict the playback deadline is, and what kind of conversation people are having.

Compare recorded speech with a live phone call. A little extra delay may be nearly invisible in the recording. In a conversation, the same delay can make both people start speaking at once because each thinks the other has gone quiet. Audio quality is therefore not only about clarity; turn-taking is part of the experience too.

When debugging, look beyond average latency and inspect its distribution. Packet send time, arrival time, and playback deadline are three different clocks. Not all delay comes from the network either; device scheduling and audio buffering contribute as well. A jitter buffer is a controlled tradeoff. The goal is not zero waiting at any cost, but continuity with a delay budget you understand.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc3550.html).
