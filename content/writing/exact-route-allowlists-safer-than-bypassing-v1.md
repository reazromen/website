---
title: Exact Route Allowlists Are Safer Than Bypassing Authentication for /v1
url: /posts/exact-route-allowlists-safer-than-bypassing-v1.html
date: '2026-09-14'
read_time: 1
excerpt: A broad path prefix can expose future endpoints that did not exist when the
  exception was created.
topic: web-control-plane
tags:
- nginx
- allowlist
- api-security
- ota
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Authentication and Ingress · advanced'
outputs:
- url: /posts/exact-route-allowlists-safer-than-bypassing-v1.html
  template: cms/templates/posts/posts--exact-route-allowlists-safer-than-bypassing-v1.tpl
  source: cms/templates/posts/posts--exact-route-allowlists-safer-than-bypassing-v1.json
---

The OTA proxy needed a machine-access exception, but allowing an entire API prefix would have bypassed human SSO for enrollment, release mutation or other administrative routes added later.

Default deny and explicit allowlists are core least-privilege patterns. Security exceptions should be narrow enough that future feature growth does not silently expand the trusted surface. Prefix-based trust grows automatically with the API surface. The exception would have inherited new endpoints without a new security review. The public ingress documents and verifies four exact machine route shapes and leaves every non-allow-listed path behind Authelia.

Treat route additions as security changes when they need machine ingress. Add negative tests proving adjacent admin paths still redirect or reject access. The concrete hserver evidence is commit 8940954, so this note is tied to an actual production change rather than a hypothetical failure.
