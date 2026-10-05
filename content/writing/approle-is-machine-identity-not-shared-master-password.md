---
title: AppRole Is Machine Identity, Not a Shared Master Password
url: /posts/approle-is-machine-identity-not-shared-master-password.html
date: '2022-05-07'
read_time: 1
excerpt: Workloads should authenticate to the secret authority with narrow machine
  identities rather than one credential copied across services.
topic: security-identity
tags:
- openbao
- approle
- machine-identity
- least-privilege
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: OpenBao Secrets · advanced'
outputs:
- url: /posts/approle-is-machine-identity-not-shared-master-password.html
  template: cms/templates/posts/posts--approle-is-machine-identity-not-shared-master-password.tpl
  source: cms/templates/posts/posts--approle-is-machine-identity-not-shared-master-password.json
---

Human operators and workloads do not have the same authentication problem. A person can complete MFA. A background service needs a non-interactive identity that can be scoped and revoked independently.

OpenBao's AppRole model fits that boundary. The hserver design enables AppRole for machine access and maps narrow roles to reviewed policies. A consumer authenticates, receives a token and uses that token only for the paths permitted by its policy.

The anti-pattern would be a single long-lived master token copied into every container. One leak would then collapse the whole secret plane, rotation would require touching every workload and audit events would lose useful identity context.

Machine identity should be boring and replaceable. Each workload gets only the permissions it requires, token lifetime is bounded, and compromise of one role should not imply compromise of unrelated secret paths.

## Engineering evidence

The hserver repository evidence for this note is commit `1f583b4`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
