---
title: Google Authenticator Is a TOTP Client, Not the Authentication Server
url: /posts/google-authenticator-is-a-totp-client-not-the-server.html
date: '2026-09-14'
read_time: 2
excerpt: The six-digit code comes from a shared TOTP secret and time step; Google
  Authenticator is only one compatible client.
topic: security-identity
tags:
- totp
- google-authenticator
- authelia
- mfa
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: TOTP & MFA · advanced'
outputs:
- url: /posts/google-authenticator-is-a-totp-client-not-the-server.html
  template: cms/templates/posts/posts--google-authenticator-is-a-totp-client-not-the-server.tpl
  source: cms/templates/posts/posts--google-authenticator-is-a-totp-client-not-the-server.json
---

It is easy to describe the second factor as “Google Authenticator authentication,” but that hides the useful architecture. In the hserver stack Authelia is the verifier. Google Authenticator, or another compatible authenticator app, is a client that calculates a time-based one-time password from an enrolled secret.

RFC 6238 defines TOTP as HOTP with time replacing the event counter. Both sides need the same secret, the same time-step rules and clocks that are close enough for the verifier's acceptance window. The app does not call Google to approve my login, and Authelia does not need a Google account to verify the code.

That distinction matters operationally. The identity boundary stays self-hosted. If I replace Google Authenticator with another standards-compatible TOTP app, the protocol does not change. What must remain protected is the enrollment secret and the server-side registration state.

For this deployment Authelia uses six digits, a 30-second period and a small skew allowance. The engineering object is therefore TOTP enrollment and verification, not a dependency on one mobile application.

## Engineering evidence

The hserver repository evidence for this note is commit `ce8b908`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
