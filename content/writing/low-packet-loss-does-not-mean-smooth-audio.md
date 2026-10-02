---
title: Low Packet Loss Does Not Mean Smooth Audio
url: /posts/low-packet-loss-does-not-mean-smooth-audio.html
date: '2026-09-14'
read_time: 1
excerpt: Burst timing can hurt a speakerphone even when aggregate RTP loss is close
  to zero.
topic: loup-engineering
tags:
- rtp
- jitter
- packet-loss
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: SIP & RTP · advanced'
outputs:
- url: /posts/low-packet-loss-does-not-mean-smooth-audio.html
  template: cms/templates/posts/posts--low-packet-loss-does-not-mean-smooth-audio.tpl
  source: cms/templates/posts/posts--low-packet-loss-does-not-mean-smooth-audio.json
---

I stopped treating this part of LOUP as a black box while working on Low Packet Loss Does Not Mean Smooth Audio. LOUP captures showed low overall loss while still exposing bursts near 80 milliseconds and gaps around 153 to 240 milliseconds.

Aggregate loss hides arrival distribution. A few clustered delays can drain a small jitter buffer and cause a clearly audible break while the percentage still looks excellent. Arrival delta, sequence continuity and playout depth need to be read together.

Logs and measurements were used to decide whether the fault lived before or after the boundary, then the smallest falsifiable change was tested. Evidence marker: `low-loss-bursty-rtp`.

For conversational audio, when packets arrive can matter as much as whether they eventually arrive. The resulting test is small enough to rerun after later changes, which is what turns one successful experiment into engineering evidence.

## Project evidence

LOUP engineering marker: `low-loss-bursty-rtp`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
