---
title: ECDSA Signing Makes the Device Verify Who Produced the Firmware
url: /posts/ecdsa-signing-makes-the-device-verify-who-produced-the-firmware.html
date: '2025-03-21'
read_time: 1
excerpt: Transport security alone does not prove an artifact should be trusted after
  download.
topic: loup-engineering
tags:
- ecdsa
- signed-ota
- firmware
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: OTA & Release Engineering · advanced'
outputs:
- url: /posts/ecdsa-signing-makes-the-device-verify-who-produced-the-firmware.html
  template: cms/templates/posts/posts--ecdsa-signing-makes-the-device-verify-who-produced-the-firmware.tpl
  source: cms/templates/posts/posts--ecdsa-signing-makes-the-device-verify-who-produced-the-firmware.json
---

The bench evidence for ECDSA Signing Makes the Device Verify Who Produced the Firmware forced a narrower explanation than the original assumption. LOUP OTA acceptance includes server-side signing and ESP32-side ECDSA verification before a candidate image is installed or promoted.

The signature binds the release artifact to a trusted signing key independent of the HTTP path that delivered it. That protects against an untrusted mirror, corrupted storage or a compromised delivery layer serving an unsigned replacement.

Verification included both the happy path and the failure path because a feature that works once is not yet a production contract. Evidence marker: `ecdsa-signed-ota`.

Firmware authenticity should be verified by the device itself. Delivery and trust are separate layers. For a voice product, that kind of boundary discipline matters because audio, signalling and hardware symptoms often look deceptively similar.

## Project evidence

LOUP engineering marker: `ecdsa-signed-ota`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
