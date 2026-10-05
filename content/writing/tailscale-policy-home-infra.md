---
title: I Treat Tailscale Access Policy as Infrastructure Code
url: /posts/tailscale-policy-home-infra.html
date: '2021-07-10'
read_time: 2
excerpt: Once the tailnet becomes a real operational network, who can reach which
  host and service should not live only in memory.
topic: security-identity
tags:
- tailscale
- access-control
- grants
- security
draft: false
featured: false
language: en
eyebrow: Tailscale in My Home Infrastructure · advanced
outputs:
- url: /posts/tailscale-policy-home-infra.html
  template: cms/templates/posts/posts--tailscale-policy-home-infra.tpl
  source: cms/templates/posts/posts--tailscale-policy-home-infra.json
---

# I Treat Tailscale Access Policy as Infrastructure Code

Once the tailnet becomes a real operational network, who can reach which host and service should not live only in memory.

A small home lab can begin with allow-everything access and still work. As more services, automation workers and devices join, implicit trust becomes harder to reason about.

## The setup I use

I separate machine role from user identity and keep access rules small enough to audit. The home server may accept admin traffic from operator machines while a dashboard may be reachable from more devices. SSH is stricter than ordinary HTTPS. Reticulum transport can have its own port-level rule.

## Commands and configuration

```
tailscale status

# Policy changes are made in the tailnet access-control configuration.
# I verify the result from the source machine instead of assuming the rule matched.
```

## Where this usually fails

A policy can be syntactically valid and still deny the wrong source, allow too much, or use the wrong host identity. Access tests should therefore be part of deployment verification.

## The rule I keep

**Network membership is not blanket authorization; express service access explicitly and verify from the real source node.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://tailscale.com/docs/features/access-control
