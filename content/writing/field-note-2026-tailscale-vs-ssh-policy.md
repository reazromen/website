---
title: Tailscale Connectivity and Tailscale SSH Are Different Permissions
url: /posts/field-note-2026-tailscale-vs-ssh-policy.html
date: '2026-03-14'
read_time: 2
excerpt: A peer can be reachable over the tailnet while an SSH login is correctly
  denied by another policy layer.
topic: networking
tags:
- tailscale
- ssh
- acl
- access-control
draft: false
featured: false
language: en
eyebrow: Network Reliability Field Notes · intermediate
outputs:
- url: /posts/field-note-2026-tailscale-vs-ssh-policy.html
  template: cms/templates/posts/posts--field-note-2026-tailscale-vs-ssh-policy.tpl
  source: cms/templates/posts/posts--field-note-2026-tailscale-vs-ssh-policy.json
---

# Tailscale Connectivity and Tailscale SSH Are Different Permissions

A peer can be reachable over the tailnet while an SSH login is correctly denied by another policy layer.

I keep this as a field note because the failure mode is easy to misclassify: active peer status is treated as proof that every SSH user is allowed. The useful move is to identify the boundary first, then change only the layer that owns it.

## What I model

The system is easier to debug when intent, observation and transport are not collapsed into one state. For this case, my rule is simple: **Reachable does not mean authorized.**

## Implementation pattern

Test peer connectivity separately from SSH user policy and record whether automation uses Tailscale SSH or normal OpenSSH.

I prefer a small explicit contract over a clever implicit one. That gives logs, tests and dashboards something concrete to verify and keeps unrelated layers from compensating for each other.

## What I verify

- peer connectivity is independent
- policy denial is recognized
- automation specifies host and user

## Failure handling

When one of those checks fails, I preserve the failing evidence before restarting or changing configuration. The first broken contract determines the next investigation. That keeps troubleshooting causal instead of turning it into a sequence of guesses.

## What I keep

Reachable does not mean authorized. The specific tools can change, but that ownership boundary remains useful across firmware, networks and infrastructure.
