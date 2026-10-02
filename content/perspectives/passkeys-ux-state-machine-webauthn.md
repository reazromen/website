---
title: Passkeys Are Cryptographically Simple Compared With Their UX State Machine
url: /posts/passkeys-ux-state-machine-webauthn.html
date: '2026-09-26'
read_time: 9
excerpt: WebAuthn can prove possession of a scoped private key. The product still
  has to reason about synced credentials, discoverable accounts, conditional UI, recovery,
  re-registration, and what the browser chooses to show.
topic: ''
tags:
- passkeys
- webauthn
- authentication
- security
draft: false
featured: false
language: en
eyebrow: Identity & Security · systems note
outputs:
- url: /posts/passkeys-ux-state-machine-webauthn.html
  template: cms/templates/posts/posts--passkeys-ux-state-machine-webauthn.tpl
  source: cms/templates/posts/posts--passkeys-ux-state-machine-webauthn.json
---

Passkeys are often introduced with a wonderfully clean diagram.

The server stores a public key. The authenticator keeps the private key. A challenge is signed. Phishing resistance improves because the credential is scoped to the relying party.

Cryptographically, that mental model is useful.

Product behavior gets messy because the credential is not living in an isolated protocol diagram. It is living inside browsers, operating systems, platform credential stores, password managers, device sync, account recovery, and user expectations built by decades of passwords.

## The server does not fully control credential presentation[#](#the-server-does-not-fully-control-credential-presentation)

WebAuthn deliberately gives the user agent a mediation role. Browsers and authenticators decide how available credentials are presented while preserving privacy and requiring user consent.

That means a relying party cannot assume it owns every visual step of the authentication flow.

Conditional mediation makes this more visible. A site can allow passkeys to appear in an autofill-style experience, but the browser/platform controls how discoverable credentials are surfaced.

That is good security architecture. It also means UX debugging crosses an API boundary.

## Discoverable credentials change account lookup[#](#discoverable-credentials-change-account-lookup)

Traditional authentication starts with an identifier:

```
email -> find account -> verify secret
```

A discoverable WebAuthn credential can invert that:

```
authenticator selects credential
    -> assertion includes credential identity
    -> relying party resolves account
```

This enables username-less sign-in, but it changes how account selection, multiple accounts, and recovery need to work.

If one user has several accounts on the same relying party, what should the account picker show? If a passkey is synced to a new device, what name helps the user choose the right account? If an old credential remains in a platform store after the server removed it, how does the error path explain the mismatch?

Those are state-model problems.

## Registration is not “one passkey per user”[#](#registration-is-not-one-passkey-per-user)

A real account can have multiple credentials: phone, laptop, hardware security key, synced passkey provider, enterprise authenticator, or replacements over time.

The server therefore needs a credential inventory, not one credential column.

Useful metadata includes credential ID, creation time, last-used time, user-visible label, transport hints where appropriate, and revocation state. The exact data model depends on privacy and product requirements, but the conceptual point is stable: authentication devices have a lifecycle.

Re-registration also needs thought. `excludeCredentials` can help prevent creating a duplicate credential when the authenticator can identify an existing one, but browsers and synced credential systems can still produce user experiences that surprise application developers.

## A “ghost passkey” can exist from either side[#](#a-ghost-passkey-can-exist-from-either-side)

Imagine the user deletes a passkey from the website but a synced credential remains visible in a platform picker. Or the user deletes the local/synced credential while the server still lists it in account security settings.

Neither side has universal authority over the other side's storage.

So the account UI needs to tolerate asymmetry:

- credential exists server-side but is unavailable to the user,
- credential appears client-side but server no longer recognizes it,
- credential is available on one device but not another,
- provider sync has not converged yet.

Errors such as “invalid credential” may be technically accurate and still be useless UX.

## Recovery is part of passkey architecture[#](#recovery-is-part-of-passkey-architecture)

A passkey system is only as secure as the path used when the passkey is unavailable.

If recovery falls back to a weak email flow with no additional protection, the account has not magically become phishing resistant in every state. If support staff can bypass the strong credential casually, the human process becomes part of the trust boundary.

I would model authentication states explicitly:

```
normal passkey login
new device with synced passkey
new device without passkey
lost authenticator
credential revoked
account recovery
high-risk recovery
credential re-enrollment
```

Each transition should have a threat model, not just a screen design.

## PWAs and embedded contexts add more state[#](#pwas-and-embedded-contexts-add-more-state)

Developers naturally expect an installed PWA to behave like “the same site in an app.” Authentication APIs, platform credential UI, browser mediation, origin rules, and OS integration can make the user experience differ across contexts.

The correct debugging method is to capture the exact environment: origin, browser engine, installed/not installed, platform, authenticator type, conditional mediation state, and whether the credential is discoverable or server-selected.

Without that matrix, passkey bugs become anecdotes.

## Level 3 does not eliminate product work[#](#level-3-does-not-eliminate-product-work)

WebAuthn Level 3 became a W3C Recommendation on August 25, 2026. That maturity is significant: the protocol surface is becoming more capable and standardized.

But a Recommendation cannot decide your recovery policy, account model, credential-management UI, fraud controls, or how you explain platform-owned credential state to a human.

Those are product and security decisions built on top of the protocol.

## The right abstraction[#](#the-right-abstraction)

I would not think of passkeys as a replacement password field.

I would think of them as a distributed credential system with three authorities:

- the relying party owns account authorization and registered public credentials,
- the authenticator owns private-key operations and user verification,
- the browser/OS mediates discovery and user interaction.

Once those boundaries are explicit, the confusing UX makes more sense.

The cryptography can be correct while the account state machine is wrong. Most difficult passkey deployments are not failing on signature verification. They are failing in the transitions around it.

## Sources and further reading[#](#sources-and-further-reading)

- [W3C: WebAuthn Level 3 became a Recommendation on August 25, 2026](https://www.w3.org/news/2026/web-authentication-an-api-for-accessing-public-key-credentials-level-3-is-now-a-w3c-recommendation/)
- [W3C WebAuthn Level 3 specification](https://www.w3.org/TR/webauthn-3/)
- [FIDO Alliance: Passkeys](https://fidoalliance.org/passkeys/)
