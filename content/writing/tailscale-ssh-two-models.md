---
title: Tailscale SSH and Ordinary SSH over Tailscale Are Two Different Models
url: /posts/tailscale-ssh-two-models.html
date: '2025-04-06'
read_time: 2
excerpt: I can send SSH packets over the tailnet without asking Tailscale to become
  the SSH authentication system.
topic: security-identity
tags:
- tailscale-ssh
- openssh
- access-control
- linux
draft: false
featured: false
language: en
eyebrow: Tailscale in My Home Infrastructure · intermediate
outputs:
- url: /posts/tailscale-ssh-two-models.html
  template: cms/templates/posts/posts--tailscale-ssh-two-models.tpl
  source: cms/templates/posts/posts--tailscale-ssh-two-models.json
---

# Tailscale SSH and Ordinary SSH over Tailscale Are Two Different Models

I can send SSH packets over the tailnet without asking Tailscale to become the SSH authentication system.

This distinction became important in my own setup. A host can be reachable through its Tailscale address while a Tailscale SSH policy denies a particular login. That does not mean the tailnet is down; it means authentication or authorization rejected the session.

## The setup I use

In one model, normal OpenSSH listens on the host and Tailscale only provides the private network path. In the other, Tailscale SSH is enabled and Tailscale manages authentication and authorization for connections to the node's Tailscale port 22.

## Commands and configuration

```
# Enable Tailscale SSH on a Linux destination
sudo tailscale set --ssh

# Disable it again, after confirming another access path exists
sudo tailscale set --ssh=false
```

## Where this usually fails

The failure mode is mixing the two models. An operator changes Tailscale SSH policy while automation expects ordinary OpenSSH, or enables Tailscale SSH and is surprised that existing tailnet SSH behavior changes.

## The rule I keep

**Decide explicitly whether Tailscale owns only the network path or both the path and SSH authorization, then document that choice per host.**

That rule is more useful to me than memorising one command because it identifies which layer owns the decision. Tailscale is excellent at creating a private, authenticated IP network between machines, but I still keep application state, Reticulum state, SSH authorization and public ingress as explicit layers.

## References

- https://tailscale.com/docs/features/tailscale-ssh
