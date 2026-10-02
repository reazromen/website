---
title: Heartbeat Is Observation, Not Enrollment
url: /posts/ota-state-heartbeat-is-observation-not-enrollment.html
date: '2026-09-15'
read_time: 8
excerpt: A device sending telemetry could look alive even when its identity or enrollment
  state was not valid for production operations.
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
- url: /posts/ota-state-heartbeat-is-observation-not-enrollment.html
  template: cms/templates/posts/posts--ota-state-heartbeat-is-observation-not-enrollment.tpl
  source: cms/templates/posts/posts--ota-state-heartbeat-is-observation-not-enrollment.json
---

# Heartbeat Is Observation, Not Enrollment

A firmware image can be perfectly valid and still be the wrong update. This case started because A device sending telemetry could look alive even when its identity or enrollment state was not valid for production operations.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The architecture treats enrollment/authentication separately from heartbeat; heartbeat reports running release, boot state, schema/security generations and health telemetry only after per-device authentication.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **Heartbeat remained an authenticated observation channel rather than an identity-creation mechanism.**

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

I approached this as a transaction with an explicit commit point. The problem was A device sending telemetry could look alive even when its identity or enrollment state was not valid for production operations. The evidence was The architecture treats enrollment/authentication separately from heartbeat; heartbeat reports running release, boot state, schema/security generations and health telemetry only after per-device authentication. The reason that evidence mattered is Telemetry is evidence about current runtime state, not proof that the original trust transition was valid. I deliberately avoided Promoting a device into the fleet merely because it can POST a heartbeat-shaped payload.. The accepted outcome was Heartbeat remained an authenticated observation channel rather than an identity-creation mechanism.

The practical rule was: **Do not let observability silently become authorization.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
factory_registered --consume bootstrap--> enrolled
      |                                  |
      |                                  +--> unique runtime credential
      |                                         |
      +-----------------------------------------+--> active / blocked / revoked
heartbeat observes runtime; it does not create trust.
```

I used one question to keep the model honest: **Which component is allowed to commit this state?**

For this case, the answer starts with the observed problem: A device sending telemetry could look alive even when its identity or enrollment state was not valid for production operations. The control plane already had evidence that The architecture treats enrollment/authentication separately from heartbeat; heartbeat reports running release, boot state, schema/security generations and health telemetry only after per-device authentication. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Telemetry is evidence about current runtime state, not proof that the original trust transition was valid.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Promoting a device into the fleet merely because it can POST a heartbeat-shaped payload. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—Heartbeat remained an authenticated observation channel rather than an identity-creation mechanism.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

The implementation boundary starts before the OTA code. Device inventory must retain hardware identity even when credentials rotate. Enrollment consumes bootstrap authority and returns a runtime credential once; the database stores a verifier/hash rather than the reusable plaintext. Heartbeat endpoints then authenticate that runtime credential before accepting observations. If an operator blocks a device, the policy decision should be visible separately from credential revocation so recovery does not require inventing a new identity.

The control plane should remain conservative when evidence is missing or stale. In this case, the key observation is **The architecture treats enrollment/authentication separately from heartbeat; heartbeat reports running release, boot state, schema/security generations and health telemetry only after per-device authentication.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Promoting a device into the fleet merely because it can POST a heartbeat-shaped payload.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## Operational consequence

The retained engineering rule is **Do not let observability silently become authorization.**. I want that rule enforced in code or policy wherever possible, not left as a runbook sentence that an operator must remember under pressure.

That means state transitions should reject incompatible releases, release promotion should have explicit blockers, heartbeat processing should be conservative about terminal states, and artifact serving should repeat compatibility checks. The event log should preserve who or what caused each important transition. Recovery should be a first-class path rather than an exceptional database repair.

For this article, the operational result was Heartbeat remained an authenticated observation channel rather than an identity-creation mechanism. That makes the system easier to reason about because each dashboard badge corresponds to a bounded claim rather than an optimistic summary.

## Incident contract

| Question | Recorded answer |
| --- | --- |
| Problem | A device sending telemetry could look alive even when its identity or enrollment state was not valid for production operations. |
| Evidence | The architecture treats enrollment/authentication separately from heartbeat; heartbeat reports running release, boot state, schema/security generations and health telemetry only after per-device authentication. |
| Mechanism | Telemetry is evidence about current runtime state, not proof that the original trust transition was valid. |
| Rejected shortcut | Promoting a device into the fleet merely because it can POST a heartbeat-shaped payload. |
| Result | Heartbeat remained an authenticated observation channel rather than an identity-creation mechanism. |
| Rule | Do not let observability silently become authorization. |

I keep this matrix because OTA incidents are easy to rewrite after recovery. Once a device comes back, an old heartbeat string, an assignment row and a release state can all look consistent even when they referred to different transitions. Recording causal identity while the incident is active prevents that retrospective simplification.

## The failure test I would run

I would deliberately **rotate credential while preserving device identity**.

The expected outcome is not merely “the request fails.” I want the resulting state to remain explainable. The device row, assignment state, release state and append-only event history should agree on what happened and which release the event belonged to. If recovery occurs, it should happen through a defined transition rather than an administrator manually editing the database until the dashboard turns green.

This case is particularly useful because the rejected shortcut was **Promoting a device into the fleet merely because it can POST a heartbeat-shaped payload.**. The failure test forces that shortcut to reveal its ambiguity. A good state model should make the unsafe interpretation impossible or at least operationally visible.

## The rule I kept

**Do not let observability silently become authorization.**

The result from this case was Heartbeat remained an authenticated observation channel rather than an identity-creation mechanism.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
