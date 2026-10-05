---
title: 'My Tailscale Failure Drill for a Home Server: Name, Peer, Policy, Port, Service'
url: /posts/tailscale-failure-drill.html
date: '2024-07-13'
read_time: 2
excerpt: I troubleshoot from the network boundary inward so I do not restart a healthy
  server because one naming or authorization layer failed.
topic: networking
tags:
- tailscale
- troubleshooting
- ssh
- home-server
draft: false
featured: false
language: en
eyebrow: Tailscale in My Home Infrastructure · intermediate
outputs:
- url: /posts/tailscale-failure-drill.html
  template: cms/templates/posts/posts--tailscale-failure-drill.tpl
  source: cms/templates/posts/posts--tailscale-failure-drill.json
---

# My Tailscale Failure Drill for a Home Server: Name, Peer, Policy, Port, Service

I troubleshoot from the network boundary inward so I do not restart a healthy server because one naming or authorization layer failed.

A failed remote command can come from several independent layers. The fastest recovery method is to identify the first failed contract instead of changing all of them at once.

## The setup I use

I check whether the expected peer exists, whether Tailscale can ping it, whether the destination port is reachable, whether the chosen SSH model authorizes the user, and only then whether the Docker service is healthy. If LAN naming such as .local fails, I test the tailnet identity before declaring the server offline.

## Commands and configuration

```
tailscale status
tailscale ping hserver

# Then, depending on the intended access model:
ssh <server-user>@hserver

# Finally verify the application on the server:
docker ps
```

## Where this usually fails

Restarting networking, Tailscale and Docker together may restore service, but it destroys the evidence needed to understand the incident. The same failure then returns as a mystery.

## The rule I keep

**Name the failed layer before changing configuration: discovery -> tailnet reachability -> access policy -> transport -> application.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://tailscale.com/docs/reference/tailscale-cli/status
- https://tailscale.com/docs/reference/tailscale-cli/ping
- https://tailscale.com/docs/features/tailscale-ssh
