---
title: A Factory-Only Partition Layout Cannot Magically Become Dual-Slot OTA
url: /posts/firmware-release-factory-layout-cannot-magically-become-dual-slot-ota.html
date: '2026-09-15'
read_time: 9
excerpt: The earlier firmware context used a factory application partition and had
  no otadata, ota_0 or ota_1, yet production OTA required dual application slots.
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
- url: /posts/firmware-release-factory-layout-cannot-magically-become-dual-slot-ota.html
  template: cms/templates/posts/posts--firmware-release-factory-layout-cannot-magically-become-dual-slot-ota.tpl
  source: cms/templates/posts/posts--firmware-release-factory-layout-cannot-magically-become-dual-slot-ota.json
---

# A Factory-Only Partition Layout Cannot Magically Become Dual-Slot OTA

A working ESP32-S3 build is easy to over-trust. In this case, the earlier firmware context used a factory application partition and had no otadata, ota\_0 or ota\_1, yet production OTA required dual application slots.

The LOUP firmware path had a particularly unforgiving constraint: SIP/audio behavior already worked well enough to be valuable, so release work could not casually erase NVS, rewrite the flash layout, merge unrelated features or replace the rollback image. The goal was to make delivery safer without sacrificing the only known-good behavior.

For this article, the key evidence is specific: The OTA integration plan explicitly warned that the first transition to an OTA-capable partition layout would likely require serial/USB service and should not be pretended to be a normal app OTA migration. The retained result was equally specific: Partition-generation changes were separated from normal application releases. I treat both as observations from the documented release state, not as universal ESP32 rules.

## Case notebook

| Question | Recorded conclusion |
| --- | --- |
| Release problem | The earlier firmware context used a factory application partition and had no otadata, ota\_0 or ota\_1, yet production OTA required dual application slots. |
| Evidence | The OTA integration plan explicitly warned that the first transition to an OTA-capable partition layout would likely require serial/USB service and should not be pretended to be a normal app OTA migration. |
| Mechanism | The partition table is boot infrastructure. Normal application OTA writes an application slot; it does not safely rewrite the entire flash layout by assumption. |
| Rejected shortcut | Shipping code that attempts to OTA itself into a layout that has no inactive OTA slot. |
| Retained result | Partition-generation changes were separated from normal application releases. |
| Rule carried forward | Freeze production partition architecture early and treat layout migrations as service-mode operations. |

The table is intentionally stricter than a normal release note. A release note usually tells a reader what changed. This notebook also records what was *not* proven and which shortcut would have produced a misleading green status. That distinction mattered repeatedly in the LOUP work, especially while the golden V132A artifact, reconstructed source tree, V133A feature branch and later OTA control plane existed at different maturity levels.

## Rollback is code plus boot state plus data state

Dual OTA slots solve only one part of recovery. The bootloader needs to know which image is pending and which image is accepted. The new application needs a deterministic self-test that does not depend on an unreliable external service. Persistent configuration must remain readable if the bootloader chooses the previous image. If any one of those conditions is false, “we have two slots” can still leave the product unrecoverable.

I therefore model rollback compatibility as a relation between releases rather than a property of a single binary. Release B can roll back to release A only if the flash layout permits it, the bootloader policy permits it, and the persistent schema written by B remains acceptable to A or has a reversible migration path.

This becomes especially important when partition layout itself changes. A layout migration is not an ordinary application update because it changes the substrate normal OTA relies on. That is why service-mode recovery remains part of the design.

## A concrete scenario I use to test the rule

A factory-only layout has no inactive OTA slot waiting to receive a candidate. Pretending otherwise moves the risk into boot infrastructure. The first OTA-capable transition therefore belongs to a controlled service operation.

For this article, the scenario is useful because it targets the rejected shortcut directly: **Shipping code that attempts to OTA itself into a layout that has no inactive OTA slot.**. I want the system to make that shortcut either impossible or obviously non-compliant with the release gate.

The falsification question is equally important. If a future implementation can demonstrate the same safety property with a simpler mechanism, I would change the mechanism. What I would not change casually is the invariant: **Freeze production partition architecture early and treat layout migrations as service-mode operations.**. The release process exists to preserve that invariant while the implementation evolves.

## The mechanism underneath the release decision

Rollback depends on flash topology and persistent data. The bootloader needs somewhere safe to boot from, the new image needs a pending/accepted state, and the previous image needs to understand whatever state the new image already wrote. A second slot without schema discipline is only half a rollback system.

For **A Factory-Only Partition Layout Cannot Magically Become Dual-Slot OTA**, the important mechanism is this: The partition table is boot infrastructure. Normal application OTA writes an application slot; it does not safely rewrite the entire flash layout by assumption.

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

## How I would try to break this before trusting it

Release safety is difficult to prove with only the happy path. For this class of change I want at least one test that intentionally violates the assumption the release depends on.

For **A Factory-Only Partition Layout Cannot Magically Become Dual-Slot OTA**, I would construct a negative test around the mechanism: The partition table is boot infrastructure. Normal application OTA writes an application slot; it does not safely rewrite the entire flash layout by assumption. That might mean removing a required source file from the clean checkout, presenting a wrong signature, assigning a release to the wrong hardware revision, forcing first-boot self-test failure, rolling back after a schema migration, or replaying a terminal OTA result for an older release ID.

The expected behavior should be boring: reject the artifact or assignment, keep/restore the previous accepted image, preserve persistent state where promised, and surface an attributable failure state. A test is especially valuable when it proves the system does *not* accept a dangerous shortcut.

This is why I distinguish recoverability tests from build tests. A compiler can prove syntax and linking. It cannot prove that a power interruption during slot write, a bad first boot or a stale heartbeat result leaves the fleet in a state the operator can understand.

## What this costs

The stricter release model adds work. Hashes, manifests, detached signatures, isolated builds, compatibility metadata, dual slots, schema versions and promotion gates all create operational surface area. On a small product team that overhead can feel disproportionate to one ESP32-S3 binary.

The alternative cost is hidden. Without these controls, a good audio artifact can be overwritten, a feature branch can silently become the new baseline, an old image can be unable to read migrated NVS, a runtime server compromise can become signing compromise, or the fleet can report “failed” for the wrong release because one stale result had no causal identity.

For this case the retained rule is **Freeze production partition architecture early and treat layout migrations as service-mode operations.**. I accept the additional release machinery when it closes a failure mode that would otherwise require physical recovery or make the operator unable to state which firmware is really running.

## The controls I would require before accepting this state

- inspect the actual partition table before migration
- keep NVS unless migration explicitly requires change
- enable first-boot rollback state
- version persistent schemas
- test rollback after migration, not only upgrade

The point is not to maximize checklist length. Each control closes a different ambiguity that appeared in the real work. For this case, the shortcut I reject is **Shipping code that attempts to OTA itself into a layout that has no inactive OTA slot.**. If that shortcut is allowed, the release can look successful while the underlying recovery or provenance guarantee is false.

I prefer a release gate that fails loudly and leaves the old artifact usable. That is why full-flash erasure, force-pushing golden tags, disabling certificate verification, or widening a rollout to compensate for unclear state are all wrong directions. They destroy evidence or increase blast radius exactly when uncertainty is highest.

## What changes when the fleet grows

On one board, I can recover with USB and inspect serial output manually. At five or twenty devices, release identity, assignment and rollback have to be queryable. At a larger production fleet, I would tighten the same model rather than replace it: hardware-backed key provisioning, Secure Boot v2 and Flash Encryption under a controlled ceremony, more formal signing custody, staged rollout cohorts, automated rollback evidence, schema-compatibility tests and independent release audit records.

The important thing is that scale does not remove the original invariant. Freeze production partition architecture early and treat layout migrations as service-mode operations. A larger fleet only makes violations more expensive.

I would also keep service-mode releases separate from normal app OTA. Partition-table, bootloader and security-epoch transitions deserve a dedicated recovery plan because they modify the machinery that normal OTA depends on. That separation is useful at ten devices and essential at ten thousand.

## The lesson I keep

The result I keep from this case is: **Partition-generation changes were separated from normal application releases.**

The deeper lesson is **Freeze production partition architecture early and treat layout migrations as service-mode operations.**

That is how I now define production firmware work. The release is not the moment a `.bin` file appears. It is the chain that connects source, artifact, signature, compatibility, flash topology, persistent state, real-device acceptance and observable running state—with a rollback path whose assumptions have actually been tested.
