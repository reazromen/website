---
title: Partition, Bootloader and Security Changes Are Not Normal App OTA
url: /posts/ota-state-service-mode-release-classes.html
date: '2026-09-15'
read_time: 8
excerpt: Some changes alter the substrate that makes normal A/B OTA safe and therefore
  cannot be treated like another application image.
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
- url: /posts/ota-state-service-mode-release-classes.html
  template: cms/templates/posts/posts--ota-state-service-mode-release-classes.tpl
  source: cms/templates/posts/posts--ota-state-service-mode-release-classes.json
---

# Partition, Bootloader and Security Changes Are Not Normal App OTA

A firmware image can be perfectly valid and still be the wrong update. This case started because Some changes alter the substrate that makes normal A/B OTA safe and therefore cannot be treated like another application image.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The migration policy classifies PARTITION\_TABLE, BOOTLOADER and SECURITY\_EPOCH as service-mode changes and refuses to serve them through the normal app OTA path.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **Infrastructure-changing releases require an explicit recovery-oriented service procedure.**

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

I treated this as a causality problem. The symptom was Some changes alter the substrate that makes normal A/B OTA safe and therefore cannot be treated like another application image. The strongest evidence was The migration policy classifies PARTITION\_TABLE, BOOTLOADER and SECURITY\_EPOCH as service-mode changes and refuses to serve them through the normal app OTA path. The underlying mechanism was A normal OTA assumes compatible partition metadata, bootloader behavior and security epoch already exist. That made the tempting shortcut—Forcing every flash change through the same remote update endpoint.—unsafe. The retained result was Infrastructure-changing releases require an explicit recovery-oriented service procedure.

The practical rule was: **The updater cannot safely replace every layer beneath itself.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
assignment gate ---- model/hw/partition/bootloader/schema/security
artifact gate   ---- SHA-256 + approved ECDSA signature
migration gate  ---- rollback-compatible OR explicit service mode
only then can normal A/B OTA proceed.
```

I used one question to keep the model honest: **What would the database say if the device never came back?**

For this case, the answer starts with the observed problem: Some changes alter the substrate that makes normal A/B OTA safe and therefore cannot be treated like another application image. The control plane already had evidence that The migration policy classifies PARTITION\_TABLE, BOOTLOADER and SECURITY\_EPOCH as service-mode changes and refuses to serve them through the normal app OTA path. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is A normal OTA assumes compatible partition metadata, bootloader behavior and security epoch already exist.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Forcing every flash change through the same remote update endpoint. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—Infrastructure-changing releases require an explicit recovery-oriented service procedure.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

Compatibility belongs in structured metadata rather than release notes. Device heartbeat reports partition generation, bootloader generation, schema version, security version and rollback capability; release metadata states the compatible window. The server rejects a mismatch at assignment and checks again at artifact request. Signature verification is independent: an image can be compatible but untrusted, or trusted but incompatible.

The database model is part of the safety mechanism, not just storage. In this case, the key observation is **The migration policy classifies PARTITION\_TABLE, BOOTLOADER and SECURITY\_EPOCH as service-mode changes and refuses to serve them through the normal app OTA path.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Forcing every flash change through the same remote update endpoint.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## Operational consequence

The retained engineering rule is **The updater cannot safely replace every layer beneath itself.**. I want that rule enforced in code or policy wherever possible, not left as a runbook sentence that an operator must remember under pressure.

That means state transitions should reject incompatible releases, release promotion should have explicit blockers, heartbeat processing should be conservative about terminal states, and artifact serving should repeat compatibility checks. The event log should preserve who or what caused each important transition. Recovery should be a first-class path rather than an exceptional database repair.

For this article, the operational result was Infrastructure-changing releases require an explicit recovery-oriented service procedure. That makes the system easier to reason about because each dashboard badge corresponds to a bounded claim rather than an optimistic summary.

## Incident contract

| Question | Recorded answer |
| --- | --- |
| Problem | Some changes alter the substrate that makes normal A/B OTA safe and therefore cannot be treated like another application image. |
| Evidence | The migration policy classifies PARTITION\_TABLE, BOOTLOADER and SECURITY\_EPOCH as service-mode changes and refuses to serve them through the normal app OTA path. |
| Mechanism | A normal OTA assumes compatible partition metadata, bootloader behavior and security epoch already exist. |
| Rejected shortcut | Forcing every flash change through the same remote update endpoint. |
| Result | Infrastructure-changing releases require an explicit recovery-oriented service procedure. |
| Rule | The updater cannot safely replace every layer beneath itself. |

I keep this matrix because OTA incidents are easy to rewrite after recovery. Once a device comes back, an old heartbeat string, an assignment row and a release state can all look consistent even when they referred to different transitions. Recording causal identity while the incident is active prevents that retrospective simplification.

## The failure test I would run

I would deliberately **assign wrong hardware revision**.

The expected outcome is not merely “the request fails.” I want the resulting state to remain explainable. The device row, assignment state, release state and append-only event history should agree on what happened and which release the event belonged to. If recovery occurs, it should happen through a defined transition rather than an administrator manually editing the database until the dashboard turns green.

This case is particularly useful because the rejected shortcut was **Forcing every flash change through the same remote update endpoint.**. The failure test forces that shortcut to reveal its ambiguity. A good state model should make the unsafe interpretation impossible or at least operationally visible.

## The rule I kept

**The updater cannot safely replace every layer beneath itself.**

The result from this case was Infrastructure-changing releases require an explicit recovery-oriented service procedure.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
