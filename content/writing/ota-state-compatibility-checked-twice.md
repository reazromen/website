---
title: Compatibility Is Checked at Assignment and Artifact Request
url: /posts/ota-state-compatibility-checked-twice.html
date: '2026-09-15'
read_time: 8
excerpt: A device can change state after assignment, so one compatibility decision
  made earlier may become stale before download.
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
- url: /posts/ota-state-compatibility-checked-twice.html
  template: cms/templates/posts/posts--ota-state-compatibility-checked-twice.tpl
  source: cms/templates/posts/posts--ota-state-compatibility-checked-twice.json
---

# Compatibility Is Checked at Assignment and Artifact Request

The dangerous shortcut here was to collapse distributed state into one field. The actual problem was that A device can change state after assignment, so one compatibility decision made earlier may become stale before download.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The production architecture checks model, MCU, hardware revision, partition/bootloader/schema/security compatibility at assignment and repeats validation when the device requests the artifact.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **Incompatible images are blocked both when intent is created and when bytes are served.**

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

The first design looked simpler because it removed a state. That simplicity was false. The problem was A device can change state after assignment, so one compatibility decision made earlier may become stale before download. The system already knew The production architecture checks model, MCU, hardware revision, partition/bootloader/schema/security compatibility at assignment and repeats validation when the device requests the artifact. Once I modeled Authorization should be re-evaluated at the action boundary using current state., the shortcut Assuming an old assignment permanently authorizes artifact delivery. stopped being acceptable. The retained result was Incompatible images are blocked both when intent is created and when bytes are served.

The practical rule was: **Critical compatibility checks belong at both planning and execution boundaries.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
assignment gate ---- model/hw/partition/bootloader/schema/security
artifact gate   ---- SHA-256 + approved ECDSA signature
migration gate  ---- rollback-compatible OR explicit service mode
only then can normal A/B OTA proceed.
```

I used one question to keep the model honest: **What stale value could make this look successful when it is not?**

For this case, the answer starts with the observed problem: A device can change state after assignment, so one compatibility decision made earlier may become stale before download. The control plane already had evidence that The production architecture checks model, MCU, hardware revision, partition/bootloader/schema/security compatibility at assignment and repeats validation when the device requests the artifact. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Authorization should be re-evaluated at the action boundary using current state.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Assuming an old assignment permanently authorizes artifact delivery. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—Incompatible images are blocked both when intent is created and when bytes are served.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

Compatibility belongs in structured metadata rather than release notes. Device heartbeat reports partition generation, bootloader generation, schema version, security version and rollback capability; release metadata states the compatible window. The server rejects a mismatch at assignment and checks again at artifact request. Signature verification is independent: an image can be compatible but untrusted, or trusted but incompatible.

Recovery paths deserve the same explicit state names as the happy path. In this case, the key observation is **The production architecture checks model, MCU, hardware revision, partition/bootloader/schema/security compatibility at assignment and repeats validation when the device requests the artifact.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Assuming an old assignment permanently authorizes artifact delivery.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## The failure test I would run

I would deliberately **present a valid hash with an unapproved signature identity**.

The expected outcome is not merely “the request fails.” I want the resulting state to remain explainable. The device row, assignment state, release state and append-only event history should agree on what happened and which release the event belonged to. If recovery occurs, it should happen through a defined transition rather than an administrator manually editing the database until the dashboard turns green.

This case is particularly useful because the rejected shortcut was **Assuming an old assignment permanently authorizes artifact delivery.**. The failure test forces that shortcut to reveal its ambiguity. A good state model should make the unsafe interpretation impossible or at least operationally visible.

## Operational consequence

The retained engineering rule is **Critical compatibility checks belong at both planning and execution boundaries.**. I want that rule enforced in code or policy wherever possible, not left as a runbook sentence that an operator must remember under pressure.

That means state transitions should reject incompatible releases, release promotion should have explicit blockers, heartbeat processing should be conservative about terminal states, and artifact serving should repeat compatibility checks. The event log should preserve who or what caused each important transition. Recovery should be a first-class path rather than an exceptional database repair.

For this article, the operational result was Incompatible images are blocked both when intent is created and when bytes are served. That makes the system easier to reason about because each dashboard badge corresponds to a bounded claim rather than an optimistic summary.

## Incident contract

| Question | Recorded answer |
| --- | --- |
| Problem | A device can change state after assignment, so one compatibility decision made earlier may become stale before download. |
| Evidence | The production architecture checks model, MCU, hardware revision, partition/bootloader/schema/security compatibility at assignment and repeats validation when the device requests the artifact. |
| Mechanism | Authorization should be re-evaluated at the action boundary using current state. |
| Rejected shortcut | Assuming an old assignment permanently authorizes artifact delivery. |
| Result | Incompatible images are blocked both when intent is created and when bytes are served. |
| Rule | Critical compatibility checks belong at both planning and execution boundaries. |

I keep this matrix because OTA incidents are easy to rewrite after recovery. Once a device comes back, an old heartbeat string, an assignment row and a release state can all look consistent even when they referred to different transitions. Recording causal identity while the incident is active prevents that retrospective simplification.

## The rule I kept

**Critical compatibility checks belong at both planning and execution boundaries.**

The result from this case was Incompatible images are blocked both when intent is created and when bytes are served.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
