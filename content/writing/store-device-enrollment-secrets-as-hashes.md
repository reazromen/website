---
title: Store Device Enrollment Secrets as Hashes When the Server Only Needs Verification
url: /posts/store-device-enrollment-secrets-as-hashes.html
date: '2026-09-14'
read_time: 1
excerpt: If a token only needs to be checked, retaining the plaintext creates unnecessary
  breach impact.
topic: ota-fleet
tags:
- tokens
- hashing
- device-enrollment
- security
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: OTA State Machines · advanced'
outputs:
- url: /posts/store-device-enrollment-secrets-as-hashes.html
  template: cms/templates/posts/posts--store-device-enrollment-secrets-as-hashes.tpl
  source: cms/templates/posts/posts--store-device-enrollment-secrets-as-hashes.json
---

Enrollment generates unique credentials, returns the secret at provisioning time and stores a hash for later verification. Rotation and revocation operate on the device identity rather than exposing stored plaintext.

Per-device OTA credentials are long-lived enough to matter and numerous enough that storing them in plaintext would create a concentrated secret database. The server normally needs to verify a presented token, not recover the original value. The storage model was a credential-lifecycle decision, not just a database column choice. Recoverable plaintext increases the value of a database compromise without helping normal authentication.

This follows the same principle used for passwords: store a verifier when authentication does not require secret recovery. OWASP secret-management guidance also favors minimizing exposure and access surface.

Treat enrollment output as a one-time provisioning event, log only non-secret identifiers, and make credential rotation a normal API path rather than a database repair operation. The concrete hserver evidence is commit c7ff2df, so this note is tied to an actual production change rather than a hypothetical failure.
