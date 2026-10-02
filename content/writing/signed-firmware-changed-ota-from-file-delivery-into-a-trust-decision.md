---
title: Signed Firmware Changed OTA from File Delivery into a Trust Decision
url: /posts/signed-firmware-changed-ota-from-file-delivery-into-a-trust-decision.html
date: '2026-09-14'
read_time: 1
excerpt: A device should decide whether firmware is authorized, not merely whether
  the download completed successfully.
topic: embedded-firmware
tags:
- ota
- firmware-signing
- ecdsa
- security
draft: false
featured: false
language: en
eyebrow: 2025 Voice and Infrastructure Notes · advanced
outputs:
- url: /posts/signed-firmware-changed-ota-from-file-delivery-into-a-trust-decision.html
  template: cms/templates/posts/posts--signed-firmware-changed-ota-from-file-delivery-into-a-trust-decision.tpl
  source: cms/templates/posts/posts--signed-firmware-changed-ota-from-file-delivery-into-a-trust-decision.json
---

A checksum can tell me that a firmware image arrived intact. It cannot tell me who authorized that image, which is the distinction that matters once an OTA server becomes part of a production trust chain.

Signing changes the trust model. The release process signs an artifact with a private key; the device verifies it with a public key before accepting the update. The OTA server can distribute the file without becoming the final authority on whether the device should run it.

This also forced key-management questions into the design. The signing key must not live on the build machine casually. Public verification keys need a rotation strategy. Version policy still matters because a perfectly valid old image may be unsafe to reinstall.

The useful separation is integrity, authenticity and policy. Hashes help with integrity. Signatures establish authenticity. The device's release policy decides whether an authentic image is acceptable right now.
