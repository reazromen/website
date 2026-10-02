---
title: Rollback Safety Ends at Persistent Schema Compatibility
url: /posts/ota-state-nvs-schema-defines-rollback-boundary.html
date: '2026-09-15'
read_time: 8
excerpt: A previous binary is not a valid rollback target if the new firmware transformed
  NVS into a format the old firmware cannot read.
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
- url: /posts/ota-state-nvs-schema-defines-rollback-boundary.html
  template: cms/templates/posts/posts--ota-state-nvs-schema-defines-rollback-boundary.tpl
  source: cms/templates/posts/posts--ota-state-nvs-schema-defines-rollback-boundary.json
---

# Rollback Safety Ends at Persistent Schema Compatibility

The dangerous shortcut here was to collapse distributed state into one field. The actual problem was that A previous binary is not a valid rollback target if the new firmware transformed NVS into a format the old firmware cannot read.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The migration policy requires APP\_ONLY rollback compatibility and allows CONFIG\_SCHEMA OTA only when old and new firmware can safely read the relevant persistent state; otherwise service mode is required.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **Schema compatibility became release metadata and a promotion gate.**

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

I wrote the state before the transition and the state after it. The issue was A previous binary is not a valid rollback target if the new firmware transformed NVS into a format the old firmware cannot read. The control-plane evidence was The migration policy requires APP\_ONLY rollback compatibility and allows CONFIG\_SCHEMA OTA only when old and new firmware can safely read the relevant persistent state; otherwise service mode is required. Because Code rollback and data rollback are separate problems., I rejected Assuming A/B application slots guarantee rollback regardless of NVS migration. as sufficient. The operational result was Schema compatibility became release metadata and a promotion gate.

The practical rule was: **A rollback plan must include persistent state, not only executable bytes.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
assignment gate ---- model/hw/partition/bootloader/schema/security
artifact gate   ---- SHA-256 + approved ECDSA signature
migration gate  ---- rollback-compatible OR explicit service mode
only then can normal A/B OTA proceed.
```

I used one question to keep the model honest: **Which field is intent and which field is observation?**

For this case, the answer starts with the observed problem: A previous binary is not a valid rollback target if the new firmware transformed NVS into a format the old firmware cannot read. The control plane already had evidence that The migration policy requires APP\_ONLY rollback compatibility and allows CONFIG\_SCHEMA OTA only when old and new firmware can safely read the relevant persistent state; otherwise service mode is required. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Code rollback and data rollback are separate problems.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Assuming A/B application slots guarantee rollback regardless of NVS migration. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—Schema compatibility became release metadata and a promotion gate.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

Compatibility belongs in structured metadata rather than release notes. Device heartbeat reports partition generation, bootloader generation, schema version, security version and rollback capability; release metadata states the compatible window. The server rejects a mismatch at assignment and checks again at artifact request. Signature verification is independent: an image can be compatible but untrusted, or trusted but incompatible.

The API boundary should reject impossible transitions before the device sees them. In this case, the key observation is **The migration policy requires APP\_ONLY rollback compatibility and allows CONFIG\_SCHEMA OTA only when old and new firmware can safely read the relevant persistent state; otherwise service mode is required.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Assuming A/B application slots guarantee rollback regardless of NVS migration.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Code rollback and data rollback are separate problems. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The invariants I wanted before the transition

- model/MCU/hardware match
- partition and bootloader generations match
- schema/security compatibility holds
- hash and detached signature verify
- signing authority is outside delivery host

For **Rollback Safety Ends at Persistent Schema Compatibility**, the key mechanism is that Code rollback and data rollback are separate problems. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **Schema compatibility became release metadata and a promotion gate.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Code rollback and data rollback are separate problems.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## The rule I kept

**A rollback plan must include persistent state, not only executable bytes.**

The result from this case was Schema compatibility became release metadata and a promotion gate.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
