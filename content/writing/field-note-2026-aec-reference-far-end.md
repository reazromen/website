---
title: AEC Reference Is the Far-End Signal, Not Another Microphone
url: /posts/field-note-2026-aec-reference-far-end.html
date: '2026-04-21'
read_time: 2
excerpt: Echo cancellation only has a useful reference when the reference represents
  what the loudspeaker actually played.
topic: embedded-audio-voice
tags:
- aec
- esp32-s3
- i2s
- voice
draft: false
featured: false
language: en
eyebrow: Embedded Voice Field Notes · advanced
outputs:
- url: /posts/field-note-2026-aec-reference-far-end.html
  template: cms/templates/posts/posts--field-note-2026-aec-reference-far-end.tpl
  source: cms/templates/posts/posts--field-note-2026-aec-reference-far-end.json
---

# AEC Reference Is the Far-End Signal, Not Another Microphone

Echo cancellation only has a useful reference when the reference represents what the loudspeaker actually played.

I keep this as a field note because the failure mode is easy to misclassify: the microphone, reference and playback channels can all contain valid audio while representing different physical signals. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Feed AEC with the far-end playback signal and keep the microphone path separate.**

## Implementation pattern

Trace network decode -> playback PCM -> AEC reference and trace microphone ADC -> AEC mic input as two distinct paths.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- channel identity is known at the codec boundary
- reference advances with playback
- raw-mic bypass is available

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Feed AEC with the far-end playback signal and keep the microphone path separate. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
