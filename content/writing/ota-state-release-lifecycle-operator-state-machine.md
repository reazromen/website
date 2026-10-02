---
title: Release Lifecycle Is an Operator State Machine
url: /posts/ota-state-release-lifecycle-operator-state-machine.html
date: '2026-09-15'
read_time: 7
excerpt: A release needed gates between registration and fleet-wide use rather than
  one published flag.
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
- url: /posts/ota-state-release-lifecycle-operator-state-machine.html
  template: cms/templates/posts/posts--ota-state-release-lifecycle-operator-state-machine.tpl
  source: cms/templates/posts/posts--ota-state-release-lifecycle-operator-state-machine.json
---

# Release Lifecycle Is an Operator State Machine

Production OTA got easier when I stopped treating it as file transfer. In this case, A release needed gates between registration and fleet-wide use rather than one published flag.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The live service implements DRAFT -> REGISTERED -> TESTED -> CANARY -> ROLLING\_OUT -> STABLE with pause/fail/rollback branches.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **Promotion became a controlled transition with blockers.**

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

I approached this as a transaction with an explicit commit point. The problem was A release needed gates between registration and fleet-wide use rather than one published flag. The evidence was The live service implements DRAFT -> REGISTERED -> TESTED -> CANARY -> ROLLING\_OUT -> STABLE with pause/fail/rollback branches. The reason that evidence mattered is Release state encodes accumulated evidence and allowed operations. I deliberately avoided Using a single active=true field for both test artifacts and stable releases.. The accepted outcome was Promotion became a controlled transition with blockers.

The practical rule was: **Promotion should record evidence, not just intent.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
release object: DRAFT -> REGISTERED -> TESTED -> CANARY -> ROLLING_OUT -> STABLE
                                      |
operator assignment -----------------+--> desired_release_id
                                               !=
device heartbeat --------------------------> running_release_id
```

I used one question to keep the model honest: **Which component is allowed to commit this state?**

For this case, the answer starts with the observed problem: A release needed gates between registration and fleet-wide use rather than one published flag. The control plane already had evidence that The live service implements DRAFT -> REGISTERED -> TESTED -> CANARY -> ROLLING\_OUT -> STABLE with pause/fail/rollback branches. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Release state encodes accumulated evidence and allowed operations.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Using a single active=true field for both test artifacts and stable releases. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—Promotion became a controlled transition with blockers.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The control plane needs separate columns and API semantics for release identity, desired assignment and observed running release. Assignment should not mutate the running fields. Heartbeat should not mutate release policy. Promotion should not depend on a version comparison alone. The admin UI can derive “pending” from desired\_release\_id != running\_release\_id while the assignment is non-terminal, which makes convergence visible without pretending it already happened.

The control plane should remain conservative when evidence is missing or stale. In this case, the key observation is **The live service implements DRAFT -> REGISTERED -> TESTED -> CANARY -> ROLLING\_OUT -> STABLE with pause/fail/rollback branches.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Using a single active=true field for both test artifacts and stable releases.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **Promotion became a controlled transition with blockers.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Release state encodes accumulated evidence and allowed operations.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Release state encodes accumulated evidence and allowed operations. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The invariants I wanted before the transition

- release object is immutable
- desired assignment is explicit
- running\_release\_id comes from the device
- release state is eligible for serving
- terminal assignment state is not overwritten casually

For **Release Lifecycle Is an Operator State Machine**, the key mechanism is that Release state encodes accumulated evidence and allowed operations. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## The rule I kept

**Promotion should record evidence, not just intent.**

The result from this case was Promotion became a controlled transition with blockers.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
