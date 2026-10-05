---
title: SIP Registration Is an Address, Not Complete Proof of Liveness
date: '2024-01-20'
draft: false
language: en
url: /posts/bn-sip-registration-expiry-liveness.html
topic: telecom-voip
tags:
- sip
- state
featured: false
read_time: 2
excerpt: >-
  SIP registration records a relationship between an identity and a reachable contact
  address. That address being present does not prove the phone is fully usable at this
  moment. Registration is a memory of recent state, and expiry defines how long that memory is trusted.
editorial_batch: 20261003-100-niches
---

SIP registration records a relationship between an identity and a reachable contact address. That address being present does not prove the phone is fully usable at this moment. The phone may have moved networks, lost a NAT mapping, or stalled in its audio stack. The server's registration is then a memory of an earlier state, and expiry defines how long that memory is trusted.

A very short expiry forces the phone to register frequently, increasing signaling and potentially affecting battery-powered devices. A very long expiry can leave stale contacts around after a device disappears. There is no universal ideal interval. A mobile endpoint, a stable LAN phone, and a Wi-Fi device that moves between networks do not have identical behavior.

It helps to separate levels of liveness: knowing a contact address, reaching the device, establishing a call, and exchanging media are different claims. Passing one level does not prove the next. If a dashboard says online, the word needs a definition or operators may treat an audio failure as impossible because the registration indicator is green.

I prefer status that states its own limits. Last registration time, last successful interaction, and the exact probe that was performed make troubleshooting easier. Registration is useful evidence, but turning it into a full certificate of conversation readiness makes a larger claim than the data supports.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc3261.html).
