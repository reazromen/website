---
title: Session Inactivity, Expiration and Remember Me Solve Different Problems
url: /posts/session-inactivity-expiration-remember-me-different-problems.html
date: '2023-04-21'
read_time: 1
excerpt: A session can have an idle timeout, a hard lifetime and a trusted-browser
  persistence policy at the same time.
topic: security-identity
tags:
- authelia
- session
- cookies
- sso
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: Authelia SSO · advanced'
outputs:
- url: /posts/session-inactivity-expiration-remember-me-different-problems.html
  template: cms/templates/posts/posts--session-inactivity-expiration-remember-me-different-problems.tpl
  source: cms/templates/posts/posts--session-inactivity-expiration-remember-me-different-problems.json
---

I originally treated “how long should login last?” as one setting. Authelia makes it three separate decisions, and that is a better model.

`inactivity` limits how long an unused session survives. `expiration` sets the maximum lifetime of the active session. `remember_me` controls how long a trusted browser can retain the ability to resume authentication according to the identity provider's policy. Our reviewed values are 12 hours inactivity, 24 hours expiration and 30 days remember-me.

Those controls answer different threat and usability questions. A short idle timeout protects an abandoned workstation. A hard expiration prevents a continuously used session from living forever. Remember-me reduces repeated MFA prompts on an explicitly trusted browser without making the active session itself infinite.

The debugging lesson is equally useful: when a user says “I got logged out,” first identify which lifetime expired. Treating every logout as a cookie bug hides the actual session policy.

## Engineering evidence

The hserver repository evidence for this note is commit `aa114a5`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
