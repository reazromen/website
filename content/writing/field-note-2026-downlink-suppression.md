---
title: When Downlink Suppression Makes Speech Worse
url: /posts/field-note-2026-downlink-suppression.html
date: '2026-07-31'
read_time: 2
excerpt: A processor that removes noise can also remove speech detail when its assumptions
  do not match the signal.
topic: embedded-audio-voice
tags:
- dsp
- noise-suppression
- speech
- audio
draft: false
featured: false
language: en
eyebrow: Embedded Voice Field Notes · advanced
outputs:
- url: /posts/field-note-2026-downlink-suppression.html
  template: cms/templates/posts/posts--field-note-2026-downlink-suppression.tpl
  source: cms/templates/posts/posts--field-note-2026-downlink-suppression.json
---

# When Downlink Suppression Makes Speech Worse

A processor that removes noise can also remove speech detail when its assumptions do not match the signal.

I keep this as a field note because the failure mode is easy to misclassify: multiple DSP stages stay enabled because each sounds useful in isolation. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Every DSP stage must earn its place with a controlled A/B comparison.**

## Implementation pattern

Bypass suppression, AGC, resampling and other stages one at a time while holding source and volume constant.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- one stage changes per comparison
- raw decoded audio remains available
- volume is held constant

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Every DSP stage must earn its place with a controlled A/B comparison. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
