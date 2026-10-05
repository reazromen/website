---
title: CSP connect-src Should Be a Small Network Allowlist
url: /posts/csp-connect-src-small-network-allowlist.html
date: '2024-06-02'
read_time: 1
excerpt: Browser-side health checks needed cross-origin access, but the fix was two
  explicit origins rather than a broad wildcard.
topic: web-control-plane
tags:
- csp
- connect-src
- browser-security
- least-privilege
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Authentication and Ingress · advanced'
outputs:
- url: /posts/csp-connect-src-small-network-allowlist.html
  template: cms/templates/posts/posts--csp-connect-src-small-network-allowlist.tpl
  source: cms/templates/posts/posts--csp-connect-src-small-network-allowlist.json
---

`connect-src` was added with only those two HTTPS origins, while the rest of the restrictive CSP stayed intact. The Access Hub needed JavaScript to probe two HTTPS dashboards, and the original CSP blocked those connections. Relaxing CSP globally would have fixed the feature while weakening the page's network boundary. The required browser capability was narrow: connect to exactly the canonical Ops and OTA origins. The policy had not encoded that legitimate use case.

Security-policy changes should grant the smallest capability that satisfies the application. A CSP is most useful when exceptions are specific enough to reveal unexpected new dependencies.

Assert critical CSP directives in CI and review origin additions like network firewall changes rather than ordinary frontend configuration. The concrete hserver evidence is commit cda0247, so this note is tied to an actual production change rather than a hypothetical failure.
