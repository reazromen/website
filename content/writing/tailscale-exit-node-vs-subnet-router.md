---
title: Exit Node or Subnet Router? I Choose Based on Which Traffic Must Move
url: /posts/tailscale-exit-node-vs-subnet-router.html
date: '2026-09-18'
read_time: 2
excerpt: Both features route packets through another tailnet device, but they solve
  different problems.
topic: networking
tags:
- tailscale
- exit-node
- subnet-router
- routing
draft: false
featured: false
language: en
eyebrow: Tailscale in My Home Infrastructure · beginner
outputs:
- url: /posts/tailscale-exit-node-vs-subnet-router.html
  template: cms/templates/posts/posts--tailscale-exit-node-vs-subnet-router.tpl
  source: cms/templates/posts/posts--tailscale-exit-node-vs-subnet-router.json
---

# Exit Node or Subnet Router? I Choose Based on Which Traffic Must Move

Both features route packets through another tailnet device, but they solve different problems.

I use one question to choose between these features: am I trying to reach a private network behind a node, or am I trying to send general internet traffic through that node?

## The setup I use

A subnet router makes selected private prefixes reachable. An exit node becomes the default path for non-tailnet internet traffic when a client opts into using it. On a laptop away from home, an exit node can make internet egress come from the home connection. For reaching a LAN-only sensor, a subnet route is the smaller tool.

## Commands and configuration

```
# On a node intended to advertise exit-node capability
sudo tailscale set --advertise-exit-node

# Client-side selection is explicit and should be verified
tailscale status
```

## Where this usually fails

Using an exit node when only one private subnet is needed changes much more traffic than necessary. It can also affect local-network access unless the client is configured to allow it.

## The rule I keep

**Route only the traffic the use case requires: private prefixes with subnet routes, general egress with an explicitly selected exit node.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://tailscale.com/docs/features/exit-nodes
- https://tailscale.com/docs/features/subnet-routers
