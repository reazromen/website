---
title: A 422 Can Be Healthier Than a 302 for a Device API
url: /posts/422-healthier-than-302-device-api.html
date: '2026-09-14'
read_time: 1
excerpt: For an intentionally invalid API payload, validation failure proves the request
  reached the correct application boundary.
topic: web-control-plane
tags:
- http
- api-testing
- status-codes
- ota
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Authentication and Ingress · intermediate'
outputs:
- url: /posts/422-healthier-than-302-device-api.html
  template: cms/templates/posts/posts--422-healthier-than-302-device-api.tpl
  source: cms/templates/posts/posts--422-healthier-than-302-device-api.json
---

The OTA endpoint verifier sends an empty JSON object to heartbeat and events. The expected result is not 200; it is a validation error from the API. A 302 would mean the proxy diverted the machine request to SSO.

Success had to be defined in terms of the test objective rather than a generic 2xx status. The probe wants evidence that routing and API parsing are correct, not evidence that the intentionally bad payload was accepted. Acceptance checks expect HTTP 422 on those invalid POSTs, while artifact probes accept authentication or not-found errors and admin paths must return the SSO redirect.

Contract testing uses meaningful negative cases. Status codes are part of the interface and can prove which layer handled the request. Build endpoint tests around expected semantics, including failure responses, so proxies and auth layers cannot regress while every simplistic 200-only health check stays green. The concrete hserver evidence is commit 8940954, so this note is tied to an actual production change rather than a hypothetical failure.
