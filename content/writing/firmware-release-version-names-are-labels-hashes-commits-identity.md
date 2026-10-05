---
title: Version Names Are Labels; Hashes and Commits Are Identity
url: /posts/firmware-release-version-names-are-labels-hashes-commits-identity.html
date: '2021-09-24'
read_time: 9
excerpt: Names such as V132A and V133A were convenient in conversation but too weak
  to prove which bytes or source tree were actually under test.
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
- url: /posts/firmware-release-version-names-are-labels-hashes-commits-identity.html
  template: cms/templates/posts/posts--firmware-release-version-names-are-labels-hashes-commits-identity.tpl
  source: cms/templates/posts/posts--firmware-release-version-names-are-labels-hashes-commits-identity.json
---

# Version Names Are Labels; Hashes and Commits Are Identity

This part of the LOUP firmware work was less about adding code than deciding what I was allowed to call a release. Names such as V132A and V133A were convenient in conversation but too weak to prove which bytes or source tree were actually under test.

The LOUP firmware path had a particularly unforgiving constraint: SIP/audio behavior already worked well enough to be valuable, so release work could not casually erase NVS, rewrite the flash layout, merge unrelated features or replace the rollback image. The goal was to make delivery safer without sacrificing the only known-good behavior.

For this article, the key evidence is specific: The handoff required exact Git commit IDs and SHA-256 values and explicitly said version names alone were insufficient identity. The retained result was equally specific: The release process could compare a device artifact, Git state and delivery package without relying on memory. I treat both as observations from the documented release state, not as universal ESP32 rules.

## Case notebook

| Question | Recorded conclusion |
| --- | --- |
| Release problem | Names such as V132A and V133A were convenient in conversation but too weak to prove which bytes or source tree were actually under test. |
| Evidence | The handoff required exact Git commit IDs and SHA-256 values and explicitly said version names alone were insufficient identity. |
| Mechanism | Human-readable versions describe intent; cryptographic hashes and immutable commits bind that intent to concrete content. |
| Rejected shortcut | Using a filename or marketing version as the only evidence in a regression report. |
| Retained result | The release process could compare a device artifact, Git state and delivery package without relying on memory. |
| Rule carried forward | Every acceptance result should point to immutable content identity. |

The table is intentionally stricter than a normal release note. A release note usually tells a reader what changed. This notebook also records what was *not* proven and which shortcut would have produced a misleading green status. That distinction mattered repeatedly in the LOUP work, especially while the golden V132A artifact, reconstructed source tree, V133A feature branch and later OTA control plane existed at different maturity levels.

## Artifact identity is a multi-key problem

For a production firmware artifact I want enough information to distinguish four questions that are often collapsed: What bytes are on the device? What source state was intended to produce them? Which toolchain/dependencies produced the candidate? Which physical test proved the behavior? A binary SHA answers only the first. A Git commit answers only part of the second. A successful call answers the last but does not reconstruct source provenance.

That is why the golden-image workflow preserved exact application bytes separately from source cleanup. The golden artifact could remain the rollback authority even while the repository was being repaired. This is not an admission that reproducibility does not matter; it is a way to avoid destroying the only trusted executable while reproducibility is being established.

In a larger release system I would store this relationship explicitly rather than in filenames: artifact digest, source commit, build environment identity, hardware compatibility, signer key ID and acceptance record. The operational rule is that none of those fields silently substitutes for another.

## A concrete scenario I use to test the rule

The practical reason for hashes is not cryptographic elegance. It is avoiding the sentence “I think this is the same binary.” A release process should make that sentence unnecessary.

For this article, the scenario is useful because it targets the rejected shortcut directly: **Using a filename or marketing version as the only evidence in a regression report.**. I want the system to make that shortcut either impossible or obviously non-compliant with the release gate.

The falsification question is equally important. If a future implementation can demonstrate the same safety property with a simpler mechanism, I would change the mechanism. What I would not change casually is the invariant: **Every acceptance result should point to immutable content identity.**. The release process exists to preserve that invariant while the implementation evolves.

## The mechanism underneath the release decision

The first release problem was preservation. A voice build that users trusted was more valuable than a prettier repository if the repository could not yet prove it produced the same behavior. I therefore separate the golden binary, source provenance, hardware context and test evidence. That lets source recovery move forward without rewriting the operational truth that already exists on the device.

For **Version Names Are Labels; Hashes and Commits Are Identity**, the important mechanism is this: Human-readable versions describe intent; cryptographic hashes and immutable commits bind that intent to concrete content.

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

## The controls I would require before accepting this state

- read back and hash the known-good application image
- record flash offset and image metadata
- pin the source commit separately from the binary hash
- keep golden tags immutable
- store acceptance notes beside the artifact

The point is not to maximize checklist length. Each control closes a different ambiguity that appeared in the real work. For this case, the shortcut I reject is **Using a filename or marketing version as the only evidence in a regression report.**. If that shortcut is allowed, the release can look successful while the underlying recovery or provenance guarantee is false.

I prefer a release gate that fails loudly and leaves the old artifact usable. That is why full-flash erasure, force-pushing golden tags, disabling certificate verification, or widening a rollout to compensate for unclear state are all wrong directions. They destroy evidence or increase blast radius exactly when uncertainty is highest.

## How I would try to break this before trusting it

Release safety is difficult to prove with only the happy path. For this class of change I want at least one test that intentionally violates the assumption the release depends on.

For **Version Names Are Labels; Hashes and Commits Are Identity**, I would construct a negative test around the mechanism: Human-readable versions describe intent; cryptographic hashes and immutable commits bind that intent to concrete content. That might mean removing a required source file from the clean checkout, presenting a wrong signature, assigning a release to the wrong hardware revision, forcing first-boot self-test failure, rolling back after a schema migration, or replaying a terminal OTA result for an older release ID.

The expected behavior should be boring: reject the artifact or assignment, keep/restore the previous accepted image, preserve persistent state where promised, and surface an attributable failure state. A test is especially valuable when it proves the system does *not* accept a dangerous shortcut.

This is why I distinguish recoverability tests from build tests. A compiler can prove syntax and linking. It cannot prove that a power interruption during slot write, a bad first boot or a stale heartbeat result leaves the fleet in a state the operator can understand.

## Keep chronology honest

The V132A/V133A recovery documents are useful because they did not retroactively turn incomplete work into completed work. At the August handoff, the golden V132A rollback binary was proven, while the V133A feature branch had source work that still needed clean-build, flash, physical power and clear-audio regression evidence. Later fleet/OTA work added a different layer of production acceptance.

That chronology matters for this topic because **The release process could compare a device artifact, Git state and delivery package without relying on memory.** should be read as the result of the evidence chain that actually existed at that stage. I do not use a later production capability to rewrite an earlier handoff as if it had already passed.

This is also how I want release dashboards and articles to behave. A state such as `built`, `signed`, `assigned`, `booted`, `accepted`, `active` or `stable` should mean one thing and be backed by the evidence required for that state. The system becomes hard to operate when success words float free of their acceptance gates.

## What this costs

The stricter release model adds work. Hashes, manifests, detached signatures, isolated builds, compatibility metadata, dual slots, schema versions and promotion gates all create operational surface area. On a small product team that overhead can feel disproportionate to one ESP32-S3 binary.

The alternative cost is hidden. Without these controls, a good audio artifact can be overwritten, a feature branch can silently become the new baseline, an old image can be unable to read migrated NVS, a runtime server compromise can become signing compromise, or the fleet can report “failed” for the wrong release because one stale result had no causal identity.

For this case the retained rule is **Every acceptance result should point to immutable content identity.**. I accept the additional release machinery when it closes a failure mode that would otherwise require physical recovery or make the operator unable to state which firmware is really running.

## The lesson I keep

The result I keep from this case is: **The release process could compare a device artifact, Git state and delivery package without relying on memory.**

The deeper lesson is **Every acceptance result should point to immutable content identity.**

That is how I now define production firmware work. The release is not the moment a `.bin` file appears. It is the chain that connects source, artifact, signature, compatibility, flash topology, persistent state, real-device acceptance and observable running state—with a rollback path whose assumptions have actually been tested.
