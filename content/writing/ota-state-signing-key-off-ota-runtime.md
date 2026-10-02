---
title: The Signing Private Key Does Not Belong on the OTA Runtime Host
url: /posts/ota-state-signing-key-off-ota-runtime.html
date: '2026-09-15'
read_time: 8
excerpt: If the OTA server stored the production signing private key, compromise of
  the delivery plane could become authority to mint trusted firmware.
topic: production-ota-fleet
tags:
- ota
- esp32-s3
- fleet-management
- release-engineering
draft: false
featured: false
language: en
eyebrow: 'Production OTA: Compatibility & Trust · deep-dive'
outputs:
- url: /posts/ota-state-signing-key-off-ota-runtime.html
  template: cms/templates/posts/posts--ota-state-signing-key-off-ota-runtime.tpl
  source: cms/templates/posts/posts--ota-state-signing-key-off-ota-runtime.json
---

# The Signing Private Key Does Not Belong on the OTA Runtime Host

The OTA bug was not in the downloader. The real problem was that If the OTA server stored the production signing private key, compromise of the delivery plane could become authority to mint trusted firmware.

The system behind this series is LOUP's production-style OTA control plane: per-device identity, explicit release objects, compatibility metadata, assignment state, heartbeat observation, A/B application slots, signed artifacts, first-boot validation, append-only events and staged rollout. The point is not the exact API shape. It is the state discipline required when server, device and bootloader can each be correct locally while disagreeing about the fleet globally.

The evidence for this case was specific: **The migration policy keeps the P-256 private key on the authorized operator machine with mode 0600; hserver and devices receive only the public verification key.** I keep that claim tied to this implementation and policy rather than presenting it as a universal OTA benchmark.

The result I retained was: **The runtime can verify and distribute releases without being able to create new trusted signatures.**

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

Compatibility and trust decide whether a technically downloadable image is safe and authorized to run. Partition generation, bootloader generation, persistent schema, security epoch, hash and signature are independent gates.

I approached this as a transaction with an explicit commit point. The problem was If the OTA server stored the production signing private key, compromise of the delivery plane could become authority to mint trusted firmware. The evidence was The migration policy keeps the P-256 private key on the authorized operator machine with mode 0600; hserver and devices receive only the public verification key. The reason that evidence mattered is Signing authority and artifact distribution are separate trust domains. I deliberately avoided Keeping the private key beside the files for operational convenience.. The accepted outcome was The runtime can verify and distribute releases without being able to create new trusted signatures.

The practical rule was: **Separate signing authority from delivery authority.** That rule is more durable than any one endpoint or database column because it defines which component is allowed to claim which truth.

## Reconstructing the transition

```
assignment gate ---- model/hw/partition/bootloader/schema/security
artifact gate   ---- SHA-256 + approved ECDSA signature
migration gate  ---- rollback-compatible OR explicit service mode
only then can normal A/B OTA proceed.
```

I used one question to keep the model honest: **Which component is allowed to commit this state?**

For this case, the answer starts with the observed problem: If the OTA server stored the production signing private key, compromise of the delivery plane could become authority to mint trusted firmware. The control plane already had evidence that The migration policy keeps the P-256 private key on the authorized operator machine with mode 0600; hserver and devices receive only the public verification key. That evidence only becomes useful when it is attached to the correct transition. The underlying reason is Signing authority and artifact distribution are separate trust domains.

Now consider the counterfactual. Suppose the server keeps its desired state, but the device never reports the corresponding running state. Nothing should silently advance. Suppose the device reports a terminal-looking string that belongs to an older release. The new assignment should not inherit that causality. Suppose a release is cryptographically valid but persistent-state compatibility is wrong. Delivery still has to stop. These are all examples of locally reasonable facts that become globally wrong when their scope is lost.

The shortcut I rejected was Keeping the private key beside the files for operational convenience. It removes a state or validation step, but that apparent simplicity only pushes ambiguity into recovery. The retained result—The runtime can verify and distribute releases without being able to create new trusted signatures.—keeps the ambiguity visible until a component with the right authority resolves it.

## Implementation boundary

Compatibility belongs in structured metadata rather than release notes. Device heartbeat reports partition generation, bootloader generation, schema version, security version and rollback capability; release metadata states the compatible window. The server rejects a mismatch at assignment and checks again at artifact request. Signature verification is independent: an image can be compatible but untrusted, or trusted but incompatible.

The control plane should remain conservative when evidence is missing or stale. In this case, the key observation is **The migration policy keeps the P-256 private key on the authorized operator machine with mode 0600; hserver and devices receive only the public verification key.**. I would expose enough state to verify that observation without copying secrets or giant diagnostic payloads into the event stream.

The minimum useful operational record includes the device identifier, release identifier where relevant, previous and target versions, assignment state, boot/update state, and a sanitized result. For device-side acceptance I also want the generations that determine compatibility. These fields are not decoration: they let an incident review distinguish “server wanted release X,” “device downloaded release X,” “device booted release X,” and “device accepted release X.”

The unsafe alternative was **Keeping the private key beside the files for operational convenience.**. That alternative usually saves one field or one state transition, but it makes recovery ambiguous. When the system later fails, an operator has to infer what probably happened from timestamps and logs. I would rather spend a little more schema/API complexity up front and make the transition mechanically provable.

## The invariants I wanted before the transition

- model/MCU/hardware match
- partition and bootloader generations match
- schema/security compatibility holds
- hash and detached signature verify
- signing authority is outside delivery host

For **The Signing Private Key Does Not Belong on the OTA Runtime Host**, the key mechanism is that Signing authority and artifact distribution are separate trust domains. If one of these invariants is unknown, the control plane should prefer a blocked or pending state over inventing convergence.

This is where production OTA diverges from a lab script. A lab script can assume the operator remembers which board is on which image. A fleet service has to make those assumptions explicit enough that another process can reject a dangerous transition automatically.

## What the evidence proves—and what it does not

The evidence supports this narrow statement: **The runtime can verify and distribute releases without being able to create new trusted signatures.**

It does not prove that every future firmware is safe, that every device will remain online, or that the server can infer unreported device state. OTA is distributed: the server knows assignment intent, the device knows what it is executing, and the bootloader knows pending/rollback state. No one component has perfect knowledge at every instant.

That is why **Signing authority and artifact distribution are separate trust domains.** The correct model tolerates temporary disagreement and waits for the observation that resolves it. It is better to show PENDING than to manufacture success from stale data.

## What changes when the fleet grows

At two devices, an engineer can remember almost everything. At five devices, informal state already becomes unreliable. At twenty devices, a shared secret, ambiguous version string or manual “I think that board updated” workflow becomes an incident generator.

I would keep the same model as the fleet grows and change the implementation around it: stronger key custody, richer cohorts, more formal release approvals, better metrics and eventually geographically independent control-plane recovery. I would not remove the distinctions between device identity, desired release, running release, release policy and rollback state. Those distinctions become more valuable with scale.

The mechanism remains the same: Signing authority and artifact distribution are separate trust domains. Distributed state does not disappear when more automation is added; automation simply makes incorrect state transitions happen faster if the model is weak.

## The rule I kept

**Separate signing authority from delivery authority.**

The result from this case was The runtime can verify and distribute releases without being able to create new trusted signatures.

That is the core of production OTA for me. The hard problem is not moving a `.bin` file over HTTPS. The hard problem is preserving causal truth while identity, policy, persistent data, bootloader state, device observations and operator intent change at different times.

A successful update is therefore not “download returned 200.” It is a sequence of authorized, compatible and observable state transitions with a recovery path at every irreversible boundary.
