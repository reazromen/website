---
title: Desired Release and Running Release Are Different Truths
url: /posts/ota-state-desired-vs-running-release.html
date: '2026-09-15'
read_time: 7
excerpt: The server needed to know what a device should run without pretending the
  device had already installed it.
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
- url: /posts/ota-state-desired-vs-running-release.html
  template: cms/templates/posts/posts--ota-state-desired-vs-running-release.tpl
  source: cms/templates/posts/posts--ota-state-desired-vs-running-release.json
---

# Desired Release and Running Release Are Different Truths

The useful question was not 'did the device download it?' but whether the state transition was valid. Here, The server needed to know what a device should run without pretending the device had already installed it.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The fleet tracks desired release assignment separately from running\_release\_id reported by heartbeat.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **The UI and API could show pending convergence instead of fictional success.**

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

I wrote the state before the transition and the state after it. The issue was The server needed to know what a device should run without pretending the device had already installed it. The control-plane evidence was The fleet tracks desired release assignment separately from running\_release\_id reported by heartbeat. Because Desired state is operator intent; running state is device observation. Convergence between them is the update process., I rejected Updating the database current version at assignment time. as sufficient. The operational result was The UI and API could show pending convergence instead of fictional success.

The practical rule was: **Never overwrite observed state with desired state.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
release object: DRAFT -> REGISTERED -> TESTED -> CANARY -> ROLLING_OUT -> STABLE
                                      |
operator assignment -----------------+--> desired_release_id
                                               !=
device heartbeat --------------------------> running_release_id
```

I used one question to keep the model honest: **Which field is intent and which field is observation?**

For this case, the answer starts with the observed problem: The server needed to know what a device should run without pretending the device had already installed it. The control plane already had evidence that The fleet tracks desired release assignment separately from running\_release\_id reported by heartbeat. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Desired state is operator intent; running state is device observation. Convergence between them is the update process.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Updating the database current version at assignment time. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—The UI and API could show pending convergence instead of fictional success.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The control plane needs separate columns and API semantics for release identity, desired assignment and observed running release. Assignment should not mutate the running fields. Heartbeat should not mutate release policy. Promotion should not depend on a version comparison alone. The admin UI can derive “pending” from desired\_release\_id != running\_release\_id while the assignment is non-terminal, which makes convergence visible without pretending it already happened.

The API boundary should reject impossible transitions before the device sees them. In this case, the key observation is **The fleet tracks desired release assignment separately from running\_release\_id reported by heartbeat.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Updating the database current version at assignment time.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## The invariants I wanted before the transition

- release object is immutable
- desired assignment is explicit
- running\_release\_id comes from the device
- release state is eligible for serving
- terminal assignment state is not overwritten casually

For **Desired Release and Running Release Are Different Truths**, the key mechanism is that Desired state is operator intent; running state is device observation. Convergence between them is the update process. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **The UI and API could show pending convergence instead of fictional success.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Desired state is operator intent; running state is device observation. Convergence between them is the update process.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Desired state is operator intent; running state is device observation. Convergence between them is the update process. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The rule I kept

**Never overwrite observed state with desired state.**

The result from this case was The UI and API could show pending convergence instead of fictional success.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
