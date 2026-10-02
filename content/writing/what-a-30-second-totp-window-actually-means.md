---
title: What a 30-Second TOTP Window Actually Means
url: /posts/what-a-30-second-totp-window-actually-means.html
date: '2026-09-14'
read_time: 2
excerpt: TOTP is not a random six-digit number every half minute; it is a deterministic
  moving-factor calculation with a strict verifier window.
topic: security-identity
tags:
- totp
- rfc-6238
- time
- mfa
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: TOTP & MFA · advanced'
outputs:
- url: /posts/what-a-30-second-totp-window-actually-means.html
  template: cms/templates/posts/posts--what-a-30-second-totp-window-actually-means.tpl
  source: cms/templates/posts/posts--what-a-30-second-totp-window-actually-means.json
---

The 30-second setting in Authelia is more than a UI detail. It defines the moving time step used by the authenticator and verifier. During a given step, both sides can independently derive the same one-time password from the shared enrollment secret.

That explains two behaviors that otherwise look mysterious. A code can be rejected even though it was typed correctly if it belongs to an older time step, and two devices holding the same enrollment secret can generate the same code without talking to each other. There is no server push involved.

The verifier can allow a small amount of skew because real clocks are not perfectly aligned. Our Authelia configuration uses `skew: 1`, which deliberately trades a little extra acceptance window for tolerance of small time differences. Increasing that window casually would weaken the temporal constraint of the second factor.

When debugging TOTP I therefore check time synchronization and enrollment state before blaming the authenticator app. The code is only the visible output of a time-and-secret synchronization protocol.

## Engineering evidence

The hserver repository evidence for this note is commit `ce8b908`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
