---
title: Rate Limiting Is Not Authentication
url: /posts/rate-limiting-is-not-authentication.html
date: '2024-12-26'
read_time: 1
excerpt: The public machine API uses request throttling as abuse resistance while
  retaining Bearer validation as the real identity check.
topic: web-control-plane
tags:
- rate-limiting
- authentication
- nginx
- api
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Authentication and Ingress · advanced'
outputs:
- url: /posts/rate-limiting-is-not-authentication.html
  template: cms/templates/posts/posts--rate-limiting-is-not-authentication.tpl
  source: cms/templates/posts/posts--rate-limiting-is-not-authentication.json
---

Once OTA machine routes were exposed publicly, nginx rate limits became useful for reducing accidental or abusive request volume. It would have been easy to overstate that control as part of device authentication.

Defense in depth works when each layer has a clear job. Rate limiting protects capacity; authentication establishes identity; authorization decides allowed operations. Availability controls and identity controls solve different threats. A caller under the rate limit can still be unauthorized, and an authenticated caller can still generate excessive traffic. The ingress applies method restrictions and rate limiting, while the OTA API continues to validate per-device Bearer credentials independently.

Keep those controls independently testable. Never remove API authentication because a proxy sits in front, and never assume valid credentials make request-volume controls unnecessary. The concrete hserver evidence is commit 8940954, so this note is tied to an actual production change rather than a hypothetical failure.
