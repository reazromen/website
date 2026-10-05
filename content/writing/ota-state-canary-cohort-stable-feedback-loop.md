---
title: Canary to Cohort to Stable Is a Feedback Loop
url: /posts/ota-state-canary-cohort-stable-feedback-loop.html
date: '2023-10-16'
read_time: 8
excerpt: Rolling all boards at once would maximize blast radius before the first device
  produced field evidence.
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
- url: /posts/ota-state-canary-cohort-stable-feedback-loop.html
  template: cms/templates/posts/posts--ota-state-canary-cohort-stable-feedback-loop.tpl
  source: cms/templates/posts/posts--ota-state-canary-cohort-stable-feedback-loop.json
---

# Canary to Cohort to Stable Is a Feedback Loop

The dangerous shortcut here was to collapse distributed state into one field. The actual problem was that Rolling all boards at once would maximize blast radius before the first device produced field evidence.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The production architecture starts with one designated canary, observes download/first boot/self-test/heartbeat/application health, then expands to 3 and 5 devices before broader rollout.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **Promotion pauses on unexpected rollback, crash-loop or health regression.**

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

This case became a distributed-systems boundary test. Device observation, server intent and release policy did not mean the same thing. The failure was Rolling all boards at once would maximize blast radius before the first device produced field evidence. Evidence showed The production architecture starts with one designated canary, observes download/first boot/self-test/heartbeat/application health, then expands to 3 and 5 devices before broader rollout. The mechanism was Staged rollout uses small cohorts to convert production observations into a decision about the next cohort. and the useful conclusion was Promotion pauses on unexpected rollback, crash-loop or health regression.

The practical rule was: **A canary is useful only when later rollout waits for its evidence.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
canary assignment -> release-scoped events -> heartbeat proves running release
        |                    |                         |
        +------ rollback/failure pauses promotion ----+
                             |
                       cohort -> cohort -> STABLE
```

I used one question to keep the model honest: **What event would prove the transition rather than merely suggest it?**

For this case, the answer starts with the observed problem: Rolling all boards at once would maximize blast radius before the first device produced field evidence. The control plane already had evidence that The production architecture starts with one designated canary, observes download/first boot/self-test/heartbeat/application health, then expands to 3 and 5 devices before broader rollout. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Staged rollout uses small cohorts to convert production observations into a decision about the next cohort.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Treating canary as a label while automatically scheduling the rest of the fleet immediately. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—Promotion pauses on unexpected rollback, crash-loop or health regression.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

Rollout logic should consume evidence rather than timers alone. Append-only events record release-scoped transitions, heartbeat confirms the actual running release, assignment status records convergence, and release state controls whether new devices may receive the image. A pause must stop new rollout while preserving evidence from devices already assigned. Rollback is then another explicit transition, not a manual rewrite of history.

The device should report facts it can observe and avoid guessing operator intent. In this case, the key observation is **The production architecture starts with one designated canary, observes download/first boot/self-test/heartbeat/application health, then expands to 3 and 5 devices before broader rollout.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Treating canary as a label while automatically scheduling the rest of the fleet immediately.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Staged rollout uses small cohorts to convert production observations into a decision about the next cohort. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The invariants I wanted before the transition

- canary evidence exists
- append-only events explain transitions
- promotion pauses on rollback/failure
- manual rollback target is still data-compatible
- failure drills exercise safety paths

For **Canary to Cohort to Stable Is a Feedback Loop**, the key mechanism is that Staged rollout uses small cohorts to convert production observations into a decision about the next cohort. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **Promotion pauses on unexpected rollback, crash-loop or health regression.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Staged rollout uses small cohorts to convert production observations into a decision about the next cohort.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## The rule I kept

**A canary is useful only when later rollout waits for its evidence.**

The result from this case was Promotion pauses on unexpected rollback, crash-loop or health regression.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
