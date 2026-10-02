---
title: Clocked Playout Beats Packet-Driven Audio
url: /posts/field-note-2026-clocked-playout.html
date: '2026-09-18'
read_time: 2
excerpt: Network packets arrive when the network allows; speakers need samples when
  the audio clock demands them.
topic: embedded-audio-voice
tags:
- rtp
- jitter
- i2s
- audio
draft: false
featured: false
language: en
eyebrow: Embedded Voice Field Notes · advanced
outputs:
- url: /posts/field-note-2026-clocked-playout.html
  template: cms/templates/posts/posts--field-note-2026-clocked-playout.tpl
  source: cms/templates/posts/posts--field-note-2026-clocked-playout.json
---

# Clocked Playout Beats Packet-Driven Audio

Network packets arrive when the network allows; speakers need samples when the audio clock demands them.

I keep this as a field note because the failure mode is easy to misclassify: packet arrival timing gets coupled directly to the speaker write schedule. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Let the audio clock own playout; let the network only refill a bounded buffer.**

## Implementation pattern

Receive RTP into a jitter buffer and consume one frame on a stable playout cadence.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- playout cadence stays stable during bursty arrival
- underrun and overrun counters are visible
- rebuffering has an explicit threshold

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Let the audio clock own playout; let the network only refill a bounded buffer. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
