---
title: SHA-256 Proves Integrity; ECDSA Adds Authorship
url: /posts/ota-state-sha256-and-ecdsa-different-trust.html
date: '2024-04-10'
read_time: 8
excerpt: A correct hash could prove that downloaded bytes matched the manifest but
  not that an authorized release process created that manifest and artifact.
topic: production-ota-fleet
tags:
- ota
- esp32-s3
- fleet-management
- release-engineering
draft: false
featured: false
language: en
eyebrow: 'Production OTA: Compatibility & Trust · deep-dive'
outputs:
- url: /posts/ota-state-sha256-and-ecdsa-different-trust.html
  template: cms/templates/posts/posts--ota-state-sha256-and-ecdsa-different-trust.tpl
  source: cms/templates/posts/posts--ota-state-sha256-and-ecdsa-different-trust.json
---

# SHA-256 Proves Integrity; ECDSA Adds Authorship

The dangerous shortcut here was to collapse distributed state into one field. The actual problem was that A correct hash could prove that downloaded bytes matched the manifest but not that an authorized release process created that manifest and artifact.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **Production policy uses detached ECDSA P-256/SHA-256 signatures; the server verifies the signature at registration and the device independently checks hash and signature before activation.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **Integrity and release authorship became separate validation gates.**

## The state I was actually debugging

```
operator -> release state -> device assignment (desired)
                           |
                           v
device heartbeat ----> running_release_id (observed)
       |                   |
       |                   v
       +---- desired manifest if eligible/compatible
                           |
                      inactive OTA slot
                           |
                      reboot pending verify
                           |
                 local self-test -> accept / rollback
                           |
                  release-scoped event + heartbeat
```

Compatibility and trust decide whether a technically downloadable image is safe and authorized to run. Partition generation, bootloader generation, persistent schema, security epoch, hash and signature are independent gates.

This case became a distributed-systems boundary test. Device observation, server intent and release policy did not mean the same thing. The failure was A correct hash could prove that downloaded bytes matched the manifest but not that an authorized release process created that manifest and artifact. Evidence showed Production policy uses detached ECDSA P-256/SHA-256 signatures; the server verifies the signature at registration and the device independently checks hash and signature before activation. The mechanism was A digest detects alteration relative to an expected value; a signature binds that digest to possession of an approved private key. and the useful conclusion was Integrity and release authorship became separate validation gates.

The practical rule was: **Checksums answer “same bytes”; signatures answer “authorized signer.”** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
assignment gate ---- model/hw/partition/bootloader/schema/security
artifact gate   ---- SHA-256 + approved ECDSA signature
migration gate  ---- rollback-compatible OR explicit service mode
only then can normal A/B OTA proceed.
```

I used one question to keep the model honest: **What event would prove the transition rather than merely suggest it?**

For this case, the answer starts with the observed problem: A correct hash could prove that downloaded bytes matched the manifest but not that an authorized release process created that manifest and artifact. The control plane already had evidence that Production policy uses detached ECDSA P-256/SHA-256 signatures; the server verifies the signature at registration and the device independently checks hash and signature before activation. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is A digest detects alteration relative to an expected value; a signature binds that digest to possession of an approved private key.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Calling a SHA-256 match a firmware authenticity check. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—Integrity and release authorship became separate validation gates.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

Compatibility belongs in structured metadata rather than release notes. Device heartbeat reports partition generation, bootloader generation, schema version, security version and rollback capability; release metadata states the compatible window. The server rejects a mismatch at assignment and checks again at artifact request. Signature verification is independent: an image can be compatible but untrusted, or trusted but incompatible.

The device should report facts it can observe and avoid guessing operator intent. In this case, the key observation is **Production policy uses detached ECDSA P-256/SHA-256 signatures; the server verifies the signature at registration and the device independently checks hash and signature before activation.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Calling a SHA-256 match a firmware authenticity check.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## Incident contract

| Question | Recorded answer |
| --- | --- |
| Problem | A correct hash could prove that downloaded bytes matched the manifest but not that an authorized release process created that manifest and artifact. |
| Evidence | Production policy uses detached ECDSA P-256/SHA-256 signatures; the server verifies the signature at registration and the device independently checks hash and signature before activation. |
| Mechanism | A digest detects alteration relative to an expected value; a signature binds that digest to possession of an approved private key. |
| Rejected shortcut | Calling a SHA-256 match a firmware authenticity check. |
| Result | Integrity and release authorship became separate validation gates. |
| Rule | Checksums answer “same bytes”; signatures answer “authorized signer.” |

I keep this matrix because OTA incidents are easy to rewrite after recovery. Once a device comes back, an old heartbeat string, an assignment row and a release state can all look consistent even when they referred to different transitions. Recording causal identity while the incident is active prevents that retrospective simplification.

## The failure test I would run

I would deliberately **introduce non-backward-compatible schema**.

The expected outcome is not merely “the request fails.” I want the resulting state to remain explainable. The device row, assignment state, release state and append-only event history should agree on what happened and which release the event belonged to. If recovery occurs, it should happen through a defined transition rather than an administrator manually editing the database until the dashboard turns green.

This case is particularly useful because the rejected shortcut was **Calling a SHA-256 match a firmware authenticity check.**. The failure test forces that shortcut to reveal its ambiguity. A good state model should make the unsafe interpretation impossible or at least operationally visible.

## Operational consequence

The retained engineering rule is **Checksums answer “same bytes”; signatures answer “authorized signer.”**. I want that rule enforced in code or policy wherever possible, not left as a runbook sentence that an operator must remember under pressure.

That means state transitions should reject incompatible releases, release promotion should have explicit blockers, heartbeat processing should be conservative about terminal states, and artifact serving should repeat compatibility checks. The event log should preserve who or what caused each important transition. Recovery should be a first-class path rather than an exceptional database repair.

For this article, the operational result was Integrity and release authorship became separate validation gates. That makes the system easier to reason about because each dashboard badge corresponds to a bounded claim rather than an optimistic summary.

## The rule I kept

**Checksums answer “same bytes”; signatures answer “authorized signer.”**

The result from this case was Integrity and release authorship became separate validation gates.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
