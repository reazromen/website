---
title: Human SSO and Machine Authentication Should Not Share One Gate
url: /posts/human-sso-and-machine-authentication-should-not-share-one-gate.html
date: '2026-04-21'
read_time: 1
excerpt: Firmware cannot complete an interactive Authelia login, but bypassing authentication
  entirely would expose the OTA control plane.
topic: web-control-plane
tags:
- authelia
- ota
- bearer-token
- ingress
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/human-sso-and-machine-authentication-should-not-share-one-gate.html
  template: cms/templates/posts/posts--human-sso-and-machine-authentication-should-not-share-one-gate.tpl
  source: cms/templates/posts/posts--human-sso-and-machine-authentication-should-not-share-one-gate.json
---

The public OTA hostname needed to serve both human administration and device traffic. Putting every route behind interactive SSO caused firmware API calls to receive redirects, while removing SSO from the whole host would expose administrative surfaces.

This is authentication boundary decomposition. Machine-to-machine credentials and human interactive identity should meet at explicit route boundaries rather than one mechanism being weakened to accommodate the other. Two client classes had different authentication capabilities and threat models. A single ingress rule could not correctly represent both.

The proxy now allow-lists only the exact machine routes, which bypass human SSO but still require per-device Bearer authentication at the OTA API. Admin and all other routes continue to redirect through Authelia.

Test representative status codes externally: machine validation errors must remain API responses, invalid artifacts must remain unauthorized or missing, and admin paths must still redirect to SSO. The concrete hserver evidence is commit 8940954, so this note is tied to an actual production change rather than a hypothetical failure.
