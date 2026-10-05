---
title: The TOTP QR Code Is a Secret-Enrollment Ceremony
url: /posts/totp-qr-code-is-a-secret-enrollment-ceremony.html
date: '2026-06-20'
read_time: 1
excerpt: Scanning the QR code transfers long-lived secret material; it should be treated
  more carefully than an ordinary setup screen.
topic: security-identity
tags:
- totp
- qr-code
- secret-enrollment
- mfa
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: TOTP & MFA · advanced'
outputs:
- url: /posts/totp-qr-code-is-a-secret-enrollment-ceremony.html
  template: cms/templates/posts/posts--totp-qr-code-is-a-secret-enrollment-ceremony.tpl
  source: cms/templates/posts/posts--totp-qr-code-is-a-secret-enrollment-ceremony.json
---

The QR code shown during TOTP enrollment looks harmless because it is only visible for a moment. Architecturally it is one of the most sensitive moments in the whole second-factor lifecycle.

The code encodes the information an authenticator needs to generate future OTP values, including the shared secret. Anyone who copies that enrollment material can generate the same future codes. The six-digit OTP expires quickly; the enrollment secret does not.

That changes how I think about screenshots, screen sharing and device enrollment. A screenshot of a normal settings page may be low risk. A screenshot of a live TOTP enrollment QR code can become a durable second-factor clone. The right model is key provisioning, not convenience setup.

For a self-hosted identity system the enrollment flow should therefore happen over the trusted authentication origin, after first-factor identity has been established, with registration state stored by the identity provider and recovery handled deliberately.

## Engineering evidence

The hserver repository evidence for this note is commit `ce8b908`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
