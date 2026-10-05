---
title: I Validate an ESP32-S3 Image Before I Let It Touch the Phone
url: /posts/firmware-release-validate-esp32s3-image-before-flash.html
date: '2025-12-10'
read_time: 9
excerpt: A successful linker exit does not prove the produced file is the intended
  target image or that its metadata/checksum are sane.
topic: firmware-release-engineering
tags:
- esp32-s3
- firmware-release-engineering
- loup
draft: false
featured: false
language: en
eyebrow: 'Production Firmware: Reproducible Builds & Source Integrity · deep-dive'
outputs:
- url: /posts/firmware-release-validate-esp32s3-image-before-flash.html
  template: cms/templates/posts/posts--firmware-release-validate-esp32s3-image-before-flash.tpl
  source: cms/templates/posts/posts--firmware-release-validate-esp32s3-image-before-flash.json
---

# I Validate an ESP32-S3 Image Before I Let It Touch the Phone

I used to think a firmware release was the binary produced after a successful build. A successful linker exit does not prove the produced file is the intended target image or that its metadata/checksum are sane.

The LOUP firmware path had a particularly unforgiving constraint: SIP/audio behavior already worked well enough to be valuable, so release work could not casually erase NVS, rewrite the flash layout, merge unrelated features or replace the rollback image. The goal was to make delivery safer without sacrificing the only known-good behavior.

For this article, the key evidence is specific: The clean-build gate required esptool image-info to identify an ESP32-S3 application with valid checksum/validation data and required the binary to fit the configured application partition before flashing. The retained result was equally specific: Flashing became downstream of image validation rather than a way to discover build mistakes on the device. I treat both as observations from the documented release state, not as universal ESP32 rules.

## Case notebook

| Question | Recorded conclusion |
| --- | --- |
| Release problem | A successful linker exit does not prove the produced file is the intended target image or that its metadata/checksum are sane. |
| Evidence | The clean-build gate required esptool image-info to identify an ESP32-S3 application with valid checksum/validation data and required the binary to fit the configured application partition before flashing. |
| Mechanism | Build success, image-format validity and flash-layout compatibility are separate acceptance layers. |
| Rejected shortcut | Treating the existence of voip\_app.bin as sufficient flash authorization. |
| Retained result | Flashing became downstream of image validation rather than a way to discover build mistakes on the device. |
| Rule carried forward | Validate cheap static properties before risking persistent device state. |

The table is intentionally stricter than a normal release note. A release note usually tells a reader what changed. This notebook also records what was *not* proven and which shortcut would have produced a misleading green status. That distinction mattered repeatedly in the LOUP work, especially while the golden V132A artifact, reconstructed source tree, V133A feature branch and later OTA control plane existed at different maturity levels.

## Reproducibility needs an adversarial build environment

A reproducibility test should remove conveniences. It should not run inside the same directory tree that has years of old headers, generated files and component caches arranged exactly as the developer expects. It should clone or export the chosen commit into an unrelated path, use a fresh build directory and fail if the source tree reaches outside itself.

I also care about the delivery boundary. The recipient receives an archive or Git checkout, not my workstation filesystem. So I treat “extract package somewhere unrelated and rebuild it” as a separate test. That catches ignored files, absolute paths, missing embedded assets, undocumented environment variables and local component assumptions that a normal incremental build hides.

A build that fails under this test is useful evidence. It tells me the repository contract is incomplete before the failure becomes somebody else’s integration problem.

## A concrete scenario I use to test the rule

I use image-info because the device should not be the first parser to tell me that a candidate is malformed or for the wrong target. Cheap static validation belongs before flash.

For this article, the scenario is useful because it targets the rejected shortcut directly: **Treating the existence of voip\_app.bin as sufficient flash authorization.**. I want the system to make that shortcut either impossible or obviously non-compliant with the release gate.

The falsification question is equally important. If a future implementation can demonstrate the same safety property with a simpler mechanism, I would change the mechanism. What I would not change casually is the invariant: **Validate cheap static properties before risking persistent device state.**. The release process exists to preserve that invariant while the implementation evolves.

## The mechanism underneath the release decision

Reproducibility is a hostile-environment test. I want the release to fail when it depends on a neighboring checkout, ignored generated file, stale object or workstation-specific path. A fresh isolated build is useful precisely because it removes the accidental help of the developer machine. The package the next engineer receives must survive the same test.

For **I Validate an ESP32-S3 Image Before I Let It Touch the Phone**, the important mechanism is this: Build success, image-format validity and flash-layout compatibility are separate acceptance layers.

That mechanism tells me which evidence is relevant. If the question is artifact identity, a call test alone is not enough; I need a hash and source identity. If the question is rollback, a signature alone is not enough; I need partition and persistent-schema compatibility. If the question is promotion, a CI pass is not enough; I need observed device state tied to the same release ID.

```
fresh checkout/export
  -> no external source/include paths
  -> empty build directory
  -> configure + link
  -> image-info validation
  -> partition-fit check
  -> record commit/toolchain/dependencies
```

The purpose is to remove undeclared state, not merely to run the compiler again.

I use this model to stop release engineering from becoming a sequence of shell commands. The commands are implementation. The release contract is the set of invariants that must still be true when the commands finish.

## The controls I would require before accepting this state

- clone/export into an unrelated path
- build in a fresh directory
- reject source/include paths escaping the repository
- validate image metadata and partition fit
- rebuild the delivery archive after extraction

The point is not to maximize checklist length. Each control closes a different ambiguity that appeared in the real work. For this case, the shortcut I reject is **Treating the existence of voip\_app.bin as sufficient flash authorization.**. If that shortcut is allowed, the release can look successful while the underlying recovery or provenance guarantee is false.

I prefer a release gate that fails loudly and leaves the old artifact usable. That is why full-flash erasure, force-pushing golden tags, disabling certificate verification, or widening a rollout to compensate for unclear state are all wrong directions. They destroy evidence or increase blast radius exactly when uncertainty is highest.

## How I would try to break this before trusting it

Release safety is difficult to prove with only the happy path. For this class of change I want at least one test that intentionally violates the assumption the release depends on.

For **I Validate an ESP32-S3 Image Before I Let It Touch the Phone**, I would construct a negative test around the mechanism: Build success, image-format validity and flash-layout compatibility are separate acceptance layers. That might mean removing a required source file from the clean checkout, presenting a wrong signature, assigning a release to the wrong hardware revision, forcing first-boot self-test failure, rolling back after a schema migration, or replaying a terminal OTA result for an older release ID.

The expected behavior should be boring: reject the artifact or assignment, keep/restore the previous accepted image, preserve persistent state where promised, and surface an attributable failure state. A test is especially valuable when it proves the system does *not* accept a dangerous shortcut.

This is why I distinguish recoverability tests from build tests. A compiler can prove syntax and linking. It cannot prove that a power interruption during slot write, a bad first boot or a stale heartbeat result leaves the fleet in a state the operator can understand.

## Keep chronology honest

The V132A/V133A recovery documents are useful because they did not retroactively turn incomplete work into completed work. At the August handoff, the golden V132A rollback binary was proven, while the V133A feature branch had source work that still needed clean-build, flash, physical power and clear-audio regression evidence. Later fleet/OTA work added a different layer of production acceptance.

That chronology matters for this topic because **Flashing became downstream of image validation rather than a way to discover build mistakes on the device.** should be read as the result of the evidence chain that actually existed at that stage. I do not use a later production capability to rewrite an earlier handoff as if it had already passed.

This is also how I want release dashboards and articles to behave. A state such as `built`, `signed`, `assigned`, `booted`, `accepted`, `active` or `stable` should mean one thing and be backed by the evidence required for that state. The system becomes hard to operate when success words float free of their acceptance gates.

## What this costs

The stricter release model adds work. Hashes, manifests, detached signatures, isolated builds, compatibility metadata, dual slots, schema versions and promotion gates all create operational surface area. On a small product team that overhead can feel disproportionate to one ESP32-S3 binary.

The alternative cost is hidden. Without these controls, a good audio artifact can be overwritten, a feature branch can silently become the new baseline, an old image can be unable to read migrated NVS, a runtime server compromise can become signing compromise, or the fleet can report “failed” for the wrong release because one stale result had no causal identity.

For this case the retained rule is **Validate cheap static properties before risking persistent device state.**. I accept the additional release machinery when it closes a failure mode that would otherwise require physical recovery or make the operator unable to state which firmware is really running.

## The lesson I keep

The result I keep from this case is: **Flashing became downstream of image validation rather than a way to discover build mistakes on the device.**

The deeper lesson is **Validate cheap static properties before risking persistent device state.**

That is how I now define production firmware work. The release is not the moment a `.bin` file appears. It is the chain that connects source, artifact, signature, compatibility, flash topology, persistent state, real-device acceptance and observable running state—with a rollback path whose assumptions have actually been tested.
