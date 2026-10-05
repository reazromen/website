---
title: The Backend Can Be Down Without Making the Phone Useless
url: /posts/ota-state-cached-config-survives-backend-outage.html
date: '2020-03-11'
read_time: 8
excerpt: Provisioning and OTA control were new dependencies, but a temporary backend
  outage should not break an already configured voice device.
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
- url: /posts/ota-state-cached-config-survives-backend-outage.html
  template: cms/templates/posts/posts--ota-state-cached-config-survives-backend-outage.tpl
  source: cms/templates/posts/posts--ota-state-cached-config-survives-backend-outage.json
---

# The Backend Can Be Down Without Making the Phone Useless

Production OTA got easier when I stopped treating it as file transfer. In this case, Provisioning and OTA control were new dependencies, but a temporary backend outage should not break an already configured voice device.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The firmware contract explicitly says provisioning-server failure must not make the device unusable when valid cached SIP configuration already exists.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **The device retained valid local configuration and allowed calls while control-plane work retried independently.**

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

The first design looked simpler because it removed a state. That simplicity was false. The problem was Provisioning and OTA control were new dependencies, but a temporary backend outage should not break an already configured voice device. The system already knew The firmware contract explicitly says provisioning-server failure must not make the device unusable when valid cached SIP configuration already exists. Once I modeled Configuration control plane availability and real-time product function have different failure budgets; cached state can decouple them., the shortcut Restarting or clearing working SIP state whenever config sync fails. stopped being acceptable. The retained result was The device retained valid local configuration and allowed calls while control-plane work retried independently.

The practical rule was: **A management plane should fail softer than the product function it manages.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
factory_registered --consume bootstrap--> enrolled
      |                                  |
      |                                  +--> unique runtime credential
      |                                         |
      +-----------------------------------------+--> active / blocked / revoked
heartbeat observes runtime; it does not create trust.
```

I used one question to keep the model honest: **What stale value could make this look successful when it is not?**

For this case, the answer starts with the observed problem: Provisioning and OTA control were new dependencies, but a temporary backend outage should not break an already configured voice device. The control plane already had evidence that The firmware contract explicitly says provisioning-server failure must not make the device unusable when valid cached SIP configuration already exists. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Configuration control plane availability and real-time product function have different failure budgets; cached state can decouple them.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Restarting or clearing working SIP state whenever config sync fails. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—The device retained valid local configuration and allowed calls while control-plane work retried independently.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The implementation boundary starts before the OTA code. Device inventory must retain hardware identity even when credentials rotate. Enrollment consumes bootstrap authority and returns a runtime credential once; the database stores a verifier/hash rather than the reusable plaintext. Heartbeat endpoints then authenticate that runtime credential before accepting observations. If an operator blocks a device, the policy decision should be visible separately from credential revocation so recovery does not require inventing a new identity.

Recovery paths deserve the same explicit state names as the happy path. In this case, the key observation is **The firmware contract explicitly says provisioning-server failure must not make the device unusable when valid cached SIP configuration already exists.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Restarting or clearing working SIP state whenever config sync fails.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Configuration control plane availability and real-time product function have different failure budgets; cached state can decouple them. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The invariants I wanted before the transition

- factory identity exists before enrollment
- bootstrap secret is single-use
- runtime token is unique per device
- credential state is independent from online status
- blocked/revoked transitions are auditable

For **The Backend Can Be Down Without Making the Phone Useless**, the key mechanism is that Configuration control plane availability and real-time product function have different failure budgets; cached state can decouple them. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **The device retained valid local configuration and allowed calls while control-plane work retried independently.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Configuration control plane availability and real-time product function have different failure budgets; cached state can decouple them.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## The rule I kept

**A management plane should fail softer than the product function it manages.**

The result from this case was The device retained valid local configuration and allowed calls while control-plane work retried independently.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
