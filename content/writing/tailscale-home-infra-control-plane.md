---
title: Why Tailscale Became the Control Plane for My Home Infrastructure
url: /posts/tailscale-home-infra-control-plane.html
date: '2025-03-20'
read_time: 2
excerpt: I do not use Tailscale as a generic VPN. I use it as the stable identity
  and reachability layer between my laptop, desktop and home server.
topic: linux-homelab
tags:
- tailscale
- homelab
- wireguard
- home-server
draft: false
featured: false
language: en
eyebrow: Tailscale in My Home Infrastructure · intermediate
outputs:
- url: /posts/tailscale-home-infra-control-plane.html
  template: cms/templates/posts/posts--tailscale-home-infra-control-plane.tpl
  source: cms/templates/posts/posts--tailscale-home-infra-control-plane.json
---

# Why Tailscale Became the Control Plane for My Home Infrastructure

I do not use Tailscale as a generic VPN. I use it as the stable identity and reachability layer between my laptop, desktop and home server.

My home infrastructure has several machines that are not always on the same LAN: a home server, a laptop, a desktop worker and occasionally a phone. The useful thing Tailscale gives me is not merely encrypted packets. It gives each machine a stable tailnet identity even when the underlay changes.

## The setup I use

The home server remains the long-lived service host. The laptop or desktop can become the current operator or automation worker. The worker reaches the server through the tailnet when local naming is unreliable or when it is outside the house. I still keep LAN access because the LAN is often the shortest path, but Tailscale is the continuity layer that makes location less important.

## Commands and configuration

```
tailscale status
tailscale ip -4
tailscale ping hserver
```

## Where this usually fails

The most common mistake is to treat Tailscale as if it replaces every other network layer. It does not. DNS can fail, SSH policy can deny a user, the application can be down, or the peer can be reachable only through a relay. I separate peer reachability from login authorization and from application health.

## The rule I keep

**Use Tailscale as stable machine identity and secure reachability; keep service health, SSH authorization and application routing as separate contracts.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://tailscale.com/docs/how-to/quickstart
