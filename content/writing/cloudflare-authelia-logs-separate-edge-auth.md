---
title: Cloudflare and Authelia Logs Explain Edge Failures Differently
url: /posts/cloudflare-authelia-logs-separate-edge-auth.html
date: '2026-09-14'
read_time: 1
excerpt: A public request can fail before reaching Authelia, inside the authentication
  flow, or after authentication while the upstream application is unavailable.
topic: observability-monitoring
tags:
- cloudflare
- authelia
- loki
- edge-logs
draft: false
featured: false
language: en
eyebrow: 'Hserver Monitoring: Logs & Security · advanced'
outputs:
- url: /posts/cloudflare-authelia-logs-separate-edge-auth.html
  template: cms/templates/posts/posts--cloudflare-authelia-logs-separate-edge-auth.tpl
  source: cms/templates/posts/posts--cloudflare-authelia-logs-separate-edge-auth.json
---

A public request can fail before reaching Authelia, inside the authentication flow, or after authentication while the upstream application is unavailable. What made the issue measurable was `separate Cloudflare and Authelia log streams`. Keeping edge transport and identity logs distinct lets an operator place the failure at the right layer instead of searching one combined stream.

I classify this as layered log topology. The useful debugging sequence is to confirm the signal, compare it with the neighboring subsystem, then look at logs or detailed metrics only after the failure domain is smaller.

The production rule that came out of it is: Preserve service identifiers and query both timelines around the same timestamp while avoiding unbounded labels such as client IP in Prometheus. This is deliberately more specific than adding another broad alert with no response procedure.

Commit `b65d5d4` is the repository evidence behind the note. It provides the concrete configuration or fix that turned the observation into a repeatable monitoring control.
