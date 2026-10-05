---
title: AEC Only Worked Once the Reference Signal Was Actually the Far-End Audio
url: /posts/aec-only-worked-once-the-reference-signal-was-actually-the-far-end-audio.html
date: '2023-07-08'
read_time: 1
excerpt: An echo canceller cannot remove what its reference channel does not represent.
topic: embedded-firmware
tags:
- aec
- audio
- dsp
- esp32-s3
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · advanced
outputs:
- url: /posts/aec-only-worked-once-the-reference-signal-was-actually-the-far-end-audio.html
  template: cms/templates/posts/posts--aec-only-worked-once-the-reference-signal-was-actually-the-far-end-audio.tpl
  source: cms/templates/posts/posts--aec-only-worked-once-the-reference-signal-was-actually-the-far-end-audio.json
---

Acoustic echo cancellation is easy to describe and easy to wire incorrectly. The algorithm needs the microphone signal and a reference representing what was sent to the speaker. If the reference channel is wrong, delayed incorrectly or processed through a different path, the canceller is trying to model the wrong system.

That made channel mapping one of the first checks instead of the last. I traced the I2S channels, confirmed which samples represented far-end playback, and compared timing before changing suppression parameters.

The other lesson was that AEC quality depends on the whole acoustic path. Speaker volume, enclosure coupling, clipping and nonlinear distortion all make the echo harder to model. DSP settings cannot compensate for every hardware problem.

Once the reference was correct, tuning became meaningful. Before that, every parameter change was just noise around a wiring error.
