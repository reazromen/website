---
title: Remember-Me Is a Security Policy, Not a Convenience Toggle
url: /posts/remember-me-is-security-policy-not-convenience-toggle.html
date: '2021-09-02'
read_time: 1
excerpt: Long-lived trusted-browser sessions change the authentication risk model
  and should be chosen deliberately.
topic: web-control-plane
tags:
- authelia
- session
- 2fa
- security
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Authentication and Ingress · intermediate'
outputs:
- url: /posts/remember-me-is-security-policy-not-convenience-toggle.html
  template: cms/templates/posts/posts--remember-me-is-security-policy-not-convenience-toggle.tpl
  source: cms/templates/posts/posts--remember-me-is-security-policy-not-convenience-toggle.json
---

The operator experience needed fewer repeated logins, but simply making sessions 'never expire' would have traded usability for an uncontrolled credential lifetime. Inactivity timeout, absolute expiration and remember-me duration solve different problems. Mixing them into one long number makes revocation and stolen-browser risk harder to reason about.

The SSO policy separates a 12-hour inactivity window, 24-hour normal expiration and 30-day remember-me duration while retaining two-factor access for the admin group.

Document why each session lifetime exists, review it with the threat model, and keep account-level revocation available so a long remember-me window does not become an irreversible access grant. Session management is risk-based authentication design. Long-lived sessions should be revocable, stored safely and scoped to a trusted cookie domain rather than used as a substitute for identity assurance. The concrete hserver evidence is commit aa114a5, so this note is tied to an actual production change rather than a hypothetical failure.
