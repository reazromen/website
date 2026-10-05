---
title: App-Only Flashing at 0x20000 Protected the State I Was Not Trying to Change
url: /posts/firmware-release-app-only-flash-0x20000-protected-state.html
date: '2024-03-22'
read_time: 9
excerpt: Audio iteration needed to replace application code without repeatedly erasing
  NVS, bootloader, partition metadata or other persistent device state.
topic: firmware-release-engineering
tags:
- esp32-s3
- firmware-release-engineering
- loup
draft: false
featured: false
language: en
eyebrow: 'Production Firmware: Partitions, Rollback & Persistent State · deep-dive'
outputs:
- url: /posts/firmware-release-app-only-flash-0x20000-protected-state.html
  template: cms/templates/posts/posts--firmware-release-app-only-flash-0x20000-protected-state.tpl
  source: cms/templates/posts/posts--firmware-release-app-only-flash-0x20000-protected-state.json
---

# App-Only Flashing at 0x20000 Protected the State I Was Not Trying to Change

This part of the LOUP firmware work was less about adding code than deciding what I was allowed to call a release. Audio iteration needed to replace application code without repeatedly erasing NVS, bootloader, partition metadata or other persistent device state.

The LOUP firmware path had a particularly unforgiving constraint: SIP/audio behavior already worked well enough to be valuable, so release work could not casually erase NVS, rewrite the flash layout, merge unrelated features or replace the rollback image. The goal was to make delivery safer without sacrificing the only known-good behavior.

For this article, the key evidence is specific: The V132A/V133A recovery rules specified application-only flashing at 0x20000 and explicitly prohibited full erase for that task. The retained result was equally specific: Audio and feature candidates could be tested while preserving the rest of the known device environment and keeping immediate rollback available. I treat both as observations from the documented release state, not as universal ESP32 rules.

## Case notebook

| Question | Recorded conclusion |
| --- | --- |
| Release problem | Audio iteration needed to replace application code without repeatedly erasing NVS, bootloader, partition metadata or other persistent device state. |
| Evidence | The V132A/V133A recovery rules specified application-only flashing at 0x20000 and explicitly prohibited full erase for that task. |
| Mechanism | A flash operation has a blast radius. When only the application is under test, preserving unrelated persistent regions reduces both risk and diagnostic ambiguity. |
| Rejected shortcut | Using erase\_flash as a generic cure for every boot or configuration problem. |
| Retained result | Audio and feature candidates could be tested while preserving the rest of the known device environment and keeping immediate rollback available. |
| Rule carried forward | Make the flash operation no broader than the hypothesis under test. |

The table is intentionally stricter than a normal release note. A release note usually tells a reader what changed. This notebook also records what was *not* proven and which shortcut would have produced a misleading green status. That distinction mattered repeatedly in the LOUP work, especially while the golden V132A artifact, reconstructed source tree, V133A feature branch and later OTA control plane existed at different maturity levels.

## Rollback is code plus boot state plus data state

Dual OTA slots solve only one part of recovery. The bootloader needs to know which image is pending and which image is accepted. The new application needs a deterministic self-test that does not depend on an unreliable external service. Persistent configuration must remain readable if the bootloader chooses the previous image. If any one of those conditions is false, “we have two slots” can still leave the product unrecoverable.

I therefore model rollback compatibility as a relation between releases rather than a property of a single binary. Release B can roll back to release A only if the flash layout permits it, the bootloader policy permits it, and the persistent schema written by B remains acceptable to A or has a reversible migration path.

This becomes especially important when partition layout itself changes. A layout migration is not an ordinary application update because it changes the substrate normal OTA relies on. That is why service-mode recovery remains part of the design.

## A concrete scenario I use to test the rule

The safest app-only iteration is intentionally boring: write the application partition, boot, test, and preserve NVS/boot metadata unless the experiment is specifically about them. That keeps rollback meaningful and reduces variables.

For this article, the scenario is useful because it targets the rejected shortcut directly: **Using erase\_flash as a generic cure for every boot or configuration problem.**. I want the system to make that shortcut either impossible or obviously non-compliant with the release gate.

The falsification question is equally important. If a future implementation can demonstrate the same safety property with a simpler mechanism, I would change the mechanism. What I would not change casually is the invariant: **Make the flash operation no broader than the hypothesis under test.**. The release process exists to preserve that invariant while the implementation evolves.

## The mechanism underneath the release decision

Rollback depends on flash topology and persistent data. The bootloader needs somewhere safe to boot from, the new image needs a pending/accepted state, and the previous image needs to understand whatever state the new image already wrote. A second slot without schema discipline is only half a rollback system.

For **App-Only Flashing at 0x20000 Protected the State I Was Not Trying to Change**, the important mechanism is this: A flash operation has a blast radius. When only the application is under test, preserving unrelated persistent regions reduces both risk and diagnostic ambiguity.

That mechanism tells me which evidence is relevant. If the question is artifact identity, a call test alone is not enough; I need a hash and source identity. If the question is rollback, a signature alone is not enough; I need partition and persistent-schema compatibility. If the question is promotion, a CI pass is not enough; I need observed device state tied to the same release ID.

```
otadata
ota_0   <- currently accepted app
ota_1   <- inactive target

install -> set boot partition -> reboot
        -> PENDING_VERIFY
        -> local self-test
        -> VALID  or  rollback
```

Persistent schema compatibility must be evaluated across the same transition.

I use this model to stop release engineering from becoming a sequence of shell commands. The commands are implementation. The release contract is the set of invariants that must still be true when the commands finish.

## The controls I would require before accepting this state

- inspect the actual partition table before migration
- keep NVS unless migration explicitly requires change
- enable first-boot rollback state
- version persistent schemas
- test rollback after migration, not only upgrade

The point is not to maximize checklist length. Each control closes a different ambiguity that appeared in the real work. For this case, the shortcut I reject is **Using erase\_flash as a generic cure for every boot or configuration problem.**. If that shortcut is allowed, the release can look successful while the underlying recovery or provenance guarantee is false.

I prefer a release gate that fails loudly and leaves the old artifact usable. That is why full-flash erasure, force-pushing golden tags, disabling certificate verification, or widening a rollout to compensate for unclear state are all wrong directions. They destroy evidence or increase blast radius exactly when uncertainty is highest.

## How I would try to break this before trusting it

Release safety is difficult to prove with only the happy path. For this class of change I want at least one test that intentionally violates the assumption the release depends on.

For **App-Only Flashing at 0x20000 Protected the State I Was Not Trying to Change**, I would construct a negative test around the mechanism: A flash operation has a blast radius. When only the application is under test, preserving unrelated persistent regions reduces both risk and diagnostic ambiguity. That might mean removing a required source file from the clean checkout, presenting a wrong signature, assigning a release to the wrong hardware revision, forcing first-boot self-test failure, rolling back after a schema migration, or replaying a terminal OTA result for an older release ID.

The expected behavior should be boring: reject the artifact or assignment, keep/restore the previous accepted image, preserve persistent state where promised, and surface an attributable failure state. A test is especially valuable when it proves the system does *not* accept a dangerous shortcut.

This is why I distinguish recoverability tests from build tests. A compiler can prove syntax and linking. It cannot prove that a power interruption during slot write, a bad first boot or a stale heartbeat result leaves the fleet in a state the operator can understand.

## Keep chronology honest

The V132A/V133A recovery documents are useful because they did not retroactively turn incomplete work into completed work. At the August handoff, the golden V132A rollback binary was proven, while the V133A feature branch had source work that still needed clean-build, flash, physical power and clear-audio regression evidence. Later fleet/OTA work added a different layer of production acceptance.

That chronology matters for this topic because **Audio and feature candidates could be tested while preserving the rest of the known device environment and keeping immediate rollback available.** should be read as the result of the evidence chain that actually existed at that stage. I do not use a later production capability to rewrite an earlier handoff as if it had already passed.

This is also how I want release dashboards and articles to behave. A state such as `built`, `signed`, `assigned`, `booted`, `accepted`, `active` or `stable` should mean one thing and be backed by the evidence required for that state. The system becomes hard to operate when success words float free of their acceptance gates.

## What changes when the fleet grows

On one board, I can recover with USB and inspect serial output manually. At five or twenty devices, release identity, assignment and rollback have to be queryable. At a larger production fleet, I would tighten the same model rather than replace it: hardware-backed key provisioning, Secure Boot v2 and Flash Encryption under a controlled ceremony, more formal signing custody, staged rollout cohorts, automated rollback evidence, schema-compatibility tests and independent release audit records.

The important thing is that scale does not remove the original invariant. Make the flash operation no broader than the hypothesis under test. A larger fleet only makes violations more expensive.

I would also keep service-mode releases separate from normal app OTA. Partition-table, bootloader and security-epoch transitions deserve a dedicated recovery plan because they modify the machinery that normal OTA depends on. That separation is useful at ten devices and essential at ten thousand.

## The lesson I keep

The result I keep from this case is: **Audio and feature candidates could be tested while preserving the rest of the known device environment and keeping immediate rollback available.**

The deeper lesson is **Make the flash operation no broader than the hypothesis under test.**

That is how I now define production firmware work. The release is not the moment a `.bin` file appears. It is the chain that connects source, artifact, signature, compatibility, flash topology, persistent state, real-device acceptance and observable running state—with a rollback path whose assumptions have actually been tested.
