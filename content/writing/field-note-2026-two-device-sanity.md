---
title: Two-Device Local Calling Is the Fastest Telephony Sanity Check
url: /posts/field-note-2026-two-device-sanity.html
date: '2026-08-18'
read_time: 2
excerpt: A small closed call loop isolates core SIP/RTP behavior before carrier and
  DID complexity is introduced.
topic: telecom-voip
tags:
- sip
- rtp
- test-strategy
- pbx
draft: false
featured: false
language: en
eyebrow: VoIP Field Notes · intermediate
outputs:
- url: /posts/field-note-2026-two-device-sanity.html
  template: cms/templates/posts/posts--field-note-2026-two-device-sanity.tpl
  source: cms/templates/posts/posts--field-note-2026-two-device-sanity.json
---

# Two-Device Local Calling Is the Fastest Telephony Sanity Check

A small closed call loop isolates core SIP/RTP behavior before carrier and DID complexity is introduced.

I keep this as a field note because the failure mode is easy to misclassify: external trunks are added before the basic device-to-device media path is stable. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Prove the smallest closed call loop before expanding the system boundary.**

## Implementation pattern

Keep two controlled accounts and test calls in both directions as a permanent regression path.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- A can call B and B can call A
- both directions carry intelligible audio
- repeated calls recover cleanly

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Prove the smallest closed call loop before expanding the system boundary. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
