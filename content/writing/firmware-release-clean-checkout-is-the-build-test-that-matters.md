---
title: A Clean Checkout Is the Build Test That Matters
url: /posts/firmware-release-clean-checkout-is-the-build-test-that-matters.html
date: '2020-12-23'
read_time: 9
excerpt: A firmware tree can build for months on one workstation while quietly depending
  on files that are not in the repository.
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
- url: /posts/firmware-release-clean-checkout-is-the-build-test-that-matters.html
  template: cms/templates/posts/posts--firmware-release-clean-checkout-is-the-build-test-that-matters.tpl
  source: cms/templates/posts/posts--firmware-release-clean-checkout-is-the-build-test-that-matters.json
---

# A Clean Checkout Is the Build Test That Matters

The release-engineering problem became visible when a firmware tree can build for months on one workstation while quietly depending on files that are not in the repository.

The LOUP firmware path had a particularly unforgiving constraint: SIP/audio behavior already worked well enough to be valuable, so release work could not casually erase NVS, rewrite the flash layout, merge unrelated features or replace the rollback image. The goal was to make delivery safer without sacrificing the only known-good behavior.

For this article, the key evidence is specific: The repository acceptance gate required a fresh isolated export or clone, a new build directory, zero undefined references, a valid ESP32-S3 image, partition fit and recorded toolchain/dependency identity. The retained result was equally specific: Reproducibility became a release gate rather than a developer assumption. I treat both as observations from the documented release state, not as universal ESP32 rules.

## Case notebook

| Question | Recorded conclusion |
| --- | --- |
| Release problem | A firmware tree can build for months on one workstation while quietly depending on files that are not in the repository. |
| Evidence | The repository acceptance gate required a fresh isolated export or clone, a new build directory, zero undefined references, a valid ESP32-S3 image, partition fit and recorded toolchain/dependency identity. |
| Mechanism | Incremental builds preserve local state; a clean checkout removes accidental dependency on old objects, neighboring source trees and machine-specific paths. |
| Rejected shortcut | Treating idf.py build in the long-lived development directory as proof of reproducibility. |
| Retained result | Reproducibility became a release gate rather than a developer assumption. |
| Rule carried forward | The release candidate must build where stale local state cannot rescue it. |

The table is intentionally stricter than a normal release note. A release note usually tells a reader what changed. This notebook also records what was *not* proven and which shortcut would have produced a misleading green status. That distinction mattered repeatedly in the LOUP work, especially while the golden V132A artifact, reconstructed source tree, V133A feature branch and later OTA control plane existed at different maturity levels.

## Reproducibility needs an adversarial build environment

A reproducibility test should remove conveniences. It should not run inside the same directory tree that has years of old headers, generated files and component caches arranged exactly as the developer expects. It should clone or export the chosen commit into an unrelated path, use a fresh build directory and fail if the source tree reaches outside itself.

I also care about the delivery boundary. The recipient receives an archive or Git checkout, not my workstation filesystem. So I treat “extract package somewhere unrelated and rebuild it” as a separate test. That catches ignored files, absolute paths, missing embedded assets, undocumented environment variables and local component assumptions that a normal incremental build hides.

A build that fails under this test is useful evidence. It tells me the repository contract is incomplete before the failure becomes somebody else’s integration problem.

## A concrete scenario I use to test the rule

My favorite reproducibility test is to move the build far enough away that old relative paths cannot accidentally succeed. If a source reference escapes the repository, I want it to fail immediately rather than resolve into some forgotten directory.

For this article, the scenario is useful because it targets the rejected shortcut directly: **Treating idf.py build in the long-lived development directory as proof of reproducibility.**. I want the system to make that shortcut either impossible or obviously non-compliant with the release gate.

The falsification question is equally important. If a future implementation can demonstrate the same safety property with a simpler mechanism, I would change the mechanism. What I would not change casually is the invariant: **The release candidate must build where stale local state cannot rescue it.**. The release process exists to preserve that invariant while the implementation evolves.

## The mechanism underneath the release decision

Reproducibility is a hostile-environment test. I want the release to fail when it depends on a neighboring checkout, ignored generated file, stale object or workstation-specific path. A fresh isolated build is useful precisely because it removes the accidental help of the developer machine. The package the next engineer receives must survive the same test.

For **A Clean Checkout Is the Build Test That Matters**, the important mechanism is this: Incremental builds preserve local state; a clean checkout removes accidental dependency on old objects, neighboring source trees and machine-specific paths.

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

## How I would try to break this before trusting it

Release safety is difficult to prove with only the happy path. For this class of change I want at least one test that intentionally violates the assumption the release depends on.

For **A Clean Checkout Is the Build Test That Matters**, I would construct a negative test around the mechanism: Incremental builds preserve local state; a clean checkout removes accidental dependency on old objects, neighboring source trees and machine-specific paths. That might mean removing a required source file from the clean checkout, presenting a wrong signature, assigning a release to the wrong hardware revision, forcing first-boot self-test failure, rolling back after a schema migration, or replaying a terminal OTA result for an older release ID.

The expected behavior should be boring: reject the artifact or assignment, keep/restore the previous accepted image, preserve persistent state where promised, and surface an attributable failure state. A test is especially valuable when it proves the system does *not* accept a dangerous shortcut.

This is why I distinguish recoverability tests from build tests. A compiler can prove syntax and linking. It cannot prove that a power interruption during slot write, a bad first boot or a stale heartbeat result leaves the fleet in a state the operator can understand.

## What this costs

The stricter release model adds work. Hashes, manifests, detached signatures, isolated builds, compatibility metadata, dual slots, schema versions and promotion gates all create operational surface area. On a small product team that overhead can feel disproportionate to one ESP32-S3 binary.

The alternative cost is hidden. Without these controls, a good audio artifact can be overwritten, a feature branch can silently become the new baseline, an old image can be unable to read migrated NVS, a runtime server compromise can become signing compromise, or the fleet can report “failed” for the wrong release because one stale result had no causal identity.

For this case the retained rule is **The release candidate must build where stale local state cannot rescue it.**. I accept the additional release machinery when it closes a failure mode that would otherwise require physical recovery or make the operator unable to state which firmware is really running.

## The controls I would require before accepting this state

- clone/export into an unrelated path
- build in a fresh directory
- reject source/include paths escaping the repository
- validate image metadata and partition fit
- rebuild the delivery archive after extraction

The point is not to maximize checklist length. Each control closes a different ambiguity that appeared in the real work. For this case, the shortcut I reject is **Treating idf.py build in the long-lived development directory as proof of reproducibility.**. If that shortcut is allowed, the release can look successful while the underlying recovery or provenance guarantee is false.

I prefer a release gate that fails loudly and leaves the old artifact usable. That is why full-flash erasure, force-pushing golden tags, disabling certificate verification, or widening a rollout to compensate for unclear state are all wrong directions. They destroy evidence or increase blast radius exactly when uncertainty is highest.

## What this costs

The stricter release model adds work. Hashes, manifests, detached signatures, isolated builds, compatibility metadata, dual slots, schema versions and promotion gates all create operational surface area. On a small product team that overhead can feel disproportionate to one ESP32-S3 binary.

The alternative cost is hidden. Without these controls, a good audio artifact can be overwritten, a feature branch can silently become the new baseline, an old image can be unable to read migrated NVS, a runtime server compromise can become signing compromise, or the fleet can report “failed” for the wrong release because one stale result had no causal identity.

For this case the retained rule is **The release candidate must build where stale local state cannot rescue it.**. I accept the additional release machinery when it closes a failure mode that would otherwise require physical recovery or make the operator unable to state which firmware is really running.

## The lesson I keep

The result I keep from this case is: **Reproducibility became a release gate rather than a developer assumption.**

The deeper lesson is **The release candidate must build where stale local state cannot rescue it.**

That is how I now define production firmware work. The release is not the moment a `.bin` file appears. It is the chain that connects source, artifact, signature, compatibility, flash topology, persistent state, real-device acceptance and observable running state—with a rollback path whose assumptions have actually been tested.
