---
title: Human Identity and Workload Identity Should Not Share an Auth Method
url: /posts/human-and-workload-identity-should-not-share-auth-method.html
date: '2026-09-14'
read_time: 1
excerpt: OIDC fits interactive operators; AppRole fits non-interactive services. Combining
  them weakens both lifecycle models.
topic: security-identity
tags:
- oidc
- approle
- identity
- openbao
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: OIDC, Trust & Recovery · advanced'
outputs:
- url: /posts/human-and-workload-identity-should-not-share-auth-method.html
  template: cms/templates/posts/posts--human-and-workload-identity-should-not-share-auth-method.tpl
  source: cms/templates/posts/posts--human-and-workload-identity-should-not-share-auth-method.json
---

OpenBao supports multiple authentication methods because a browser user and a backend process have different identity lifecycles, credential ceremonies, renewal behavior and revocation requirements.

For humans, the desired path is Authelia with MFA and OIDC federation. The operator already has an interactive session, group membership and a second factor. OpenBao can map that external identity to policies without inventing another password database for people.

A workload cannot scan a QR code or satisfy an interactive redirect. It needs machine authentication such as AppRole, with credentials that can be provisioned, rotated and revoked independently of any human account.

Keeping these paths separate also improves audit interpretation. A secret read from an application role means software acted. A secret lifecycle action from an OIDC-backed operator means a person acted through the human identity plane. Good identity architecture preserves that distinction instead of forcing every actor through the same credential shape.

## Engineering evidence

The hserver repository evidence for this note is commit `1f583b4`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
