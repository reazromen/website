---
title: One Ingress Is Easier to Reason About Than Three
url: /posts/field-note-2026-one-ingress.html
date: '2026-09-18'
read_time: 2
excerpt: Every extra reverse proxy adds another place for routing, TLS and headers
  to disagree.
topic: linux-homelab
tags:
- caddy
- ingress
- docker
- homelab
draft: false
featured: false
language: en
eyebrow: Home Infrastructure Field Notes · intermediate
outputs:
- url: /posts/field-note-2026-one-ingress.html
  template: cms/templates/posts/posts--field-note-2026-one-ingress.tpl
  source: cms/templates/posts/posts--field-note-2026-one-ingress.json
---

# One Ingress Is Easier to Reason About Than Three

Every extra reverse proxy adds another place for routing, TLS and headers to disagree.

I keep this as a field note because the failure mode is easy to misclassify: services accumulate multiple reverse proxies with unclear hostname ownership. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Prefer one canonical ingress boundary unless a second one has a documented isolation reason.**

## Implementation pattern

Map each hostname to exactly one ingress owner and keep application containers on internal ports.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- each hostname has one owner
- TLS termination is known
- public ports are intentional

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Prefer one canonical ingress boundary unless a second one has a documented isolation reason. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
