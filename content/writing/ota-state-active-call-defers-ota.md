---
title: An Active SIP Call Has Priority over OTA
url: /posts/ota-state-active-call-defers-ota.html
date: '2026-09-15'
read_time: 8
excerpt: A firmware update competing with a live voice call could damage the product
  function the OTA system exists to maintain.
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
- url: /posts/ota-state-active-call-defers-ota.html
  template: cms/templates/posts/posts--ota-state-active-call-defers-ota.tpl
  source: cms/templates/posts/posts--ota-state-active-call-defers-ota.json
---

# An Active SIP Call Has Priority over OTA

A firmware image can be perfectly valid and still be the wrong update. This case started because A firmware update competing with a live voice call could damage the product function the OTA system exists to maintain.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The firmware contract requires no OTA installation during an active SIP call and lower-priority provisioning/OTA work with bounded network operations.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **The update agent defers while the user-facing call path is busy.**

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

The first design looked simpler because it removed a state. That simplicity was false. The problem was A firmware update competing with a live voice call could damage the product function the OTA system exists to maintain. The system already knew The firmware contract requires no OTA installation during an active SIP call and lower-priority provisioning/OTA work with bounded network operations. Once I modeled Realtime media has tighter latency and availability requirements than management-plane update work., the shortcut Treating OTA as background work that is harmless whenever CPU appears available. stopped being acceptable. The retained result was The update agent defers while the user-facing call path is busy.

The practical rule was: **Maintenance work should yield to the real-time product path.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

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

I used one question to keep the model honest: **What stale value could make this look successful when it is not?**

For this case, the answer starts with the observed problem: A firmware update competing with a live voice call could damage the product function the OTA system exists to maintain. The control plane already had evidence that The firmware contract requires no OTA installation during an active SIP call and lower-priority provisioning/OTA work with bounded network operations. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Realtime media has tighter latency and availability requirements than management-plane update work.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Treating OTA as background work that is harmless whenever CPU appears available. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—The update agent defers while the user-facing call path is busy.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The device updater should behave like a small transactional engine. It verifies preconditions, streams into the inactive slot, validates artifact metadata, changes boot selection only after the write is complete, reboots into pending verification and reaches a local commit point with esp\_ota\_mark\_app\_valid\_cancel\_rollback(). Until that call, resets and validation failures must preserve a path back to the previous image.

Recovery paths deserve the same explicit state names as the happy path. In this case, the key observation is **The firmware contract requires no OTA installation during an active SIP call and lower-priority provisioning/OTA work with bounded network operations.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Treating OTA as background work that is harmless whenever CPU appears available.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **The update agent defers while the user-facing call path is busy.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Realtime media has tighter latency and availability requirements than management-plane update work.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Realtime media has tighter latency and availability requirements than management-plane update work. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The invariants I wanted before the transition

- candidate writes inactive slot
- boot target changes only after verified write
- pending image self-tests locally
- accept/rollback API is called explicitly
- active call and low battery can defer work

For **An Active SIP Call Has Priority over OTA**, the key mechanism is that Realtime media has tighter latency and availability requirements than management-plane update work. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## The rule I kept

**Maintenance work should yield to the real-time product path.**

The result from this case was The update agent defers while the user-facing call path is busy.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
