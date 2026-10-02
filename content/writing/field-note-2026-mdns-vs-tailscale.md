---
title: mDNS and Tailscale Fail in Different Ways
url: /posts/field-note-2026-mdns-vs-tailscale.html
date: '2026-09-18'
read_time: 2
excerpt: A .local name and a Tailscale peer can refer to the same host while depending
  on different discovery systems.
topic: linux-homelab
tags:
- mdns
- tailscale
- dns
- ssh
draft: false
featured: false
language: en
eyebrow: Home Infrastructure Field Notes · intermediate
outputs:
- url: /posts/field-note-2026-mdns-vs-tailscale.html
  template: cms/templates/posts/posts--field-note-2026-mdns-vs-tailscale.tpl
  source: cms/templates/posts/posts--field-note-2026-mdns-vs-tailscale.json
---

# mDNS and Tailscale Fail in Different Ways

A .local name and a Tailscale peer can refer to the same host while depending on different discovery systems.

I keep this as a field note because the failure mode is easy to misclassify: one failed name is mistaken for complete server downtime. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Do not use one naming mechanism as proof of host availability.**

## Implementation pattern

Test local name, LAN address, overlay peer and service port independently.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- LAN and overlay reachability are separate
- resolution errors differ from TCP errors
- automation has a deterministic fallback

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Do not use one naming mechanism as proof of host availability. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
