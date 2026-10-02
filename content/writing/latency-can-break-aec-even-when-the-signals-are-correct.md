---
title: Latency Can Break AEC Even When the Signals Are Correct
url: /posts/latency-can-break-aec-even-when-the-signals-are-correct.html
date: '2026-09-14'
read_time: 1
excerpt: A valid reference that arrives at the wrong time can be almost as useless
  as the wrong reference.
topic: loup-engineering
tags:
- aec
- latency
- alignment
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: AEC & DSP · advanced'
outputs:
- url: /posts/latency-can-break-aec-even-when-the-signals-are-correct.html
  template: cms/templates/posts/posts--latency-can-break-aec-even-when-the-signals-are-correct.tpl
  source: cms/templates/posts/posts--latency-can-break-aec-even-when-the-signals-are-correct.json
---

The acceptance condition for Latency Can Break AEC Even When the Signals Are Correct only became clear after the system was split into boundaries. LOUP audio passed through codec, buffers, sample-rate conversion and RTP playout, so the far-end reference and microphone echo had to remain time-aligned.

An adaptive filter searches over a finite delay span. Extra buffering or inconsistent scheduling can move the acoustic echo outside the effective alignment region or make the delay vary faster than adaptation can follow. Measuring reference-to-microphone timing is therefore part of AEC validation.

The design became clearer when configuration, runtime state and recovery behaviour were specified separately instead of being implied by implementation details. Evidence marker: `aec-latency-alignment`.

Signal identity and signal timing are equally important inputs to an echo canceller. Once that contract is written down, firmware and server changes can be reviewed against the same expectation instead of relying on memory.

## Project evidence

LOUP engineering marker: `aec-latency-alignment`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
