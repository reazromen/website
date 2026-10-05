---
title: Where Tailscale Serve Fits Beside Caddy and a Public Cloudflare Tunnel
url: /posts/tailscale-serve-vs-caddy-cloudflare.html
date: '2025-10-12'
read_time: 2
excerpt: Private tailnet publishing and public internet publishing are different ingress
  jobs, even when they reach the same container.
topic: linux-homelab
tags:
- tailscale-serve
- caddy
- cloudflare-tunnel
- ingress
draft: false
featured: false
language: en
eyebrow: Tailscale in My Home Infrastructure · intermediate
outputs:
- url: /posts/tailscale-serve-vs-caddy-cloudflare.html
  template: cms/templates/posts/posts--tailscale-serve-vs-caddy-cloudflare.tpl
  source: cms/templates/posts/posts--tailscale-serve-vs-caddy-cloudflare.json
---

# Where Tailscale Serve Fits Beside Caddy and a Public Cloudflare Tunnel

Private tailnet publishing and public internet publishing are different ingress jobs, even when they reach the same container.

My home infrastructure already has a public ingress path for selected services. Tailscale Serve gives me another tool: expose a local service only to tailnet members over the node's tailnet HTTPS name.

## The setup I use

For a temporary or private dashboard, Serve can proxy a local port directly to the tailnet. Current Tailscale syntax can be as simple as tailscale serve 3000 for a local service on port 3000. Public publishing is a different decision and belongs in a public ingress path such as Caddy plus a tunnel, or Tailscale Funnel when that is intentionally chosen.

## Commands and configuration

```
tailscale serve 3000
tailscale serve status

# Remove Serve configuration when it is no longer needed
tailscale serve reset
```

## Where this usually fails

The mistake is to keep adding ingress layers until nobody knows which one owns a hostname. I want one owner for public routing and an explicit reason when a second private-only route exists.

## The rule I keep

**Use Serve for tailnet-only exposure; keep public ingress as a separate, intentionally reviewed boundary.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://tailscale.com/docs/features/tailscale-serve
- https://tailscale.com/docs/reference/examples/serve
- https://tailscale.com/docs/features/tailscale-funnel
