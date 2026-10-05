---
title: PBX Registration Health Is Not Call Health
url: /posts/pbx-registration-health-is-not-call-health.html
date: '2024-11-28'
read_time: 1
excerpt: A green registration table can coexist with broken dialog routing or media.
topic: loup-engineering
tags:
- pbx
- registration
- health
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: PBX & Network · advanced'
outputs:
- url: /posts/pbx-registration-health-is-not-call-health.html
  template: cms/templates/posts/posts--pbx-registration-health-is-not-call-health.tpl
  source: cms/templates/posts/posts--pbx-registration-health-is-not-call-health.json
---

The acceptance condition for PBX Registration Health Is Not Call Health only became clear after the system was split into boundaries. LOUP devices can remain registered while an INVITE route, codec negotiation or RTP path is failing.

Monitoring registration is useful because it proves periodic signalling and credential validity, but production acceptance also needs test calls or synthetic call-path evidence. Server health should represent the actual service users depend on, not the easiest table to query.

The design became clearer when configuration, runtime state and recovery behaviour were specified separately instead of being implied by implementation details. Evidence marker: `registration-vs-call-health`.

Health signals should follow the user journey. Presence in a registry is only one layer of telephony availability. Once that contract is written down, firmware and server changes can be reviewed against the same expectation instead of relying on memory.

## Project evidence

LOUP engineering marker: `registration-vs-call-health`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
