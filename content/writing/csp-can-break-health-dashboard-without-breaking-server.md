---
title: A CSP Can Break a Health Dashboard Without Breaking the Server
url: /posts/csp-can-break-health-dashboard-without-breaking-server.html
date: '2026-09-14'
read_time: 1
excerpt: Browser security policy is part of application behavior; a blocked fetch
  can make a healthy backend look unreachable.
topic: web-control-plane
tags:
- csp
- browser
- health-checks
- caddy
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Observability · intermediate'
outputs:
- url: /posts/csp-can-break-health-dashboard-without-breaking-server.html
  template: cms/templates/posts/posts--csp-can-break-health-dashboard-without-breaking-server.tpl
  source: cms/templates/posts/posts--csp-can-break-health-dashboard-without-breaking-server.json
---

The LAN Access Hub loaded correctly but its JavaScript connectivity checks could not reach the canonical Ops and OTA HTTPS endpoints. Server-side curl checks passed, which made the problem look like an application bug at first. The Content Security Policy did not include the required `connect-src` destinations. The browser was enforcing the security boundary exactly as configured, while command-line tools were outside that browser policy.

The CSP was narrowed to explicitly allow only the two reviewed HTTPS health endpoints while keeping all other cross-origin connections blocked.

CI now asserts the expected CSP header. Security policy should be tested as functional behavior so a hardening change cannot silently disable the feature it is supposed to protect. Browser debugging requires checking network policy as well as server health. CSP failures are client-enforced authorization failures, so the console and response headers are part of the diagnostic path. The concrete hserver evidence is commit cda0247, so this note is tied to an actual production change rather than a hypothetical failure.
