---
title: Why Authelia-to-OpenBao OIDC Is a Separate Phase
url: /posts/why-authelia-to-openbao-oidc-is-separate-phase.html
date: '2022-12-01'
read_time: 1
excerpt: Human federation should be added after the secret authority is stable, not
  mixed into the initial bootstrap trust ceremony.
topic: security-identity
tags:
- oidc
- authelia
- openbao
- phased-rollout
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: OIDC, Trust & Recovery · advanced'
outputs:
- url: /posts/why-authelia-to-openbao-oidc-is-separate-phase.html
  template: cms/templates/posts/posts--why-authelia-to-openbao-oidc-is-separate-phase.tpl
  source: cms/templates/posts/posts--why-authelia-to-openbao-oidc-is-separate-phase.json
---

The target architecture is operator to Authelia/OIDC to OpenBao, but that does not mean OIDC belongs in the first OpenBao bootstrap change window.

The current runbook deliberately separates the phases. First establish OpenBao with TLS, Raft, audit, reviewed policies, AppRole machine identity, certificate operator auth, Transit auto-unseal and verified recovery snapshots. Only after that core is accepted do we configure Authelia as the OIDC provider and OpenBao as a client.

That sequencing reduces blast radius. If identity federation and the secret authority are introduced at the same time, a failed login could come from OIDC metadata, redirect URIs, session policy, TLS trust, OpenBao auth configuration or the secret service itself. Phasing removes several variables from the first acceptance test.

OIDC is therefore an architectural integration, not a checkbox. The live system should describe it as phase 2 until the provider/client flow has been deployed and verified end to end.

## Engineering evidence

The hserver repository evidence for this note is commit `04e75703`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
