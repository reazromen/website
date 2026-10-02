---
title: Clock Synchronization Is Part of the Authentication System
url: /posts/clock-synchronization-is-part-of-authentication.html
date: '2026-09-14'
read_time: 1
excerpt: A correct TOTP secret can still fail when the verifier and authenticator
  disagree about time.
topic: security-identity
tags:
- totp
- ntp
- clock-skew
- authentication
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: TOTP & MFA · advanced'
outputs:
- url: /posts/clock-synchronization-is-part-of-authentication.html
  template: cms/templates/posts/posts--clock-synchronization-is-part-of-authentication.tpl
  source: cms/templates/posts/posts--clock-synchronization-is-part-of-authentication.json
---

TOTP turns wall-clock time into authentication input. That means clock health is part of the security path, even though it sits outside the login form.

A password can be checked against stored material without knowing the current second. A TOTP verifier cannot. RFC 6238 derives a moving value from the current Unix time divided by the configured step. If the server clock drifts far enough from the phone, each side computes a different value from the same secret.

This is why NTP monitoring and TOTP troubleshooting belong in the same mental model. On hserver I already monitor time synchronization as an infrastructure signal. If second-factor failures suddenly affect multiple users, clock state is a higher-value check than asking everyone to re-enroll their authenticator.

The broader engineering lesson is that authentication dependencies include infrastructure services. DNS, TLS, time, session storage and the identity database can all break a login path without the credential itself being wrong.

## Engineering evidence

The hserver repository evidence for this note is commit `ce8b908`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
