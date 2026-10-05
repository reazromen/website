---
title: When SSH Fails, Separate the Failure Layers
date: '2024-09-01'
draft: false
language: en
url: /posts/bn-ssh-network-service-auth-layers.html
topic: networking
tags:
- ssh
- debugging
featured: false
read_time: 2
excerpt: >-
  "SSH is not working" can mean several different things: the address is wrong, there is
  no route, nothing is listening on the port, or authentication failed. Restarting the
  server is not the universal answer.
editorial_batch: 20261003-100-niches
---

"SSH is not working" can mean several different things: the address is wrong, there is no route, nothing is listening on the port, or authentication failed. Restarting the server is not the universal answer. The error itself often helps divide the problem.

A connection timeout and a rejected identity are not the same event. In the first case, the network path may be the problem. In the second, reaching the SSH server has already been demonstrated. Without that distinction, it is easy to waste time changing passwords for a routing problem.

Testing the same host through different authorized paths can be useful. If LAN access, an overlay network, and a public path produce different results, a boundary becomes visible. Each path can also have its own configuration and access policy.

Good troubleshooting accumulates small truths: how far did the request get, where did it stop, and which claims remain unknown? Once those are written down, the next change can be targeted instead of starting with the largest possible intervention.

Source: [official reference](https://www.openssh.com/manual.html).
