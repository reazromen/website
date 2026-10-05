---
title: Static Auto-Unseal Is a Temporary Root of Trust, Not HA
url: /posts/shamir-unseal-shares-root-token-do-not-belong-on-server.html
date: '2025-01-24'
read_time: 2
excerpt: The same-host seal service removes manual unseal entry, but its static key
  remains a temporary bootstrap root of trust on the same failure domain.
topic: security-identity
tags:
- openbao
- auto-unseal
- transit
- root-of-trust
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: OIDC, Trust & Recovery · advanced'
outputs:
- url: /posts/shamir-unseal-shares-root-token-do-not-belong-on-server.html
  template: cms/templates/posts/posts--shamir-unseal-shares-root-token-do-not-belong-on-server.tpl
  source: cms/templates/posts/posts--shamir-unseal-shares-root-token-do-not-belong-on-server.json
---

The current CSL design no longer asks an operator to enter Shamir shares during normal startup. A separate `hserver-csl-seal` service auto-unseals from a runtime-only 32-byte static key, then exposes a narrowly scoped Transit key to the main OpenBao service over an internal Docker network.

That is operationally cleaner, but I do not describe it as decentralization. The static seal key and the seal service still live on the same physical hserver. They remove a manual ceremony and create a clean Transit API boundary; they do not remove the host as a common failure domain.

The main OpenBao only receives a periodic orphan token that can encrypt and decrypt the `csl-root` Transit key. It does not get key-management or general secret access on the seal service. The static key and Transit token stay out of Git, logs and container environment inspection and must be included in encrypted disaster recovery.

The long-term improvement is moving the seal service to an independent node and deleting the local static-key root of trust after a controlled auto-unseal migration.

## Engineering evidence

The hserver repository evidence for this note is commit `04e75703`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
