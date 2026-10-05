---
title: SDP Is Where Signalling Hands the Call to Media
url: /posts/sdp-is-where-signalling-hands-the-call-to-media.html
date: '2025-07-04'
read_time: 1
excerpt: A SIP call can connect perfectly and still carry no useful audio if the negotiated
  media description is wrong.
topic: loup-engineering
tags:
- sdp
- rtp
- codec
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: SIP & RTP · advanced'
outputs:
- url: /posts/sdp-is-where-signalling-hands-the-call-to-media.html
  template: cms/templates/posts/posts--sdp-is-where-signalling-hands-the-call-to-media.tpl
  source: cms/templates/posts/posts--sdp-is-where-signalling-hands-the-call-to-media.json
---

The useful question in SDP Is Where Signalling Hands the Call to Media was where the behaviour actually originated. LOUP depends on SDP to learn codec, IP address and RTP port information for the media stream.

One-way audio often begins with a correct SIP dialog and an incorrect media address, port or codec expectation. Reading the offer and answer next to the RTP capture tells us whether packets are being sent where the endpoint actually agreed to receive them.

I treated the known-good configuration as a control sample, changed only the layer under investigation, and recorded the regression or improvement before the next experiment. Evidence marker: `sdp-media-contract`.

Signalling success and media success are separate acceptance layers joined by SDP. Keeping the rule explicit means the same decision can be checked again on the next board revision or firmware branch.

## Project evidence

LOUP engineering marker: `sdp-media-contract`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
