---
title: A Reference Softphone Is Valuable Because It Is Not the Device Under Test
url: /posts/a-reference-softphone-is-valuable-because-it-is-not-the-device-under-test.html
date: '2023-08-31'
read_time: 1
excerpt: Linphone provides a known endpoint for separating PBX problems from embedded
  endpoint problems.
topic: loup-engineering
tags:
- linphone
- reference-endpoint
- sip
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: PBX & Network · advanced'
outputs:
- url: /posts/a-reference-softphone-is-valuable-because-it-is-not-the-device-under-test.html
  template: cms/templates/posts/posts--a-reference-softphone-is-valuable-because-it-is-not-the-device-under-test.tpl
  source: cms/templates/posts/posts--a-reference-softphone-is-valuable-because-it-is-not-the-device-under-test.json
---

The practical ownership question in A Reference Softphone Is Valuable Because It Is Not the Device Under Test was simple to state and harder to prove. LOUP used Linphone alongside the ESP32-S3 endpoint, with acoustic processing settings such as ARC controlled during A/B tests.

If device-to-Linphone fails while Linphone-to-Linphone works, the evidence points differently than a failure affecting every endpoint. A reference client also makes SIP/SDP comparison easier because its behaviour is well understood and independently observable.

The debugging order stayed conservative: verify wiring and state transitions first, then tune performance only after correctness had been established. Evidence marker: `linphone-reference`.

Keep at least one trusted implementation in a protocol lab. Interoperability is a powerful debugging instrument. The broader result is a system that can be changed incrementally because each layer has a measurable responsibility and a known recovery path.

## Project evidence

LOUP engineering marker: `linphone-reference`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
