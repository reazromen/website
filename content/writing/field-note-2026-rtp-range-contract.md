---
title: The RTP Port Range Is Part of the Deployment Contract
url: /posts/field-note-2026-rtp-range-contract.html
date: '2026-09-18'
read_time: 2
excerpt: Media ports must agree across PBX configuration, firewall policy, containers
  and the surrounding network.
topic: telecom-voip
tags:
- rtp
- firewall
- docker
- asterisk
draft: false
featured: false
language: en
eyebrow: VoIP Field Notes · intermediate
outputs:
- url: /posts/field-note-2026-rtp-range-contract.html
  template: cms/templates/posts/posts--field-note-2026-rtp-range-contract.tpl
  source: cms/templates/posts/posts--field-note-2026-rtp-range-contract.json
---

# The RTP Port Range Is Part of the Deployment Contract

Media ports must agree across PBX configuration, firewall policy, containers and the surrounding network.

I keep this as a field note because the failure mode is easy to misclassify: SIP is exposed correctly while the selected media ports never reach the endpoint. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Treat RTP range changes like interface changes that every network boundary must understand.**

## Implementation pattern

Document one deliberate media range and verify host listening state, container mapping and packet arrival.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- configured range matches deployment rules
- packet capture sees media at the host
- one-way audio is tested in both directions

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Treat RTP range changes like interface changes that every network boundary must understand. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
