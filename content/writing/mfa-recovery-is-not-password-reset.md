---
title: MFA Recovery Is Not the Same Problem as Password Reset
url: /posts/mfa-recovery-is-not-password-reset.html
date: '2022-12-22'
read_time: 1
excerpt: Losing the authenticator device creates a second-factor recovery problem
  that should not silently collapse to the password path.
topic: security-identity
tags:
- mfa
- recovery
- totp
- identity
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: TOTP & MFA · advanced'
outputs:
- url: /posts/mfa-recovery-is-not-password-reset.html
  template: cms/templates/posts/posts--mfa-recovery-is-not-password-reset.tpl
  source: cms/templates/posts/posts--mfa-recovery-is-not-password-reset.json
---

A strong second factor becomes meaningless if its recovery path is just “enter the password again.” Recovery is part of the authentication architecture, not an exception outside it.

Our Authelia configuration deliberately disables self-service password reset and password change in the current file-backed setup. That keeps the active behavior narrow while the identity system is still small. It also makes the recovery boundary explicit: operator intervention is a separate administrative process rather than an unaudited fallback button.

TOTP recovery has two different cases. I may still control the identity but have lost the enrolled authenticator, or the enrollment secret itself may be suspected compromised. The first needs re-enrollment after strong identity verification; the second also needs revocation of the previous factor.

The useful rule is that recovery should preserve the assurance level of the original control. If bypassing MFA is easier than using MFA, the recovery flow becomes the real authentication mechanism.

## Engineering evidence

The hserver repository evidence for this note is commit `ce8b908`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
