---
title: OTA Installation Must Lose to an Active Voice Call
url: /posts/firmware-release-ota-installation-must-lose-to-active-call.html
date: '2025-06-28'
read_time: 9
excerpt: A voice device can be idle from the server perspective while a user is in
  an active SIP conversation that must not be interrupted by an update.
topic: firmware-release-engineering
tags:
- esp32-s3
- firmware-release-engineering
- loup
draft: false
featured: false
language: en
eyebrow: 'Production Firmware: Canary, Promotion & Acceptance · deep-dive'
outputs:
- url: /posts/firmware-release-ota-installation-must-lose-to-active-call.html
  template: cms/templates/posts/posts--firmware-release-ota-installation-must-lose-to-active-call.tpl
  source: cms/templates/posts/posts--firmware-release-ota-installation-must-lose-to-active-call.json
---

# OTA Installation Must Lose to an Active Voice Call

A working ESP32-S3 build is easy to over-trust. In this case, a voice device can be idle from the server perspective while a user is in an active SIP conversation that must not be interrupted by an update.

The LOUP firmware path had a particularly unforgiving constraint: SIP/audio behavior already worked well enough to be valuable, so release work could not casually erase NVS, rewrite the flash layout, merge unrelated features or replace the rollback image. The goal was to make delivery safer without sacrificing the only known-good behavior.

For this article, the key evidence is specific: The OTA integration rules explicitly defer installation during an active call and run provisioning/OTA work below the realtime audio path. The retained result was equally specific: Update scheduling became state-aware and could wait for a safe idle point. I treat both as observations from the documented release state, not as universal ESP32 rules.

## Case notebook

| Question | Recorded conclusion |
| --- | --- |
| Release problem | A voice device can be idle from the server perspective while a user is in an active SIP conversation that must not be interrupted by an update. |
| Evidence | The OTA integration rules explicitly defer installation during an active call and run provisioning/OTA work below the realtime audio path. |
| Mechanism | Firmware update is maintenance work; an active call is current user traffic with tighter latency and continuity requirements. |
| Rejected shortcut | Treating a mandatory update flag as permission to reboot immediately. |
| Retained result | Update scheduling became state-aware and could wait for a safe idle point. |
| Rule carried forward | Maintenance policy must respect the product state machine, not only the backend release state. |

The table is intentionally stricter than a normal release note. A release note usually tells a reader what changed. This notebook also records what was *not* proven and which shortcut would have produced a misleading green status. That distinction mattered repeatedly in the LOUP work, especially while the golden V132A artifact, reconstructed source tree, V133A feature branch and later OTA control plane existed at different maturity levels.

## Promotion is a distributed consensus problem in miniature

The server can say what it wants a device to run, but only the device can report what actually booted. The build system can say what artifact was produced, but only the signing/verification path can say which artifact was authorized. A heartbeat can report a result, but that result is meaningful only for the release operation that produced it.

This is why I keep desired\_release\_id, running\_release\_id and terminal OTA result identity separate. It also explains why canary and stable are not just labels. Canary describes bounded exposure while evidence is still being gathered. Stable describes a policy decision after compatible hardware has actually executed and accepted the release.

The same model prevents stale-result bugs. A device that reports yesterday’s failed release must not automatically poison today’s assignment. Causality comes from release IDs and explicit state transitions, not from whichever status flag arrived most recently.

## A concrete scenario I use to test the rule

The user’s active call outranks maintenance. Even a mandatory update can wait for an idle point unless the product explicitly defines an emergency policy that says otherwise.

For this article, the scenario is useful because it targets the rejected shortcut directly: **Treating a mandatory update flag as permission to reboot immediately.**. I want the system to make that shortcut either impossible or obviously non-compliant with the release gate.

The falsification question is equally important. If a future implementation can demonstrate the same safety property with a simpler mechanism, I would change the mechanism. What I would not change casually is the invariant: **Maintenance policy must respect the product state machine, not only the backend release state.**. The release process exists to preserve that invariant while the implementation evolves.

## The mechanism underneath the release decision

Fleet release state is distributed state. The server has a desired release; the device has a running release; a heartbeat has an observation time; an OTA result belongs to one release operation; promotion is a separate policy decision. Most subtle fleet bugs appear when those identities are collapsed.

For **OTA Installation Must Lose to an Active Voice Call**, the important mechanism is this: Firmware update is maintenance work; an active call is current user traffic with tighter latency and continuity requirements.

That mechanism tells me which evidence is relevant. If the question is artifact identity, a call test alone is not enough; I need a hash and source identity. If the question is rollback, a signature alone is not enough; I need partition and persistent-schema compatibility. If the question is promotion, a CI pass is not enough; I need observed device state tied to the same release ID.

```
CREATED -> CANARY_ASSIGNED -> DOWNLOADED -> VERIFIED
        -> BOOTED_PENDING -> FIRMWARE_ACCEPTED / ACTIVE
        -> promotion evidence -> STABLE

any terminal OTA result carries release_id
```

The state machine is only trustworthy when desired and observed release IDs are explicit.

I use this model to stop release engineering from becoming a sequence of shell commands. The commands are implementation. The release contract is the set of invariants that must still be true when the commands finish.

## How I would try to break this before trusting it

Release safety is difficult to prove with only the happy path. For this class of change I want at least one test that intentionally violates the assumption the release depends on.

For **OTA Installation Must Lose to an Active Voice Call**, I would construct a negative test around the mechanism: Firmware update is maintenance work; an active call is current user traffic with tighter latency and continuity requirements. That might mean removing a required source file from the clean checkout, presenting a wrong signature, assigning a release to the wrong hardware revision, forcing first-boot self-test failure, rolling back after a schema migration, or replaying a terminal OTA result for an older release ID.

The expected behavior should be boring: reject the artifact or assignment, keep/restore the previous accepted image, preserve persistent state where promised, and surface an attributable failure state. A test is especially valuable when it proves the system does *not* accept a dangerous shortcut.

This is why I distinguish recoverability tests from build tests. A compiler can prove syntax and linking. It cannot prove that a power interruption during slot write, a bad first boot or a stale heartbeat result leaves the fleet in a state the operator can understand.

## What this costs

The stricter release model adds work. Hashes, manifests, detached signatures, isolated builds, compatibility metadata, dual slots, schema versions and promotion gates all create operational surface area. On a small product team that overhead can feel disproportionate to one ESP32-S3 binary.

The alternative cost is hidden. Without these controls, a good audio artifact can be overwritten, a feature branch can silently become the new baseline, an old image can be unable to read migrated NVS, a runtime server compromise can become signing compromise, or the fleet can report “failed” for the wrong release because one stale result had no causal identity.

For this case the retained rule is **Maintenance policy must respect the product state machine, not only the backend release state.**. I accept the additional release machinery when it closes a failure mode that would otherwise require physical recovery or make the operator unable to state which firmware is really running.

## The controls I would require before accepting this state

- attach terminal OTA results to release\_id
- keep desired and running release IDs separate
- defer install during active calls
- require real-device acceptance before stable promotion
- expand rollout only after canary evidence

The point is not to maximize checklist length. Each control closes a different ambiguity that appeared in the real work. For this case, the shortcut I reject is **Treating a mandatory update flag as permission to reboot immediately.**. If that shortcut is allowed, the release can look successful while the underlying recovery or provenance guarantee is false.

I prefer a release gate that fails loudly and leaves the old artifact usable. That is why full-flash erasure, force-pushing golden tags, disabling certificate verification, or widening a rollout to compensate for unclear state are all wrong directions. They destroy evidence or increase blast radius exactly when uncertainty is highest.

## What changes when the fleet grows

On one board, I can recover with USB and inspect serial output manually. At five or twenty devices, release identity, assignment and rollback have to be queryable. At a larger production fleet, I would tighten the same model rather than replace it: hardware-backed key provisioning, Secure Boot v2 and Flash Encryption under a controlled ceremony, more formal signing custody, staged rollout cohorts, automated rollback evidence, schema-compatibility tests and independent release audit records.

The important thing is that scale does not remove the original invariant. Maintenance policy must respect the product state machine, not only the backend release state. A larger fleet only makes violations more expensive.

I would also keep service-mode releases separate from normal app OTA. Partition-table, bootloader and security-epoch transitions deserve a dedicated recovery plan because they modify the machinery that normal OTA depends on. That separation is useful at ten devices and essential at ten thousand.

## The lesson I keep

The result I keep from this case is: **Update scheduling became state-aware and could wait for a safe idle point.**

The deeper lesson is **Maintenance policy must respect the product state machine, not only the backend release state.**

That is how I now define production firmware work. The release is not the moment a `.bin` file appears. It is the chain that connects source, artifact, signature, compatibility, flash topology, persistent state, real-device acceptance and observable running state—with a rollback path whose assumptions have actually been tested.
