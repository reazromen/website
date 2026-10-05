---
title: Health Probes Should Not Follow Redirects Blindly
url: /posts/health-probes-should-not-follow-redirects-blindly.html
date: '2026-03-27'
read_time: 1
excerpt: A probe that follows a redirect can report success for the wrong endpoint
  and hide an authentication or routing failure.
topic: observability
tags:
- http
- health-checks
- redirects
- security
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Observability · advanced'
outputs:
- url: /posts/health-probes-should-not-follow-redirects-blindly.html
  template: cms/templates/posts/posts--health-probes-should-not-follow-redirects-blindly.tpl
  source: cms/templates/posts/posts--health-probes-should-not-follow-redirects-blindly.json
---

The ops runner originally used a normal HTTP client for service probes, which could follow redirects automatically. A protected or misrouted endpoint might redirect to a login page and still produce a successful HTTP exchange.

The probe was testing eventual reachability instead of the exact endpoint contract. Redirect following changed the meaning of the check without making that behavior visible to the operator. The runner now installs a no-redirect handler, validates that targets are HTTPS URLs without embedded credentials, and evaluates the original response directly.

Black-box monitoring should assert the protocol behavior users or machines depend on. A 302, 401, 422 and 200 mean different things; converting them all into a final page load destroys diagnostic information. Write probes with explicit redirect, TLS, status-code and response-size policies. Monitoring clients should be less permissive than browsers because their job is to detect boundary failures, not work around them. The concrete hserver evidence is commit bdd8b2e, so this note is tied to an actual production change rather than a hypothetical failure.
