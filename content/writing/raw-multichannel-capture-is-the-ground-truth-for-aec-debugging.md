---
title: Raw Multichannel Capture Is the Ground Truth for AEC Debugging
url: /posts/raw-multichannel-capture-is-the-ground-truth-for-aec-debugging.html
date: '2024-08-31'
read_time: 1
excerpt: Processed audio alone hides whether the wrong signal entered the algorithm.
topic: loup-engineering
tags:
- aec
- raw-capture
- multichannel
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: AEC & DSP · advanced'
outputs:
- url: /posts/raw-multichannel-capture-is-the-ground-truth-for-aec-debugging.html
  template: cms/templates/posts/posts--raw-multichannel-capture-is-the-ground-truth-for-aec-debugging.tpl
  source: cms/templates/posts/posts--raw-multichannel-capture-is-the-ground-truth-for-aec-debugging.json
---

The lab result behind Raw Multichannel Capture Is the Ground Truth for AEC Debugging changed the implementation more than the first hypothesis did. The most informative LOUP AEC tests preserved raw microphone and reference channels before processing.

A raw capture lets the same input be replayed through different algorithms offline, compared channel by channel and checked for clipping, routing errors and timing. It also separates hardware capture from live DSP behavior because the data can be inspected after the call.

Reversibility stayed part of the experiment: preserve the previous artifact, make the change, then prove the new path before promoting it. Evidence marker: `raw-channel-capture`.

Keep observability before transformation. Once signals are mixed or suppressed, evidence about the original failure may be gone. Preserving that distinction is what lets the project increase complexity without losing the ability to explain a regression.

## Project evidence

LOUP engineering marker: `raw-channel-capture`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
