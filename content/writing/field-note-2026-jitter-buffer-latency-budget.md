---
title: Jitter Buffer Depth Is a Latency Budget
url: /posts/field-note-2026-jitter-buffer-latency-budget.html
date: '2026-06-08'
read_time: 2
excerpt: Every extra buffered frame trades conversational responsiveness for tolerance
  to arrival variation.
topic: embedded-audio-voice
tags:
- rtp
- jitter-buffer
- latency
- voip
draft: false
featured: false
language: en
eyebrow: Embedded Voice Field Notes · advanced
outputs:
- url: /posts/field-note-2026-jitter-buffer-latency-budget.html
  template: cms/templates/posts/posts--field-note-2026-jitter-buffer-latency-budget.tpl
  source: cms/templates/posts/posts--field-note-2026-jitter-buffer-latency-budget.json
---

# Jitter Buffer Depth Is a Latency Budget

Every extra buffered frame trades conversational responsiveness for tolerance to arrival variation.

I keep this as a field note because the failure mode is easy to misclassify: buffer depth is increased until crackle disappears without accounting for added mouth-to-ear delay. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Choose depth from observed jitter and a defined latency budget.**

## Implementation pattern

Track packet inter-arrival variation, late packets and occupancy, then set a bounded target depth.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- late packets are separated from lost packets
- buffer occupancy is observable
- latency is evaluated with stability

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Choose depth from observed jitter and a defined latency budget. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
