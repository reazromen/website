---
title: A Wi-Fi MAC Address Is Not a Device Credential
url: /posts/ota-state-mac-address-not-device-credential.html
date: '2026-09-15'
read_time: 8
excerpt: A board needed a stable fleet identity without turning a public hardware
  identifier into an authentication secret.
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
- url: /posts/ota-state-mac-address-not-device-credential.html
  template: cms/templates/posts/posts--ota-state-mac-address-not-device-credential.tpl
  source: cms/templates/posts/posts--ota-state-mac-address-not-device-credential.json
---

# A Wi-Fi MAC Address Is Not a Device Credential

The OTA bug was not in the downloader. The real problem was that A board needed a stable fleet identity without turning a public hardware identifier into an authentication secret.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The production design stores an internal device ID, serial/hardware metadata and a unique per-device credential; a fleet-wide shared secret and MAC-as-credential model were explicitly rejected.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **The fleet model separated manufacturing identity from a revocable per-device API credential.**

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

I treated this as a causality problem. The symptom was A board needed a stable fleet identity without turning a public hardware identifier into an authentication secret. The strongest evidence was The production design stores an internal device ID, serial/hardware metadata and a unique per-device credential; a fleet-wide shared secret and MAC-as-credential model were explicitly rejected. The underlying mechanism was Identity answers “which device is this?” while authentication answers “can this caller prove it is that device?” Those are different security properties. That made the tempting shortcut—Using the Wi-Fi MAC address as both lookup key and bearer credential because every board already has one.—unsafe. The retained result was The fleet model separated manufacturing identity from a revocable per-device API credential.

The practical rule was: **A hardware identifier can name a device; it should not automatically authorize one.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
factory_registered --consume bootstrap--> enrolled
      |                                  |
      |                                  +--> unique runtime credential
      |                                         |
      +-----------------------------------------+--> active / blocked / revoked
heartbeat observes runtime; it does not create trust.
```

I used one question to keep the model honest: **What would the database say if the device never came back?**

For this case, the answer starts with the observed problem: A board needed a stable fleet identity without turning a public hardware identifier into an authentication secret. The control plane already had evidence that The production design stores an internal device ID, serial/hardware metadata and a unique per-device credential; a fleet-wide shared secret and MAC-as-credential model were explicitly rejected. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Identity answers “which device is this?” while authentication answers “can this caller prove it is that device?” Those are different security properties.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Using the Wi-Fi MAC address as both lookup key and bearer credential because every board already has one. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—The fleet model separated manufacturing identity from a revocable per-device API credential.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The implementation boundary starts before the OTA code. Device inventory must retain hardware identity even when credentials rotate. Enrollment consumes bootstrap authority and returns a runtime credential once; the database stores a verifier/hash rather than the reusable plaintext. Heartbeat endpoints then authenticate that runtime credential before accepting observations. If an operator blocks a device, the policy decision should be visible separately from credential revocation so recovery does not require inventing a new identity.

The database model is part of the safety mechanism, not just storage. In this case, the key observation is **The production design stores an internal device ID, serial/hardware metadata and a unique per-device credential; a fleet-wide shared secret and MAC-as-credential model were explicitly rejected.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Using the Wi-Fi MAC address as both lookup key and bearer credential because every board already has one.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## The invariants I wanted before the transition

- factory identity exists before enrollment
- bootstrap secret is single-use
- runtime token is unique per device
- credential state is independent from online status
- blocked/revoked transitions are auditable

For **A Wi-Fi MAC Address Is Not a Device Credential**, the key mechanism is that Identity answers “which device is this?” while authentication answers “can this caller prove it is that device?” Those are different security properties. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **The fleet model separated manufacturing identity from a revocable per-device API credential.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Identity answers “which device is this?” while authentication answers “can this caller prove it is that device?” Those are different security properties.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Identity answers “which device is this?” while authentication answers “can this caller prove it is that device?” Those are different security properties. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The rule I kept

**A hardware identifier can name a device; it should not automatically authorize one.**

The result from this case was The fleet model separated manufacturing identity from a revocable per-device API credential.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
