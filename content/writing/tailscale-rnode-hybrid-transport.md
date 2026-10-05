---
title: Combining an RNode LoRa Link and a Tailscale TCP Link in One Reticulum System
url: /posts/tailscale-rnode-hybrid-transport.html
date: '2026-04-26'
read_time: 2
excerpt: The interesting architecture is not choosing radio or IP; it is letting Reticulum
  use different interfaces for different reachability conditions.
topic: lora-reticulum
tags:
- rnode
- lora
- tailscale
- reticulum
draft: false
featured: false
language: en
eyebrow: Tailscale + Reticulum · advanced
outputs:
- url: /posts/tailscale-rnode-hybrid-transport.html
  template: cms/templates/posts/posts--tailscale-rnode-hybrid-transport.tpl
  source: cms/templates/posts/posts--tailscale-rnode-hybrid-transport.json
---

# Combining an RNode LoRa Link and a Tailscale TCP Link in One Reticulum System

The interesting architecture is not choosing radio or IP; it is letting Reticulum use different interfaces for different reachability conditions.

My Reticulum setup includes an RNode radio interface for local LoRa experiments. A Tailscale-backed TCP interface solves a different problem: connecting Reticulum instances across IP networks. Reticulum can have both interfaces configured at the same time.

## The setup I use

The RNode path gives me a radio transport independent of normal IP. The Tailscale TCP path gives me a private long-distance IP transport between trusted machines. I do not tunnel LoRa packets through Tailscale and call that the same radio path; I expose two real Reticulum interfaces and let the stack understand them as separate transports.

## Commands and configuration

```
[interfaces]

  [[Khulna RNode]]
    type = RNodeInterface
    enabled = yes
    port = /dev/rnode
    # radio parameters omitted here

  [[Remote Reticulum over Tailnet]]
    type = TCPClientInterface
    enabled = yes
    target_host = <remote-tailnet-node>
    target_port = 4242
```

## Where this usually fails

If the two interfaces are collapsed conceptually, it becomes impossible to tell whether a message used radio, IP or a transport node. That matters for range testing, reliability measurement and understanding why a path exists.

## The rule I keep

**Expose each physical or virtual transport honestly; let Reticulum compose reachability instead of hiding one transport inside another.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://reticulum.network/manual/interfaces.html
