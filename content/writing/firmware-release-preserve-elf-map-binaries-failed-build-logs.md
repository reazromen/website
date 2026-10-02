---
title: Why I Preserve ELF, MAP, Binaries and Failed Build Logs
url: /posts/firmware-release-preserve-elf-map-binaries-failed-build-logs.html
date: '2026-09-15'
read_time: 9
excerpt: Build artifacts that looked obsolete became the only evidence for reconstructing
  which toolchain, sections and symbols belonged to an earlier working or failing
  state.
topic: firmware-release-engineering
tags:
- esp32-s3
- firmware-release-engineering
- loup
draft: false
featured: false
language: en
eyebrow: 'Production Firmware: Golden Artifacts & Identity · deep-dive'
outputs:
- url: /posts/firmware-release-preserve-elf-map-binaries-failed-build-logs.html
  template: cms/templates/posts/posts--firmware-release-preserve-elf-map-binaries-failed-build-logs.tpl
  source: cms/templates/posts/posts--firmware-release-preserve-elf-map-binaries-failed-build-logs.json
---

# Why I Preserve ELF, MAP, Binaries and Failed Build Logs

A working ESP32-S3 build is easy to over-trust. In this case, build artifacts that looked obsolete became the only evidence for reconstructing which toolchain, sections and symbols belonged to an earlier working or failing state.

The LOUP firmware path had a particularly unforgiving constraint: SIP/audio behavior already worked well enough to be valuable, so release work could not casually erase NVS, rewrite the flash layout, merge unrelated features or replace the rollback image. The goal was to make delivery safer without sacrificing the only known-good behavior.

For this article, the key evidence is specific: The recovery rules explicitly prohibited deleting successful build directories, ELF files, map files, binaries and failed build logs because they were forensic evidence. The retained result was equally specific: Historical artifacts remained available to distinguish build-system problems from runtime regressions. I treat both as observations from the documented release state, not as universal ESP32 rules.

## Case notebook

| Question | Recorded conclusion |
| --- | --- |
| Release problem | Build artifacts that looked obsolete became the only evidence for reconstructing which toolchain, sections and symbols belonged to an earlier working or failing state. |
| Evidence | The recovery rules explicitly prohibited deleting successful build directories, ELF files, map files, binaries and failed build logs because they were forensic evidence. |
| Mechanism | Release engineering is partly incident forensics: linker maps explain partition fit, ELF metadata ties symbols to an image, and failed logs preserve dependency or configuration faults. |
| Rejected shortcut | Cleaning the workspace aggressively once a newer build exists. |
| Retained result | Historical artifacts remained available to distinguish build-system problems from runtime regressions. |
| Rule carried forward | Delete build debris only after deciding whether it is evidence. |

The table is intentionally stricter than a normal release note. A release note usually tells a reader what changed. This notebook also records what was *not* proven and which shortcut would have produced a misleading green status. That distinction mattered repeatedly in the LOUP work, especially while the golden V132A artifact, reconstructed source tree, V133A feature branch and later OTA control plane existed at different maturity levels.

## Artifact identity is a multi-key problem

For a production firmware artifact I want enough information to distinguish four questions that are often collapsed: What bytes are on the device? What source state was intended to produce them? Which toolchain/dependencies produced the candidate? Which physical test proved the behavior? A binary SHA answers only the first. A Git commit answers only part of the second. A successful call answers the last but does not reconstruct source provenance.

That is why the golden-image workflow preserved exact application bytes separately from source cleanup. The golden artifact could remain the rollback authority even while the repository was being repaired. This is not an admission that reproducibility does not matter; it is a way to avoid destroying the only trusted executable while reproducibility is being established.

In a larger release system I would store this relationship explicitly rather than in filenames: artifact digest, source commit, build environment identity, hardware compatibility, signer key ID and acceptance record. The operational rule is that none of those fields silently substitutes for another.

## A concrete scenario I use to test the rule

A linker map from a failed build can later explain why a candidate no longer fits the partition or which component changed section size. I keep it because forensic value appears after the failure, not before.

For this article, the scenario is useful because it targets the rejected shortcut directly: **Cleaning the workspace aggressively once a newer build exists.**. I want the system to make that shortcut either impossible or obviously non-compliant with the release gate.

The falsification question is equally important. If a future implementation can demonstrate the same safety property with a simpler mechanism, I would change the mechanism. What I would not change casually is the invariant: **Delete build debris only after deciding whether it is evidence.**. The release process exists to preserve that invariant while the implementation evolves.

## The mechanism underneath the release decision

The first release problem was preservation. A voice build that users trusted was more valuable than a prettier repository if the repository could not yet prove it produced the same behavior. I therefore separate the golden binary, source provenance, hardware context and test evidence. That lets source recovery move forward without rewriting the operational truth that already exists on the device.

For **Why I Preserve ELF, MAP, Binaries and Failed Build Logs**, the important mechanism is this: Release engineering is partly incident forensics: linker maps explain partition fit, ELF metadata ties symbols to an image, and failed logs preserve dependency or configuration faults.

That mechanism tells me which evidence is relevant. If the question is artifact identity, a call test alone is not enough; I need a hash and source identity. If the question is rollback, a signature alone is not enough; I need partition and persistent-schema compatibility. If the question is promotion, a CI pass is not enough; I need observed device state tied to the same release ID.

```
release_identity = {
  binary_sha256,
  git_commit,
  hardware_revision,
  flash_offset,
  toolchain_identity,
  acceptance_evidence
}
```

A version string is metadata inside this record, not the primary key for truth.

I use this model to stop release engineering from becoming a sequence of shell commands. The commands are implementation. The release contract is the set of invariants that must still be true when the commands finish.

## How I would try to break this before trusting it

Release safety is difficult to prove with only the happy path. For this class of change I want at least one test that intentionally violates the assumption the release depends on.

For **Why I Preserve ELF, MAP, Binaries and Failed Build Logs**, I would construct a negative test around the mechanism: Release engineering is partly incident forensics: linker maps explain partition fit, ELF metadata ties symbols to an image, and failed logs preserve dependency or configuration faults. That might mean removing a required source file from the clean checkout, presenting a wrong signature, assigning a release to the wrong hardware revision, forcing first-boot self-test failure, rolling back after a schema migration, or replaying a terminal OTA result for an older release ID.

The expected behavior should be boring: reject the artifact or assignment, keep/restore the previous accepted image, preserve persistent state where promised, and surface an attributable failure state. A test is especially valuable when it proves the system does *not* accept a dangerous shortcut.

This is why I distinguish recoverability tests from build tests. A compiler can prove syntax and linking. It cannot prove that a power interruption during slot write, a bad first boot or a stale heartbeat result leaves the fleet in a state the operator can understand.

## What this costs

The stricter release model adds work. Hashes, manifests, detached signatures, isolated builds, compatibility metadata, dual slots, schema versions and promotion gates all create operational surface area. On a small product team that overhead can feel disproportionate to one ESP32-S3 binary.

The alternative cost is hidden. Without these controls, a good audio artifact can be overwritten, a feature branch can silently become the new baseline, an old image can be unable to read migrated NVS, a runtime server compromise can become signing compromise, or the fleet can report “failed” for the wrong release because one stale result had no causal identity.

For this case the retained rule is **Delete build debris only after deciding whether it is evidence.**. I accept the additional release machinery when it closes a failure mode that would otherwise require physical recovery or make the operator unable to state which firmware is really running.

## The controls I would require before accepting this state

- read back and hash the known-good application image
- record flash offset and image metadata
- pin the source commit separately from the binary hash
- keep golden tags immutable
- store acceptance notes beside the artifact

The point is not to maximize checklist length. Each control closes a different ambiguity that appeared in the real work. For this case, the shortcut I reject is **Cleaning the workspace aggressively once a newer build exists.**. If that shortcut is allowed, the release can look successful while the underlying recovery or provenance guarantee is false.

I prefer a release gate that fails loudly and leaves the old artifact usable. That is why full-flash erasure, force-pushing golden tags, disabling certificate verification, or widening a rollout to compensate for unclear state are all wrong directions. They destroy evidence or increase blast radius exactly when uncertainty is highest.

## What this costs

The stricter release model adds work. Hashes, manifests, detached signatures, isolated builds, compatibility metadata, dual slots, schema versions and promotion gates all create operational surface area. On a small product team that overhead can feel disproportionate to one ESP32-S3 binary.

The alternative cost is hidden. Without these controls, a good audio artifact can be overwritten, a feature branch can silently become the new baseline, an old image can be unable to read migrated NVS, a runtime server compromise can become signing compromise, or the fleet can report “failed” for the wrong release because one stale result had no causal identity.

For this case the retained rule is **Delete build debris only after deciding whether it is evidence.**. I accept the additional release machinery when it closes a failure mode that would otherwise require physical recovery or make the operator unable to state which firmware is really running.

## The lesson I keep

The result I keep from this case is: **Historical artifacts remained available to distinguish build-system problems from runtime regressions.**

The deeper lesson is **Delete build debris only after deciding whether it is evidence.**

That is how I now define production firmware work. The release is not the moment a `.bin` file appears. It is the chain that connects source, artifact, signature, compatibility, flash topology, persistent state, real-device acceptance and observable running state—with a rollback path whose assumptions have actually been tested.
