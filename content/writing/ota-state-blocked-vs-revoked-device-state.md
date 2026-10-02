---
title: Blocked and Revoked Are Different Fleet States
url: /posts/ota-state-blocked-vs-revoked-device-state.html
date: '2026-09-15'
read_time: 8
excerpt: Operators needed to stop a device temporarily without confusing that action
  with permanent credential invalidation.
topic: production-ota-fleet
tags:
- ota
- esp32-s3
- fleet-management
- release-engineering
draft: false
featured: false
language: en
eyebrow: 'Production OTA: Identity & Enrollment · deep-dive'
outputs:
- url: /posts/ota-state-blocked-vs-revoked-device-state.html
  template: cms/templates/posts/posts--ota-state-blocked-vs-revoked-device-state.tpl
  source: cms/templates/posts/posts--ota-state-blocked-vs-revoked-device-state.json
---

# Blocked and Revoked Are Different Fleet States

The useful question was not 'did the device download it?' but whether the state transition was valid. Here, Operators needed to stop a device temporarily without confusing that action with permanent credential invalidation.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The fleet model distinguishes lifecycle states including active, blocked and revoked, while credentials can also be rotated or revoked server-side.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **The control plane preserved separate device lifecycle and credential semantics.**

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

Device identity is the first state machine. Factory registration, one-time enrollment, runtime credential state, blocked/revoked policy and observed health should not collapse into one boolean called online.

This case became a distributed-systems boundary test. Device observation, server intent and release policy did not mean the same thing. The failure was Operators needed to stop a device temporarily without confusing that action with permanent credential invalidation. Evidence showed The fleet model distinguishes lifecycle states including active, blocked and revoked, while credentials can also be rotated or revoked server-side. The mechanism was Operational suspension and credential invalidation answer different questions: one controls service policy, the other controls authentication trust. and the useful conclusion was The control plane preserved separate device lifecycle and credential semantics.

The practical rule was: **State names should explain what recovery action is possible.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
factory_registered --consume bootstrap--> enrolled
      |                                  |
      |                                  +--> unique runtime credential
      |                                         |
      +-----------------------------------------+--> active / blocked / revoked
heartbeat observes runtime; it does not create trust.
```

I used one question to keep the model honest: **What event would prove the transition rather than merely suggest it?**

For this case, the answer starts with the observed problem: Operators needed to stop a device temporarily without confusing that action with permanent credential invalidation. The control plane already had evidence that The fleet model distinguishes lifecycle states including active, blocked and revoked, while credentials can also be rotated or revoked server-side. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Operational suspension and credential invalidation answer different questions: one controls service policy, the other controls authentication trust.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Using one boolean such as disabled for every device problem. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—The control plane preserved separate device lifecycle and credential semantics.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The implementation boundary starts before the OTA code. Device inventory must retain hardware identity even when credentials rotate. Enrollment consumes bootstrap authority and returns a runtime credential once; the database stores a verifier/hash rather than the reusable plaintext. Heartbeat endpoints then authenticate that runtime credential before accepting observations. If an operator blocks a device, the policy decision should be visible separately from credential revocation so recovery does not require inventing a new identity.

The device should report facts it can observe and avoid guessing operator intent. In this case, the key observation is **The fleet model distinguishes lifecycle states including active, blocked and revoked, while credentials can also be rotated or revoked server-side.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Using one boolean such as disabled for every device problem.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **The control plane preserved separate device lifecycle and credential semantics.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Operational suspension and credential invalidation answer different questions: one controls service policy, the other controls authentication trust.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Operational suspension and credential invalidation answer different questions: one controls service policy, the other controls authentication trust. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The invariants I wanted before the transition

- factory identity exists before enrollment
- bootstrap secret is single-use
- runtime token is unique per device
- credential state is independent from online status
- blocked/revoked transitions are auditable

For **Blocked and Revoked Are Different Fleet States**, the key mechanism is that Operational suspension and credential invalidation answer different questions: one controls service policy, the other controls authentication trust. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## The rule I kept

**State names should explain what recovery action is possible.**

The result from this case was The control plane preserved separate device lifecycle and credential semantics.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
