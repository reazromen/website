---
title: Secure ESP32 OTA Is a Chain of Trust, Not an HTTPS Download
url: /posts/secure-esp32-ota-chain-of-trust.html
date: '2026-09-26'
read_time: 9
excerpt: HTTPS protects a firmware transfer in transit. A production OTA design also
  has to prove image authenticity, select boot slots safely, confirm health, permit
  recovery, and prevent rollback to revoked vulnerable firmware.
topic: ''
tags:
- esp32
- ota
- secure-boot
- anti-rollback
draft: false
featured: false
language: en
eyebrow: Embedded Security · systems note
outputs:
- url: /posts/secure-esp32-ota-chain-of-trust.html
  template: cms/templates/posts/posts--secure-esp32-ota-chain-of-trust.tpl
  source: cms/templates/posts/posts--secure-esp32-ota-chain-of-trust.json
---

Putting an ESP32 firmware binary behind HTTPS is a good start.

It is not a secure OTA architecture.

Transport security answers one question: was the connection to the update server protected against network tampering under the trust model of TLS?

The device still needs answers for image authenticity, boot selection, health confirmation, rollback, security version, key management, and failure during flash writes.

## Start at the build artifact[#](#start-at-the-build-artifact)

A useful chain is:

```
source
 -> build
 -> signed application image
 -> release metadata
 -> HTTPS transport
 -> inactive OTA slot
 -> bootloader verification
 -> first-boot self-test
 -> mark valid
 -> future anti-rollback policy
```

If any transition is implicit, that is where operational ambiguity accumulates.

## Secure Boot protects what executes[#](#secure-boot-protects-what-executes)

With Secure Boot enabled, the boot process verifies signed software before execution according to the platform's secure-boot configuration.

That gives the device an authenticity boundary independent of the network path. A compromised update server cannot simply serve arbitrary unsigned firmware and expect the bootloader to run it.

This is different from HTTPS. TLS authenticates the server connection; Secure Boot authenticates the executable image under the device's boot trust.

## Flash Encryption protects confidentiality at rest[#](#flash-encryption-protects-confidentiality-at-rest)

Flash Encryption addresses a different property: making flash contents unreadable/use-limited outside the intended device security context.

Espressif recommends combining it with Secure Boot. During OTA, encryption can be handled by the device as data is written to flash.

Again: confidentiality and authenticity are different controls.

## A/B slots are about recoverability[#](#a-b-slots-are-about-recoverability)

ESP-IDF OTA commonly uses multiple application slots plus OTA metadata that tells the bootloader which image to try.

The critical behavior is first boot after update.

With rollback enabled, the new image enters a pending-verification state. The application runs self-tests and explicitly marks itself valid. If it crashes, resets, or loses power before successful confirmation, the bootloader can return to the previous working image.

This turns “download succeeded” into “release proved it can operate.”

## Your health check defines success[#](#your-health-check-defines-success)

A firmware can boot and still be unusable.

The self-test should reflect the product's minimum safe operation: critical peripherals initialize, configuration/storage schema is readable, required security material is accessible, watchdog loops are not tripping, and perhaps a limited network/service check succeeds.

Do not make the confirmation so late that ordinary network outages cause healthy firmware to roll back. Do not make it so early that broken core functionality is marked valid.

## Anti-rollback is intentionally irreversible in places[#](#anti-rollback-is-intentionally-irreversible-in-places)

ESP-IDF's anti-rollback mechanism compares the application's security version against a version stored in eFuse.

This solves a real problem: a perfectly signed old release can still contain a vulnerability that should no longer be bootable.

But eFuse-based security state raises the cost of mistakes. Increasing or revoking security state needs staged rollout discipline because you can remove old recovery options.

A good pattern is to deploy and validate the fixed firmware broadly before advancing the minimum security version.

## Key rotation belongs in the design[#](#key-rotation-belongs-in-the-design)

Secure Boot v2 devices can support multiple public-key digests depending on the chip family/configuration, allowing planned signing-key rotation and revocation.

The fleet needs a documented procedure for:

- introducing a new signing key,
- shipping firmware trusted by both old and new state where needed,
- confirming adoption,
- revoking the old key only after recovery paths are safe.

Key rotation that exists only in a datasheet is not an operational control.

## Power failure is part of OTA[#](#power-failure-is-part-of-ota)

ESP-IDF's OTA metadata uses redundant sectors to tolerate interruption while boot selection state is updated.

Your own release metadata and application migration logic need similar thinking. What happens if power disappears after new config is written but before firmware is marked valid? Can the previous firmware still read the data?

Firmware compatibility with persistent-state migrations is often the hidden rollback blocker.

## The control plane should know device state[#](#the-control-plane-should-know-device-state)

A fleet system should distinguish at least:

```
download started
image verified
slot selected
rebooted
pending verification
healthy / marked valid
rolled back
anti-rollback rejected
signature rejected
```

“OTA 100%” is not enough.

## Secure OTA is layered[#](#secure-ota-is-layered)

HTTPS, Secure Boot, Flash Encryption, signed images, A/B rollback, anti-rollback, health confirmation, and key rotation solve different threats and failure modes.

The robust design is the chain between them.

## Sources and further reading[#](#sources-and-further-reading)

- [ESP-IDF OTA and rollback documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/ota.html)
- [ESP-IDF Flash Encryption](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/security/flash-encryption.html)
- [ESP-IDF ESP32-C6 OTA anti-rollback](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c6/api-reference/system/ota.html)
