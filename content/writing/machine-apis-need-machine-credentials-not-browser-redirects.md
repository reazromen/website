---
title: Machine APIs Need Machine Credentials, Not Browser Redirects
url: /posts/machine-apis-need-machine-credentials-not-browser-redirects.html
date: '2025-03-28'
read_time: 1
excerpt: A firmware client cannot solve an interactive login flow, and treating the
  redirect as success hides the real authentication failure.
topic: web-control-plane
tags:
- api
- authelia
- bearer
- ota
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Authentication and Ingress · advanced'
outputs:
- url: /posts/machine-apis-need-machine-credentials-not-browser-redirects.html
  template: cms/templates/posts/posts--machine-apis-need-machine-credentials-not-browser-redirects.tpl
  source: cms/templates/posts/posts--machine-apis-need-machine-credentials-not-browser-redirects.json
---

Only the exact machine endpoints bypass Authelia, and those endpoints remain protected by device-specific Bearer credentials in the OTA API. Human routes stay behind two-factor SSO.

Public OTA device calls initially shared an ingress domain with human administration. If interactive SSO intercepted a heartbeat, the firmware received HTML or a redirect instead of the API response it expected. The ingress policy had not separated human identity from device identity. Both are authentication problems, but they use different credentials and interaction models.

Protocol boundaries should preserve the client's native authentication model. API gateways should not translate an unauthorized machine call into an unrelated browser flow.

External verification should assert status semantics, content type and redirect behavior so future proxy changes cannot silently route device traffic through the human login path. The concrete hserver evidence is commit 8940954, so this note is tied to an actual production change rather than a hypothetical failure.
