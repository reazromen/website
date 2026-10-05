---
title: Automatic Rollback and Fleet Rollback Solve Different Failures
url: /posts/ota-state-automatic-vs-control-plane-rollback.html
date: '2020-05-25'
read_time: 8
excerpt: One rollback mechanism could not cover both immediate boot failure and defects
  discovered after a release had already been accepted.
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
- url: /posts/ota-state-automatic-vs-control-plane-rollback.html
  template: cms/templates/posts/posts--ota-state-automatic-vs-control-plane-rollback.tpl
  source: cms/templates/posts/posts--ota-state-automatic-vs-control-plane-rollback.json
---

# Automatic Rollback and Fleet Rollback Solve Different Failures

A firmware image can be perfectly valid and still be the wrong update. This case started because One rollback mechanism could not cover both immediate boot failure and defects discovered after a release had already been accepted.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The architecture requires device automatic rollback for pending-image validation failure and control-plane rollback that reassigns a previous compatible release after later problems.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **The system retained both local and operator-driven recovery paths.**

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

I approached this as a transaction with an explicit commit point. The problem was One rollback mechanism could not cover both immediate boot failure and defects discovered after a release had already been accepted. The evidence was The architecture requires device automatic rollback for pending-image validation failure and control-plane rollback that reassigns a previous compatible release after later problems. The reason that evidence mattered is Bootloader rollback protects a local transaction before commit; control-plane rollback is a new desired-state transition after commit. I deliberately avoided Calling A/B rollback complete fleet rollback support.. The accepted outcome was The system retained both local and operator-driven recovery paths.

The practical rule was: **Recovery before acceptance and recovery after acceptance are different state machines.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
canary assignment -> release-scoped events -> heartbeat proves running release
        |                    |                         |
        +------ rollback/failure pauses promotion ----+
                             |
                       cohort -> cohort -> STABLE
```

I used one question to keep the model honest: **Which component is allowed to commit this state?**

For this case, the answer starts with the observed problem: One rollback mechanism could not cover both immediate boot failure and defects discovered after a release had already been accepted. The control plane already had evidence that The architecture requires device automatic rollback for pending-image validation failure and control-plane rollback that reassigns a previous compatible release after later problems. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Bootloader rollback protects a local transaction before commit; control-plane rollback is a new desired-state transition after commit.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Calling A/B rollback complete fleet rollback support. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—The system retained both local and operator-driven recovery paths.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

Rollout logic should consume evidence rather than timers alone. Append-only events record release-scoped transitions, heartbeat confirms the actual running release, assignment status records convergence, and release state controls whether new devices may receive the image. A pause must stop new rollout while preserving evidence from devices already assigned. Rollback is then another explicit transition, not a manual rewrite of history.

The control plane should remain conservative when evidence is missing or stale. In this case, the key observation is **The architecture requires device automatic rollback for pending-image validation failure and control-plane rollback that reassigns a previous compatible release after later problems.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Calling A/B rollback complete fleet rollback support.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## Incident contract

| Question | Recorded answer |
| --- | --- |
| Problem | One rollback mechanism could not cover both immediate boot failure and defects discovered after a release had already been accepted. |
| Evidence | The architecture requires device automatic rollback for pending-image validation failure and control-plane rollback that reassigns a previous compatible release after later problems. |
| Mechanism | Bootloader rollback protects a local transaction before commit; control-plane rollback is a new desired-state transition after commit. |
| Rejected shortcut | Calling A/B rollback complete fleet rollback support. |
| Result | The system retained both local and operator-driven recovery paths. |
| Rule | Recovery before acceptance and recovery after acceptance are different state machines. |

I keep this matrix because OTA incidents are easy to rewrite after recovery. Once a device comes back, an old heartbeat string, an assignment row and a release state can all look consistent even when they referred to different transitions. Recording causal identity while the incident is active prevents that retrospective simplification.

## The failure test I would run

I would deliberately **promote without reviewing event history**.

The expected outcome is not merely “the request fails.” I want the resulting state to remain explainable. The device row, assignment state, release state and append-only event history should agree on what happened and which release the event belonged to. If recovery occurs, it should happen through a defined transition rather than an administrator manually editing the database until the dashboard turns green.

This case is particularly useful because the rejected shortcut was **Calling A/B rollback complete fleet rollback support.**. The failure test forces that shortcut to reveal its ambiguity. A good state model should make the unsafe interpretation impossible or at least operationally visible.

## Operational consequence

The retained engineering rule is **Recovery before acceptance and recovery after acceptance are different state machines.**. I want that rule enforced in code or policy wherever possible, not left as a runbook sentence that an operator must remember under pressure.

That means state transitions should reject incompatible releases, release promotion should have explicit blockers, heartbeat processing should be conservative about terminal states, and artifact serving should repeat compatibility checks. The event log should preserve who or what caused each important transition. Recovery should be a first-class path rather than an exceptional database repair.

For this article, the operational result was The system retained both local and operator-driven recovery paths. That makes the system easier to reason about because each dashboard badge corresponds to a bounded claim rather than an optimistic summary.

## The rule I kept

**Recovery before acceptance and recovery after acceptance are different state machines.**

The result from this case was The system retained both local and operator-driven recovery paths.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
