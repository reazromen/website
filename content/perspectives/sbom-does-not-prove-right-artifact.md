---
title: An SBOM Tells You What You Shipped; It Does Not Prove You Shipped the Right
  Thing
url: /posts/sbom-does-not-prove-right-artifact.html
date: '2022-01-06'
read_time: 9
excerpt: An SBOM inventories components. Supply-chain trust also needs provenance,
  build identity, signatures, policy, artifact verification, and release evidence
  that connects source to the bytes actually deployed.
topic: ''
tags:
- sbom
- slsa
- sigstore
- provenance
draft: false
featured: false
language: en
eyebrow: Software Supply Chain · systems note
outputs:
- url: /posts/sbom-does-not-prove-right-artifact.html
  template: cms/templates/posts/posts--sbom-does-not-prove-right-artifact.tpl
  source: cms/templates/posts/posts--sbom-does-not-prove-right-artifact.json
---

SBOMs solved an important visibility problem: when a vulnerable component is announced, you need to know where that component exists.

But an inventory of components does not answer a different question:

**Why should I trust that this artifact is the one my build system was supposed to produce?**

Those are related supply-chain questions, not interchangeable ones.

## An SBOM describes composition[#](#an-sbom-describes-composition)

A software bill of materials can record packages, versions, relationships, hashes, and other component metadata depending on the format and producer.

That helps vulnerability response, licensing analysis, dependency discovery, and incident scoping.

It does not automatically prove:

- which source revision produced the artifact,
- which CI workflow built it,
- which identity triggered the build,
- whether the build definition was modified,
- whether the artifact was replaced after generation,
- or whether the deployed bytes match the reviewed release.

For those questions you need evidence about origin and process.

## Provenance is the chain back to the build[#](#provenance-is-the-chain-back-to-the-build)

SLSA defines provenance as verifiable information describing where, when, and how an artifact was produced.

Build provenance can bind an output digest to source and build metadata. The useful unit is not a filename such as `app.tar.gz`; it is the immutable digest of the artifact.

That gives deployment policy something concrete to verify:

```
artifact digest
    <- provenance statement
       <- trusted builder identity
          <- source revision + build definition
```

The deployment system can then reject an artifact whose provenance does not satisfy policy even if the file has a familiar name.

## A signature proves a statement by an identity[#](#a-signature-proves-a-statement-by-an-identity)

Signing is another distinct layer.

Cosign can sign container images and other artifacts, including keyless flows where short-lived certificates bind an OIDC identity to the signature. Verification checks that the signature and identity constraints match what policy expects.

A valid signature answers “an accepted identity signed this digest.”

It does not by itself tell you whether the artifact was built from the intended source or passed tests. That information can be carried in attestations and provenance, but it still has to be verified by policy.

## Attestations are claims, not magic truth[#](#attestations-are-claims-not-magic-truth)

An attestation can say that tests passed, an SBOM was generated, a scanner produced a result, or a build had certain inputs.

Sigstore supports in-toto attestations and verification. The cryptography can establish who made the claim and protect it from tampering.

The relying system must still decide which attestors are trusted and what predicates are required.

If any developer laptop can produce the “tests passed” attestation accepted by production, the signature is strong but the policy is weak.

## The mundane release failures still matter[#](#the-mundane-release-failures-still-matter)

Supply-chain conversations easily become focused on sophisticated compromise while ordinary release mistakes remain common:

- wrong artifact promoted,
- old binary packaged with new metadata,
- tag moved after review,
- debug build released,
- deployment references a mutable tag,
- build job skipped a test stage,
- artifact was rebuilt locally to “fix” CI.

These are exactly the cases where provenance and digest-based promotion improve operations even without an attacker.

## The release pipeline should verify, not remember[#](#the-release-pipeline-should-verify-not-remember)

A strong model is to make each boundary verify evidence:

```
source review
  -> trusted CI builder
     -> immutable artifact digest
        -> SBOM + provenance + attestations
           -> signature / identity verification
              -> policy gate
                 -> deployment by digest
```

No human has to remember which build “looked right.” The system evaluates the artifact it is about to deploy.

## SBOMs remain useful[#](#sboms-remain-useful)

None of this is an argument against SBOMs.

They answer a question provenance does not: what components are inside this artifact? When a library vulnerability lands at 03:00, that inventory can be the fastest way to identify affected releases.

The mistake is turning one evidence type into a supply-chain strategy.

Composition, origin, identity, policy, and runtime promotion are separate trust questions.

## Start with one verifiable path[#](#start-with-one-verifiable-path)

You do not need a giant compliance platform to improve the chain.

A practical sequence is:

1. build in a controlled CI environment,
2. identify outputs by digest,
3. generate an SBOM,
4. emit build provenance,
5. sign or use keyless identity,
6. verify identity and provenance before promotion,
7. deploy the verified digest, not a mutable tag.

Then add policy for test attestations, vulnerability thresholds, branch protection, or environment-specific controls where they actually reduce risk.

## Evidence has to connect to the bytes[#](#evidence-has-to-connect-to-the-bytes)

The core principle is simple.

An SBOM is valuable because it describes the software. Provenance is valuable because it connects the software to a build. A signature is valuable because it connects a statement to an identity. Policy is valuable because it decides which evidence is sufficient.

Supply-chain security becomes real when all of those claims terminate at the exact artifact digest entering production.

## Sources and further reading[#](#sources-and-further-reading)

- [SLSA v1.2: Provenance](https://slsa.dev/spec/v1.2/provenance)
- [Sigstore: Verifying signatures with Cosign](https://docs.sigstore.dev/cosign/verifying/verify/)
- [Sigstore: in-toto attestations](https://docs.sigstore.dev/cosign/verifying/attestation/)
- [Sigstore Cosign quickstart](https://docs.sigstore.dev/quickstart/quickstart-cosign/)
