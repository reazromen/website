---
title: Local DNS Failure Can Look Like a Dead Server
url: /posts/field-note-2026-dns-failure-dead-server.html
date: '2026-09-20'
read_time: 2
excerpt: Test the known address before rebooting a host just because its name stopped
  resolving.
topic: networking
tags:
- dns
- mdns
- troubleshooting
- network
draft: false
featured: false
language: en
eyebrow: Network Reliability Field Notes · intermediate
outputs:
- url: /posts/field-note-2026-dns-failure-dead-server.html
  template: cms/templates/posts/posts--field-note-2026-dns-failure-dead-server.tpl
  source: cms/templates/posts/posts--field-note-2026-dns-failure-dead-server.json
---

# Local DNS Failure Can Look Like a Dead Server

Test the known address before rebooting a host just because its name stopped resolving.

I keep this as a field note because the failure mode is easy to misclassify: name resolution failure is mistaken for host or service failure. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Test the address path before declaring the host down.**

## Implementation pattern

Probe resolution, route, transport and application response as separate contracts.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- known address can be tested directly
- DNS differs from TCP failure
- service health is checked after reachability

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Test the address path before declaring the host down. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
