---
title: How I Use a Tailscale Subnet Router to Reach Devices That Cannot Run Tailscale
url: /posts/tailscale-subnet-router-home-lan.html
date: '2024-01-31'
read_time: 2
excerpt: The tailnet can reach printers, embedded devices and LAN-only services without
  installing a Tailscale client on every endpoint.
topic: networking
tags:
- tailscale
- subnet-router
- lan
- routing
draft: false
featured: false
language: en
eyebrow: Tailscale in My Home Infrastructure · intermediate
outputs:
- url: /posts/tailscale-subnet-router-home-lan.html
  template: cms/templates/posts/posts--tailscale-subnet-router-home-lan.tpl
  source: cms/templates/posts/posts--tailscale-subnet-router-home-lan.json
---

# How I Use a Tailscale Subnet Router to Reach Devices That Cannot Run Tailscale

The tailnet can reach printers, embedded devices and LAN-only services without installing a Tailscale client on every endpoint.

Not every device in a home lab can run Tailscale. Embedded boards, appliances and temporary test devices may only exist on the local subnet. A subnet router is the clean bridge for that case.

## The setup I use

I enable IP forwarding on the Linux gateway, advertise only the private subnet I actually need, approve that route in the tailnet policy, and then test from a remote tailnet node. This is different from an exit node: the subnet router exposes selected private networks rather than sending all internet traffic through the gateway.

## Commands and configuration

```
sudo sysctl -w net.ipv4.ip_forward=1
sudo tailscale set --advertise-routes=192.168.0.0/24
tailscale status
```

## Where this usually fails

Advertising a broad route is easy, but it expands the reachable network. The safer pattern is to advertise the smallest useful subnet and enforce access with tailnet policy. Route advertisement also does not prove the LAN target itself accepts the connection.

## The rule I keep

**Use subnet routing for specific private networks; keep internet egress and device authorization as separate decisions.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://tailscale.com/docs/features/subnet-routers
- https://tailscale.com/docs/features/subnet-routers/how-to/setup
