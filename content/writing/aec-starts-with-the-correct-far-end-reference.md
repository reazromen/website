---
title: AEC Starts with the Correct Far-End Reference
url: /posts/aec-starts-with-the-correct-far-end-reference.html
date: '2026-07-22'
read_time: 1
excerpt: An echo canceller cannot remove playback it never receives as a reference
  signal.
topic: loup-engineering
tags:
- aec
- reference-channel
- es7210
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: AEC & DSP · advanced'
outputs:
- url: /posts/aec-starts-with-the-correct-far-end-reference.html
  template: cms/templates/posts/posts--aec-starts-with-the-correct-far-end-reference.tpl
  source: cms/templates/posts/posts--aec-starts-with-the-correct-far-end-reference.json
---

The first engineering constraint behind AEC Starts with the Correct Far-End Reference was concrete: LOUP AEC expected far-end playback on channel 0 and microphone audio on channel 1 or 3, so channel identity had to be verified before tuning.

A wrong reference can make the algorithm look unstable, underpowered or badly tuned even when the DSP itself is functioning exactly as designed. Raw channel capture and controlled playback let us prove which slot contained the far-end signal and which carried the microphone.

I kept the experiment narrow by changing one variable, capturing the observable result, and comparing it with a preserved working build before moving on. Evidence marker: `aec-ref-committed`.

DSP tuning begins after signal plumbing is correct. Reference integrity is a prerequisite, not a parameter. In practice that keeps the next LOUP change measurable because the baseline remains available for comparison.

## Project evidence

LOUP engineering marker: `aec-ref-committed`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
