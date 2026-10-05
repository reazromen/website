---
title: Failure Injection Is Part of the OTA Definition of Done
url: /posts/ota-state-failure-injection-definition-of-done.html
date: '2025-04-05'
read_time: 8
excerpt: A successful happy-path download could not prove rollback, credential rejection,
  compatibility gates or interrupted writes behaved safely.
topic: production-ota-fleet
tags:
- ota
- esp32-s3
- fleet-management
- release-engineering
draft: false
featured: false
language: en
eyebrow: 'Production OTA: Rollout, Audit & Failure Injection · deep-dive'
outputs:
- url: /posts/ota-state-failure-injection-definition-of-done.html
  template: cms/templates/posts/posts--ota-state-failure-injection-definition-of-done.tpl
  source: cms/templates/posts/posts--ota-state-failure-injection-definition-of-done.json
---

# Failure Injection Is Part of the OTA Definition of Done

The dangerous shortcut here was to collapse distributed state into one field. The actual problem was that A successful happy-path download could not prove rollback, credential rejection, compatibility gates or interrupted writes behaved safely.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **Required production tests include corrupt artifacts, wrong hardware/partition assignments, revoked credentials, power cuts, first-boot crashes, forced self-test failure and rollback after schema migration.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **Failure drills became release-readiness evidence.**

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

Fleet rollout is a feedback system. Events, heartbeat and cohort evidence must feed promotion and rollback decisions; otherwise canary and audit are labels rather than controls.

The first design looked simpler because it removed a state. That simplicity was false. The problem was A successful happy-path download could not prove rollback, credential rejection, compatibility gates or interrupted writes behaved safely. The system already knew Required production tests include corrupt artifacts, wrong hardware/partition assignments, revoked credentials, power cuts, first-boot crashes, forced self-test failure and rollback after schema migration. Once I modeled Safety properties are only exercised when the system is driven through the failure transition they are supposed to handle., the shortcut Considering rollback implemented because the API exists or the code compiles. stopped being acceptable. The retained result was Failure drills became release-readiness evidence.

The practical rule was: **If a safety path matters, deliberately trigger it before production depends on it.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
canary assignment -> release-scoped events -> heartbeat proves running release
        |                    |                         |
        +------ rollback/failure pauses promotion ----+
                             |
                       cohort -> cohort -> STABLE
```

I used one question to keep the model honest: **What stale value could make this look successful when it is not?**

For this case, the answer starts with the observed problem: A successful happy-path download could not prove rollback, credential rejection, compatibility gates or interrupted writes behaved safely. The control plane already had evidence that Required production tests include corrupt artifacts, wrong hardware/partition assignments, revoked credentials, power cuts, first-boot crashes, forced self-test failure and rollback after schema migration. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Safety properties are only exercised when the system is driven through the failure transition they are supposed to handle.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Considering rollback implemented because the API exists or the code compiles. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—Failure drills became release-readiness evidence.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

Rollout logic should consume evidence rather than timers alone. Append-only events record release-scoped transitions, heartbeat confirms the actual running release, assignment status records convergence, and release state controls whether new devices may receive the image. A pause must stop new rollout while preserving evidence from devices already assigned. Rollback is then another explicit transition, not a manual rewrite of history.

Recovery paths deserve the same explicit state names as the happy path. In this case, the key observation is **Required production tests include corrupt artifacts, wrong hardware/partition assignments, revoked credentials, power cuts, first-boot crashes, forced self-test failure and rollback after schema migration.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Considering rollback implemented because the API exists or the code compiles.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## The invariants I wanted before the transition

- canary evidence exists
- append-only events explain transitions
- promotion pauses on rollback/failure
- manual rollback target is still data-compatible
- failure drills exercise safety paths

For **Failure Injection Is Part of the OTA Definition of Done**, the key mechanism is that Safety properties are only exercised when the system is driven through the failure transition they are supposed to handle. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **Failure drills became release-readiness evidence.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Safety properties are only exercised when the system is driven through the failure transition they are supposed to handle.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Safety properties are only exercised when the system is driven through the failure transition they are supposed to handle. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The rule I kept

**If a safety path matters, deliberately trigger it before production depends on it.**

The result from this case was Failure drills became release-readiness evidence.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
