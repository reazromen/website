---
title: The Firmware Signing Private Key Does Not Belong on the OTA Server
url: /posts/firmware-release-signing-private-key-does-not-belong-on-ota-server.html
date: '2026-09-15'
read_time: 9
excerpt: If the same runtime host that stores and serves firmware also holds the signing
  private key, compromise of that host can become compromise of release authority.
topic: firmware-release-engineering
tags:
- esp32-s3
- firmware-release-engineering
- loup
draft: false
featured: false
language: en
eyebrow: 'Production Firmware: Signed OTA & Device Trust · deep-dive'
outputs:
- url: /posts/firmware-release-signing-private-key-does-not-belong-on-ota-server.html
  template: cms/templates/posts/posts--firmware-release-signing-private-key-does-not-belong-on-ota-server.tpl
  source: cms/templates/posts/posts--firmware-release-signing-private-key-does-not-belong-on-ota-server.json
---

# The Firmware Signing Private Key Does Not Belong on the OTA Server

The release-engineering problem became visible when if the same runtime host that stores and serves firmware also holds the signing private key, compromise of that host can become compromise of release authority.

The LOUP firmware path had a particularly unforgiving constraint: SIP/audio behavior already worked well enough to be valuable, so release work could not casually erase NVS, rewrite the flash layout, merge unrelated features or replace the rollback image. The goal was to make delivery safer without sacrificing the only known-good behavior.

For this article, the key evidence is specific: The production policy keeps the private key on the authorized operator machine while hserver and device firmware contain only the public verification key. The retained result was equally specific: Serving and verifying firmware no longer require the production signing secret to be resident on hserver. I treat both as observations from the documented release state, not as universal ESP32 rules.

## Case notebook

| Question | Recorded conclusion |
| --- | --- |
| Release problem | If the same runtime host that stores and serves firmware also holds the signing private key, compromise of that host can become compromise of release authority. |
| Evidence | The production policy keeps the private key on the authorized operator machine while hserver and device firmware contain only the public verification key. |
| Mechanism | Verification keys can be widely distributed; signing keys should be isolated because they authorize new executable code. |
| Rejected shortcut | Putting the private key into Git, a Docker secret on the OTA runtime, or an application environment variable for convenience. |
| Retained result | Serving and verifying firmware no longer require the production signing secret to be resident on hserver. |
| Rule carried forward | Separate artifact distribution authority from artifact signing authority. |

The table is intentionally stricter than a normal release note. A release note usually tells a reader what changed. This notebook also records what was *not* proven and which shortcut would have produced a misleading green status. That distinction mattered repeatedly in the LOUP work, especially while the golden V132A artifact, reconstructed source tree, V133A feature branch and later OTA control plane existed at different maturity levels.

## The OTA trust chain has several independent links

HTTPS authenticates the transport endpoint and protects the connection. A SHA-256 digest detects content mismatch. An ECDSA signature proves that an authorized signing key approved the artifact. Compatibility metadata prevents a correctly signed artifact from being sent to the wrong hardware or persistent-state generation. Bootloader security can later enforce additional device-local policy.

Those controls should stay separate in both implementation and incident response. If a checksum mismatches, I investigate corruption or artifact substitution. If the signature fails, I investigate release authorization or key mismatch. If compatibility fails, the artifact may be perfectly authentic but still unsafe for that device. If TLS fails, I do not bypass verification just because the signature exists.

Key custody is part of the same architecture. The private key authorizes executable code, so the runtime OTA server does not need it merely to serve and verify releases. Keeping signing authority off the distribution host limits the consequence of one class of server compromise.

## A concrete scenario I use to test the rule

Putting the private key on the OTA host would make a distribution-system compromise much more powerful. The host needs to verify and serve; it does not need to mint new authority.

For this article, the scenario is useful because it targets the rejected shortcut directly: **Putting the private key into Git, a Docker secret on the OTA runtime, or an application environment variable for convenience.**. I want the system to make that shortcut either impossible or obviously non-compliant with the release gate.

The falsification question is equally important. If a future implementation can demonstrate the same safety property with a simpler mechanism, I would change the mechanism. What I would not change casually is the invariant: **Separate artifact distribution authority from artifact signing authority.**. The release process exists to preserve that invariant while the implementation evolves.

## The mechanism underneath the release decision

OTA is remote code execution by design, so release authority is part of the threat model. TLS, checksums, signatures, compatibility metadata and irreversible eFuse policy solve different problems. I avoid using one of those controls as a substitute for the others.

For **The Firmware Signing Private Key Does Not Belong on the OTA Server**, the important mechanism is this: Verification keys can be widely distributed; signing keys should be isolated because they authorize new executable code.

That mechanism tells me which evidence is relevant. If the question is artifact identity, a call test alone is not enough; I need a hash and source identity. If the question is rollback, a signature alone is not enough; I need partition and persistent-schema compatibility. If the question is promotion, a CI pass is not enough; I need observed device state tied to the same release ID.

```
operator machine:
  artifact -> SHA-256 -> ECDSA P-256 signature
                     private key stays here

OTA server:
  stores artifact + detached signature + public verification metadata

device:
  verifies assigned artifact before accepting it
```

Integrity, authorization and transport trust remain distinct layers.

I use this model to stop release engineering from becoming a sequence of shell commands. The commands are implementation. The release contract is the set of invariants that must still be true when the commands finish.

## How I would try to break this before trusting it

Release safety is difficult to prove with only the happy path. For this class of change I want at least one test that intentionally violates the assumption the release depends on.

For **The Firmware Signing Private Key Does Not Belong on the OTA Server**, I would construct a negative test around the mechanism: Verification keys can be widely distributed; signing keys should be isolated because they authorize new executable code. That might mean removing a required source file from the clean checkout, presenting a wrong signature, assigning a release to the wrong hardware revision, forcing first-boot self-test failure, rolling back after a schema migration, or replaying a terminal OTA result for an older release ID.

The expected behavior should be boring: reject the artifact or assignment, keep/restore the previous accepted image, preserve persistent state where promised, and surface an attributable failure state. A test is especially valuable when it proves the system does *not* accept a dangerous shortcut.

This is why I distinguish recoverability tests from build tests. A compiler can prove syntax and linking. It cannot prove that a power interruption during slot write, a bad first boot or a stale heartbeat result leaves the fleet in a state the operator can understand.

## What this costs

The stricter release model adds work. Hashes, manifests, detached signatures, isolated builds, compatibility metadata, dual slots, schema versions and promotion gates all create operational surface area. On a small product team that overhead can feel disproportionate to one ESP32-S3 binary.

The alternative cost is hidden. Without these controls, a good audio artifact can be overwritten, a feature branch can silently become the new baseline, an old image can be unable to read migrated NVS, a runtime server compromise can become signing compromise, or the fleet can report “failed” for the wrong release because one stale result had no causal identity.

For this case the retained rule is **Separate artifact distribution authority from artifact signing authority.**. I accept the additional release machinery when it closes a failure mode that would otherwise require physical recovery or make the operator unable to state which firmware is really running.

## The controls I would require before accepting this state

- verify TLS without insecure fallback
- verify SHA-256 content identity
- verify detached release signature
- keep private signing material off the runtime host
- validate model/hardware/partition/schema compatibility

The point is not to maximize checklist length. Each control closes a different ambiguity that appeared in the real work. For this case, the shortcut I reject is **Putting the private key into Git, a Docker secret on the OTA runtime, or an application environment variable for convenience.**. If that shortcut is allowed, the release can look successful while the underlying recovery or provenance guarantee is false.

I prefer a release gate that fails loudly and leaves the old artifact usable. That is why full-flash erasure, force-pushing golden tags, disabling certificate verification, or widening a rollout to compensate for unclear state are all wrong directions. They destroy evidence or increase blast radius exactly when uncertainty is highest.

## What changes when the fleet grows

On one board, I can recover with USB and inspect serial output manually. At five or twenty devices, release identity, assignment and rollback have to be queryable. At a larger production fleet, I would tighten the same model rather than replace it: hardware-backed key provisioning, Secure Boot v2 and Flash Encryption under a controlled ceremony, more formal signing custody, staged rollout cohorts, automated rollback evidence, schema-compatibility tests and independent release audit records.

The important thing is that scale does not remove the original invariant. Separate artifact distribution authority from artifact signing authority. A larger fleet only makes violations more expensive.

I would also keep service-mode releases separate from normal app OTA. Partition-table, bootloader and security-epoch transitions deserve a dedicated recovery plan because they modify the machinery that normal OTA depends on. That separation is useful at ten devices and essential at ten thousand.

## The lesson I keep

The result I keep from this case is: **Serving and verifying firmware no longer require the production signing secret to be resident on hserver.**

The deeper lesson is **Separate artifact distribution authority from artifact signing authority.**

That is how I now define production firmware work. The release is not the moment a `.bin` file appears. It is the chain that connects source, artifact, signature, compatibility, flash topology, persistent state, real-device acceptance and observable running state—with a rollback path whose assumptions have actually been tested.
