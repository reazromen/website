---
title: Working DNS Does Not Mean the Application Is Healthy
date: '2021-08-26'
draft: false
language: en
url: /posts/bn-dns-path-not-application-health.html
topic: networking
tags:
- dns
- debugging
featured: false
read_time: 2
excerpt: >-
  Resolving a domain to an address is an important first step, but DNS cannot tell you
  whether the service is reachable, the certificate matches, or the application itself
  is working. Successful name resolution is not system health.
editorial_batch: 20261003-100-niches
---

Resolving a domain to an address is an important first step, but DNS cannot tell you whether the service is reachable, the certificate matches, or the application itself is working. Successful name resolution is not system health.

Suppose the domain resolves to the correct address but the reverse proxy routes to the wrong service. The user sees the wrong page. Or the proxy may be correct while the backend application is down. The same domain-level complaint can come from several layers.

Testing should therefore separate name resolution, connectivity, TLS, routing, and application response. Evidence from each step narrows the next question. Changing DNS for every failure is not a useful debugging strategy.

A simple network map helps here: which name resolves where, which component receives the connection next, and which application ultimately handles the request? Once that path is visible, a domain stops looking like a mysterious switch.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc1034.html).
