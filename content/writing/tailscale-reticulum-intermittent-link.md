---
title: What Happens to Reticulum When the Tailscale Path Drops and Returns
url: /posts/tailscale-reticulum-intermittent-link.html
date: '2022-12-09'
read_time: 2
excerpt: The useful property is not that the IP path never fails; it is that the transport
  can recover without redefining the whole Reticulum network.
topic: lora-reticulum
tags:
- reticulum
- tailscale
- resilience
- tcpinterface
draft: false
featured: false
language: en
eyebrow: Tailscale + Reticulum · advanced
outputs:
- url: /posts/tailscale-reticulum-intermittent-link.html
  template: cms/templates/posts/posts--tailscale-reticulum-intermittent-link.tpl
  source: cms/templates/posts/posts--tailscale-reticulum-intermittent-link.json
---

# What Happens to Reticulum When the Tailscale Path Drops and Returns

The useful property is not that the IP path never fails; it is that the transport can recover without redefining the whole Reticulum network.

Home networks move between Wi-Fi, Ethernet, ISP changes and NAT states. A tailnet path can change underneath a long-running Reticulum transport.

## The setup I use

Reticulum's TCP interface implementation is designed to tolerate intermittent IP links and re-establish connectivity when the peer becomes reachable again. I still monitor the interface because automatic recovery is not the same as instant recovery or guaranteed application delivery.

## Commands and configuration

```
tailscale status
tailscale ping hserver
rnstatus
```

## Where this usually fails

If I only watch the Reticulum application, I may blame identity or path discovery for what was actually an underlay outage. If I only watch Tailscale, I may miss a Reticulum interface that never returned to the expected state.

## The rule I keep

**Monitor both layers and let each layer report its own failure domain: Tailscale for IP reachability, Reticulum for Reticulum path and interface state.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://reticulum.network/manual/interfaces.html
