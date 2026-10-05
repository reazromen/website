---
title: Power Loss Has Multiple OTA Failure Windows
url: /posts/ota-state-power-loss-ota-failure-windows.html
date: '2023-07-15'
read_time: 8
excerpt: Power can disappear during download, inactive-slot write, after boot-partition
  selection or during first boot.
topic: production-ota-fleet
tags:
- ota
- esp32-s3
- fleet-management
- release-engineering
draft: false
featured: false
language: en
eyebrow: 'Production OTA: Install, Validation & Rollback · deep-dive'
outputs:
- url: /posts/ota-state-power-loss-ota-failure-windows.html
  template: cms/templates/posts/posts--ota-state-power-loss-ota-failure-windows.tpl
  source: cms/templates/posts/posts--ota-state-power-loss-ota-failure-windows.json
---

# Power Loss Has Multiple OTA Failure Windows

A firmware image can be perfectly valid and still be the wrong update. This case started because Power can disappear during download, inactive-slot write, after boot-partition selection or during first boot.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The required failure tests explicitly include power cuts while writing the inactive slot and immediately after selecting the new boot partition, plus crashes before validation.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **Power interruption became an explicit acceptance matrix.**

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

The device-side updater is a transaction across flash and reboot. Download, inactive-slot write, boot selection, pending verification and final acceptance are separate commit points with different power-loss behavior.

I approached this as a transaction with an explicit commit point. The problem was Power can disappear during download, inactive-slot write, after boot-partition selection or during first boot. The evidence was The required failure tests explicitly include power cuts while writing the inactive slot and immediately after selecting the new boot partition, plus crashes before validation. The reason that evidence mattered is Different interruption points exercise different durability guarantees in flash, otadata and rollback state. I deliberately avoided Running one happy-path update and assuming power-loss safety follows automatically from A/B partitions.. The accepted outcome was Power interruption became an explicit acceptance matrix.

The practical rule was: **Test the update at the boundaries where persistent state changes.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
running slot A
   -> download/write slot B
   -> select B
   -> reboot: PENDING_VERIFY
   -> local diagnostics
      -> ACCEPT => B becomes known-good
      -> REJECT/crash => bootloader returns to A
```

I used one question to keep the model honest: **Which component is allowed to commit this state?**

For this case, the answer starts with the observed problem: Power can disappear during download, inactive-slot write, after boot-partition selection or during first boot. The control plane already had evidence that The required failure tests explicitly include power cuts while writing the inactive slot and immediately after selecting the new boot partition, plus crashes before validation. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Different interruption points exercise different durability guarantees in flash, otadata and rollback state.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Running one happy-path update and assuming power-loss safety follows automatically from A/B partitions. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—Power interruption became an explicit acceptance matrix.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The device updater should behave like a small transactional engine. It verifies preconditions, streams into the inactive slot, validates artifact metadata, changes boot selection only after the write is complete, reboots into pending verification and reaches a local commit point with esp\_ota\_mark\_app\_valid\_cancel\_rollback(). Until that call, resets and validation failures must preserve a path back to the previous image.

The control plane should remain conservative when evidence is missing or stale. In this case, the key observation is **The required failure tests explicitly include power cuts while writing the inactive slot and immediately after selecting the new boot partition, plus crashes before validation.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Running one happy-path update and assuming power-loss safety follows automatically from A/B partitions.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## The failure test I would run

I would deliberately **fail a local self-test deliberately**.

The expected outcome is not merely “the request fails.” I want the resulting state to remain explainable. The device row, assignment state, release state and append-only event history should agree on what happened and which release the event belonged to. If recovery occurs, it should happen through a defined transition rather than an administrator manually editing the database until the dashboard turns green.

This case is particularly useful because the rejected shortcut was **Running one happy-path update and assuming power-loss safety follows automatically from A/B partitions.**. The failure test forces that shortcut to reveal its ambiguity. A good state model should make the unsafe interpretation impossible or at least operationally visible.

## Operational consequence

The retained engineering rule is **Test the update at the boundaries where persistent state changes.**. I want that rule enforced in code or policy wherever possible, not left as a runbook sentence that an operator must remember under pressure.

That means state transitions should reject incompatible releases, release promotion should have explicit blockers, heartbeat processing should be conservative about terminal states, and artifact serving should repeat compatibility checks. The event log should preserve who or what caused each important transition. Recovery should be a first-class path rather than an exceptional database repair.

For this article, the operational result was Power interruption became an explicit acceptance matrix. That makes the system easier to reason about because each dashboard badge corresponds to a bounded claim rather than an optimistic summary.

## Incident contract

| Question | Recorded answer |
| --- | --- |
| Problem | Power can disappear during download, inactive-slot write, after boot-partition selection or during first boot. |
| Evidence | The required failure tests explicitly include power cuts while writing the inactive slot and immediately after selecting the new boot partition, plus crashes before validation. |
| Mechanism | Different interruption points exercise different durability guarantees in flash, otadata and rollback state. |
| Rejected shortcut | Running one happy-path update and assuming power-loss safety follows automatically from A/B partitions. |
| Result | Power interruption became an explicit acceptance matrix. |
| Rule | Test the update at the boundaries where persistent state changes. |

I keep this matrix because OTA incidents are easy to rewrite after recovery. Once a device comes back, an old heartbeat string, an assignment row and a release state can all look consistent even when they referred to different transitions. Recording causal identity while the incident is active prevents that retrospective simplification.

## The rule I kept

**Test the update at the boundaries where persistent state changes.**

The result from this case was Power interruption became an explicit acceptance matrix.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
