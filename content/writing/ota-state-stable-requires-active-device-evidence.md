---
title: STABLE Requires Evidence from ACTIVE Devices
url: /posts/ota-state-stable-requires-active-device-evidence.html
date: '2026-09-15'
read_time: 7
excerpt: A release could look administratively complete before any device proved it
  was actually running.
topic: production-ota-fleet
tags:
- ota
- esp32-s3
- fleet-management
- release-engineering
draft: false
featured: false
language: en
eyebrow: 'Production OTA: Release & Assignment State · deep-dive'
outputs:
- url: /posts/ota-state-stable-requires-active-device-evidence.html
  template: cms/templates/posts/posts--ota-state-stable-requires-active-device-evidence.tpl
  source: cms/templates/posts/posts--ota-state-stable-requires-active-device-evidence.json
---

# STABLE Requires Evidence from ACTIVE Devices

The OTA bug was not in the downloader. The real problem was that A release could look administratively complete before any device proved it was actually running.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The live control plane blocks STABLE unless at least one assignment is ACTIVE and blocks promotion when failed or rolled-back assignments exist.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **STABLE became dependent on runtime fleet evidence.**

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

The control plane carries at least three truths at once: immutable release identity, operator desired assignment and device-reported running identity. OTA is the convergence process between them.

The first design looked simpler because it removed a state. That simplicity was false. The problem was A release could look administratively complete before any device proved it was actually running. The system already knew The live control plane blocks STABLE unless at least one assignment is ACTIVE and blocks promotion when failed or rolled-back assignments exist. Once I modeled Release stability depends on device-observed acceptance, not only server-side registration., the shortcut Marking a release stable immediately after upload or signature verification. stopped being acceptable. The retained result was STABLE became dependent on runtime fleet evidence.

The practical rule was: **A rollout state should be earned by the devices, not declared by the file server.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
release object: DRAFT -> REGISTERED -> TESTED -> CANARY -> ROLLING_OUT -> STABLE
                                      |
operator assignment -----------------+--> desired_release_id
                                               !=
device heartbeat --------------------------> running_release_id
```

I used one question to keep the model honest: **What stale value could make this look successful when it is not?**

For this case, the answer starts with the observed problem: A release could look administratively complete before any device proved it was actually running. The control plane already had evidence that The live control plane blocks STABLE unless at least one assignment is ACTIVE and blocks promotion when failed or rolled-back assignments exist. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Release stability depends on device-observed acceptance, not only server-side registration.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Marking a release stable immediately after upload or signature verification. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—STABLE became dependent on runtime fleet evidence.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The control plane needs separate columns and API semantics for release identity, desired assignment and observed running release. Assignment should not mutate the running fields. Heartbeat should not mutate release policy. Promotion should not depend on a version comparison alone. The admin UI can derive “pending” from desired\_release\_id != running\_release\_id while the assignment is non-terminal, which makes convergence visible without pretending it already happened.

Recovery paths deserve the same explicit state names as the happy path. In this case, the key observation is **The live control plane blocks STABLE unless at least one assignment is ACTIVE and blocks promotion when failed or rolled-back assignments exist.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Marking a release stable immediately after upload or signature verification.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## Operational consequence

The retained engineering rule is **A rollout state should be earned by the devices, not declared by the file server.**. I want that rule enforced in code or policy wherever possible, not left as a runbook sentence that an operator must remember under pressure.

That means state transitions should reject incompatible releases, release promotion should have explicit blockers, heartbeat processing should be conservative about terminal states, and artifact serving should repeat compatibility checks. The event log should preserve who or what caused each important transition. Recovery should be a first-class path rather than an exceptional database repair.

For this article, the operational result was STABLE became dependent on runtime fleet evidence. That makes the system easier to reason about because each dashboard badge corresponds to a bounded claim rather than an optimistic summary.

## Incident contract

| Question | Recorded answer |
| --- | --- |
| Problem | A release could look administratively complete before any device proved it was actually running. |
| Evidence | The live control plane blocks STABLE unless at least one assignment is ACTIVE and blocks promotion when failed or rolled-back assignments exist. |
| Mechanism | Release stability depends on device-observed acceptance, not only server-side registration. |
| Rejected shortcut | Marking a release stable immediately after upload or signature verification. |
| Result | STABLE became dependent on runtime fleet evidence. |
| Rule | A rollout state should be earned by the devices, not declared by the file server. |

I keep this matrix because OTA incidents are easy to rewrite after recovery. Once a device comes back, an old heartbeat string, an assignment row and a release state can all look consistent even when they referred to different transitions. Recording causal identity while the incident is active prevents that retrospective simplification.

## The failure test I would run

I would deliberately **pause a release while assignments still exist**.

The expected outcome is not merely “the request fails.” I want the resulting state to remain explainable. The device row, assignment state, release state and append-only event history should agree on what happened and which release the event belonged to. If recovery occurs, it should happen through a defined transition rather than an administrator manually editing the database until the dashboard turns green.

This case is particularly useful because the rejected shortcut was **Marking a release stable immediately after upload or signature verification.**. The failure test forces that shortcut to reveal its ambiguity. A good state model should make the unsafe interpretation impossible or at least operationally visible.

## The rule I kept

**A rollout state should be earned by the devices, not declared by the file server.**

The result from this case was STABLE became dependent on runtime fleet evidence.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
