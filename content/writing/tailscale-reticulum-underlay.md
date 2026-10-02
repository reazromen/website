---
title: Using Tailscale as the IP Underlay for Reticulum
url: /posts/tailscale-reticulum-underlay.html
date: '2026-09-18'
read_time: 2
excerpt: Reticulum does not need Tailscale, but its TCP interfaces can use a Tailscale
  path just like any other private IP network.
topic: lora-reticulum
tags:
- tailscale
- reticulum
- tcpinterface
- mesh
draft: false
featured: false
language: en
eyebrow: Tailscale + Reticulum · advanced
outputs:
- url: /posts/tailscale-reticulum-underlay.html
  template: cms/templates/posts/posts--tailscale-reticulum-underlay.tpl
  source: cms/templates/posts/posts--tailscale-reticulum-underlay.json
---

# Using Tailscale as the IP Underlay for Reticulum

Reticulum does not need Tailscale, but its TCP interfaces can use a Tailscale path just like any other private IP network.

The useful mental model is layered: Reticulum remains the networking system that handles Reticulum identities, paths and transport behavior; Tailscale provides a private IP underlay between machines that may be on different physical networks.

## The setup I use

On the stationary home server, I can run a Reticulum TCPServerInterface. On another tailnet machine, a TCPClientInterface can target the server's tailnet hostname or Tailscale address. The Reticulum manual explicitly supports TCP interfaces across private IPv4/IPv6 networks and notes that TCP client links can recover when the IP link disappears and reappears.

## Commands and configuration

```
# Server-side Reticulum idea
[[Tailnet TCP Server]]
  type = TCPServerInterface
  enabled = yes
  listen_ip = <hserver-tailnet-ip>
  listen_port = 4242

# Remote Reticulum node
[[Hserver over Tailscale]]
  type = TCPClientInterface
  enabled = yes
  target_host = <hserver-tailnet-name>
  target_port = 4242
```

## Where this usually fails

The layers should not be confused. A Tailscale peer can be reachable while the Reticulum interface is misconfigured, and Reticulum can keep other interfaces working even when the Tailscale path disappears.

## The rule I keep

**Treat Tailscale as one transport path underneath Reticulum, not as a replacement for Reticulum routing or identity.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://reticulum.network/manual/interfaces.html
