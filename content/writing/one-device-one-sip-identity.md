---
title: One Device, One SIP Identity
url: /posts/one-device-one-sip-identity.html
date: '2026-09-14'
read_time: 1
excerpt: Sharing SIP credentials across devices makes revocation, auditing and fleet
  diagnosis ambiguous.
topic: loup-engineering
tags:
- sip-identity
- device-identity
- security
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Product Architecture · advanced'
outputs:
- url: /posts/one-device-one-sip-identity.html
  template: cms/templates/posts/posts--one-device-one-sip-identity.tpl
  source: cms/templates/posts/posts--one-device-one-sip-identity.json
---

One Device, One SIP Identity became a separate note because the failure crossed more than one subsystem. Each LOUP unit needs a unique telephony identity even when several devices belong to the same household or backend account.

A unique account lets the backend disable one device, rotate one credential, observe one registration and correlate one call path without affecting every unit. It also makes transfer and retirement states implementable because ownership changes do not require keeping a global credential alive.

The fix came from assigning one owner to the behaviour and refusing to hide a hardware or network fault with an unrelated firmware workaround. Evidence marker: `unique-sip-account`.

Per-device identity creates operational control. Shared credentials save setup work early and create incident-response problems later. The value is not only the fix itself; it is having a repeatable way to prove the same class of failure has not returned.

## Project evidence

LOUP engineering marker: `unique-sip-account`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
