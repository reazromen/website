---
title: Canary and Stable Are Different Release States
url: /posts/firmware-release-canary-and-stable-are-different-release-states.html
date: '2026-09-15'
read_time: 9
excerpt: A release that is available to one test device has not earned the same operational
  meaning as a release intended for the fleet.
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
- url: /posts/firmware-release-canary-and-stable-are-different-release-states.html
  template: cms/templates/posts/posts--firmware-release-canary-and-stable-are-different-release-states.tpl
  source: cms/templates/posts/posts--firmware-release-canary-and-stable-are-different-release-states.json
---

# Canary and Stable Are Different Release States

I used to think a firmware release was the binary produced after a successful build. A release that is available to one test device has not earned the same operational meaning as a release intended for the fleet.

The LOUP firmware path had a particularly unforgiving constraint: SIP/audio behavior already worked well enough to be valuable, so release work could not casually erase NVS, rewrite the flash layout, merge unrelated features or replace the rollback image. The goal was to make delivery safer without sacrificing the only known-good behavior.

For this article, the key evidence is specific: The OTA control-plane work separates canary assignment from stable promotion and requires acceptance evidence before widening rollout. The retained result was equally specific: Promotion became an explicit state transition rather than an accidental side effect of uploading a file. I treat both as observations from the documented release state, not as universal ESP32 rules.

## Case notebook

| Question | Recorded conclusion |
| --- | --- |
| Release problem | A release that is available to one test device has not earned the same operational meaning as a release intended for the fleet. |
| Evidence | The OTA control-plane work separates canary assignment from stable promotion and requires acceptance evidence before widening rollout. |
| Mechanism | Canary is a bounded experiment; stable is a policy decision backed by observed execution on compatible hardware. |
| Rejected shortcut | Using the same channel label for upload, test and production distribution. |
| Retained result | Promotion became an explicit state transition rather than an accidental side effect of uploading a file. |
| Rule carried forward | Availability, assignment, acceptance and promotion are separate release states. |

The table is intentionally stricter than a normal release note. A release note usually tells a reader what changed. This notebook also records what was *not* proven and which shortcut would have produced a misleading green status. That distinction mattered repeatedly in the LOUP work, especially while the golden V132A artifact, reconstructed source tree, V133A feature branch and later OTA control plane existed at different maturity levels.

## Promotion is a distributed consensus problem in miniature

The server can say what it wants a device to run, but only the device can report what actually booted. The build system can say what artifact was produced, but only the signing/verification path can say which artifact was authorized. A heartbeat can report a result, but that result is meaningful only for the release operation that produced it.

This is why I keep desired\_release\_id, running\_release\_id and terminal OTA result identity separate. It also explains why canary and stable are not just labels. Canary describes bounded exposure while evidence is still being gathered. Stable describes a policy decision after compatible hardware has actually executed and accepted the release.

The same model prevents stale-result bugs. A device that reports yesterday’s failed release must not automatically poison today’s assignment. Causality comes from release IDs and explicit state transitions, not from whichever status flag arrived most recently.

## A concrete scenario I use to test the rule

A canary release that exists in the database is not evidence. A canary device that reports the target release ID after boot and acceptance is evidence. That difference is the basis for promotion.

For this article, the scenario is useful because it targets the rejected shortcut directly: **Using the same channel label for upload, test and production distribution.**. I want the system to make that shortcut either impossible or obviously non-compliant with the release gate.

The falsification question is equally important. If a future implementation can demonstrate the same safety property with a simpler mechanism, I would change the mechanism. What I would not change casually is the invariant: **Availability, assignment, acceptance and promotion are separate release states.**. The release process exists to preserve that invariant while the implementation evolves.

## The mechanism underneath the release decision

Fleet release state is distributed state. The server has a desired release; the device has a running release; a heartbeat has an observation time; an OTA result belongs to one release operation; promotion is a separate policy decision. Most subtle fleet bugs appear when those identities are collapsed.

For **Canary and Stable Are Different Release States**, the important mechanism is this: Canary is a bounded experiment; stable is a policy decision backed by observed execution on compatible hardware.

That mechanism tells me which evidence is relevant. If the question is artifact identity, a call test alone is not enough; I need a hash and source identity. If the question is rollback, a signature alone is not enough; I need partition and persistent-schema compatibility. If the question is promotion, a CI pass is not enough; I need observed device state tied to the same release ID.

```
CREATED -> CANARY_ASSIGNED -> DOWNLOADED -> VERIFIED
        -> BOOTED_PENDING -> FIRMWARE_ACCEPTED / ACTIVE
        -> promotion evidence -> STABLE

any terminal OTA result carries release_id
```

The state machine is only trustworthy when desired and observed release IDs are explicit.

I use this model to stop release engineering from becoming a sequence of shell commands. The commands are implementation. The release contract is the set of invariants that must still be true when the commands finish.

## The controls I would require before accepting this state

- attach terminal OTA results to release\_id
- keep desired and running release IDs separate
- defer install during active calls
- require real-device acceptance before stable promotion
- expand rollout only after canary evidence

The point is not to maximize checklist length. Each control closes a different ambiguity that appeared in the real work. For this case, the shortcut I reject is **Using the same channel label for upload, test and production distribution.**. If that shortcut is allowed, the release can look successful while the underlying recovery or provenance guarantee is false.

I prefer a release gate that fails loudly and leaves the old artifact usable. That is why full-flash erasure, force-pushing golden tags, disabling certificate verification, or widening a rollout to compensate for unclear state are all wrong directions. They destroy evidence or increase blast radius exactly when uncertainty is highest.

## How I would try to break this before trusting it

Release safety is difficult to prove with only the happy path. For this class of change I want at least one test that intentionally violates the assumption the release depends on.

For **Canary and Stable Are Different Release States**, I would construct a negative test around the mechanism: Canary is a bounded experiment; stable is a policy decision backed by observed execution on compatible hardware. That might mean removing a required source file from the clean checkout, presenting a wrong signature, assigning a release to the wrong hardware revision, forcing first-boot self-test failure, rolling back after a schema migration, or replaying a terminal OTA result for an older release ID.

The expected behavior should be boring: reject the artifact or assignment, keep/restore the previous accepted image, preserve persistent state where promised, and surface an attributable failure state. A test is especially valuable when it proves the system does *not* accept a dangerous shortcut.

This is why I distinguish recoverability tests from build tests. A compiler can prove syntax and linking. It cannot prove that a power interruption during slot write, a bad first boot or a stale heartbeat result leaves the fleet in a state the operator can understand.

## Keep chronology honest

The V132A/V133A recovery documents are useful because they did not retroactively turn incomplete work into completed work. At the August handoff, the golden V132A rollback binary was proven, while the V133A feature branch had source work that still needed clean-build, flash, physical power and clear-audio regression evidence. Later fleet/OTA work added a different layer of production acceptance.

That chronology matters for this topic because **Promotion became an explicit state transition rather than an accidental side effect of uploading a file.** should be read as the result of the evidence chain that actually existed at that stage. I do not use a later production capability to rewrite an earlier handoff as if it had already passed.

This is also how I want release dashboards and articles to behave. A state such as `built`, `signed`, `assigned`, `booted`, `accepted`, `active` or `stable` should mean one thing and be backed by the evidence required for that state. The system becomes hard to operate when success words float free of their acceptance gates.

## What changes when the fleet grows

On one board, I can recover with USB and inspect serial output manually. At five or twenty devices, release identity, assignment and rollback have to be queryable. At a larger production fleet, I would tighten the same model rather than replace it: hardware-backed key provisioning, Secure Boot v2 and Flash Encryption under a controlled ceremony, more formal signing custody, staged rollout cohorts, automated rollback evidence, schema-compatibility tests and independent release audit records.

The important thing is that scale does not remove the original invariant. Availability, assignment, acceptance and promotion are separate release states. A larger fleet only makes violations more expensive.

I would also keep service-mode releases separate from normal app OTA. Partition-table, bootloader and security-epoch transitions deserve a dedicated recovery plan because they modify the machinery that normal OTA depends on. That separation is useful at ten devices and essential at ten thousand.

## The lesson I keep

The result I keep from this case is: **Promotion became an explicit state transition rather than an accidental side effect of uploading a file.**

The deeper lesson is **Availability, assignment, acceptance and promotion are separate release states.**

That is how I now define production firmware work. The release is not the moment a `.bin` file appears. It is the chain that connects source, artifact, signature, compatibility, flash topology, persistent state, real-device acceptance and observable running state—with a rollback path whose assumptions have actually been tested.
