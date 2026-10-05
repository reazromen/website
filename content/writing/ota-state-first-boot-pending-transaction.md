---
title: First Boot Is a Pending Transaction, Not Success
url: /posts/ota-state-first-boot-pending-transaction.html
date: '2024-08-10'
read_time: 7
excerpt: A reboot into the new partition was too weak to count as a successful update.
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
- url: /posts/ota-state-first-boot-pending-transaction.html
  template: cms/templates/posts/posts--ota-state-first-boot-pending-transaction.tpl
  source: cms/templates/posts/posts--ota-state-first-boot-pending-transaction.json
---

# First Boot Is a Pending Transaction, Not Success

The OTA bug was not in the downloader. The real problem was that A reboot into the new partition was too weak to count as a successful update.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The firmware contract detects ESP\_OTA\_IMG\_PENDING\_VERIFY and marks the image valid only after fast local diagnostics pass.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **The update remained pending until the application crossed an acceptance checkpoint.**

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

I wrote the state before the transition and the state after it. The issue was A reboot into the new partition was too weak to count as a successful update. The control-plane evidence was The firmware contract detects ESP\_OTA\_IMG\_PENDING\_VERIFY and marks the image valid only after fast local diagnostics pass. Because The bootloader can preserve rollback authority until application code explicitly commits the candidate., I rejected Reporting success as soon as the new partition starts executing. as sufficient. The operational result was The update remained pending until the application crossed an acceptance checkpoint.

The practical rule was: **Booting is evidence of executability, not acceptance.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

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

I used one question to keep the model honest: **Which field is intent and which field is observation?**

For this case, the answer starts with the observed problem: A reboot into the new partition was too weak to count as a successful update. The control plane already had evidence that The firmware contract detects ESP\_OTA\_IMG\_PENDING\_VERIFY and marks the image valid only after fast local diagnostics pass. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is The bootloader can preserve rollback authority until application code explicitly commits the candidate.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Reporting success as soon as the new partition starts executing. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—The update remained pending until the application crossed an acceptance checkpoint.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The device updater should behave like a small transactional engine. It verifies preconditions, streams into the inactive slot, validates artifact metadata, changes boot selection only after the write is complete, reboots into pending verification and reaches a local commit point with esp\_ota\_mark\_app\_valid\_cancel\_rollback(). Until that call, resets and validation failures must preserve a path back to the previous image.

The API boundary should reject impossible transitions before the device sees them. In this case, the key observation is **The firmware contract detects ESP\_OTA\_IMG\_PENDING\_VERIFY and marks the image valid only after fast local diagnostics pass.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Reporting success as soon as the new partition starts executing.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## Incident contract

| Question | Recorded answer |
| --- | --- |
| Problem | A reboot into the new partition was too weak to count as a successful update. |
| Evidence | The firmware contract detects ESP\_OTA\_IMG\_PENDING\_VERIFY and marks the image valid only after fast local diagnostics pass. |
| Mechanism | The bootloader can preserve rollback authority until application code explicitly commits the candidate. |
| Rejected shortcut | Reporting success as soon as the new partition starts executing. |
| Result | The update remained pending until the application crossed an acceptance checkpoint. |
| Rule | Booting is evidence of executability, not acceptance. |

I keep this matrix because OTA incidents are easy to rewrite after recovery. Once a device comes back, an old heartbeat string, an assignment row and a release state can all look consistent even when they referred to different transitions. Recording causal identity while the incident is active prevents that retrospective simplification.

## The failure test I would run

I would deliberately **cut power after boot target selection**.

The expected outcome is not merely “the request fails.” I want the resulting state to remain explainable. The device row, assignment state, release state and append-only event history should agree on what happened and which release the event belonged to. If recovery occurs, it should happen through a defined transition rather than an administrator manually editing the database until the dashboard turns green.

This case is particularly useful because the rejected shortcut was **Reporting success as soon as the new partition starts executing.**. The failure test forces that shortcut to reveal its ambiguity. A good state model should make the unsafe interpretation impossible or at least operationally visible.

## Operational consequence

The retained engineering rule is **Booting is evidence of executability, not acceptance.**. I want that rule enforced in code or policy wherever possible, not left as a runbook sentence that an operator must remember under pressure.

That means state transitions should reject incompatible releases, release promotion should have explicit blockers, heartbeat processing should be conservative about terminal states, and artifact serving should repeat compatibility checks. The event log should preserve who or what caused each important transition. Recovery should be a first-class path rather than an exceptional database repair.

For this article, the operational result was The update remained pending until the application crossed an acceptance checkpoint. That makes the system easier to reason about because each dashboard badge corresponds to a bounded claim rather than an optimistic summary.

## The rule I kept

**Booting is evidence of executability, not acceptance.**

The result from this case was The update remained pending until the application crossed an acceptance checkpoint.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
