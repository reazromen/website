---
title: KV v2 Turns Secret Rotation into a Versioned State Transition
url: /posts/kv-v2-turns-secret-rotation-into-versioned-state-transition.html
date: '2025-08-11'
read_time: 1
excerpt: Keeping versions makes rotation and rollback explicit instead of overwriting
  the only known credential value.
topic: security-identity
tags:
- openbao
- kv-v2
- rotation
- rollback
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: OpenBao Secrets · advanced'
outputs:
- url: /posts/kv-v2-turns-secret-rotation-into-versioned-state-transition.html
  template: cms/templates/posts/posts--kv-v2-turns-secret-rotation-into-versioned-state-transition.tpl
  source: cms/templates/posts/posts--kv-v2-turns-secret-rotation-into-versioned-state-transition.json
---

A normal environment file encourages destructive updates: replace the old password with the new one and hope every consumer has reloaded correctly.

KV v2 gives the secret path a version history. The hserver rotation model is write version N+1, re-authenticate or reload the consumer, run a health canary, then retire version N. That sequence creates a controlled migration window rather than an instantaneous cutover with no memory.

Versioning does not automatically rotate the credential at the external system. The target database, API or service still has its own source of truth. The value of KV v2 is that OpenBao can preserve the secret-side history while the operator verifies each transition.

Rollback also becomes a defined action. Restore a prior secret version or re-issue the prior credential at the target system, then verify the consumer again. The important part is that rollback is planned before rotation rather than improvised after an outage.

## Engineering evidence

The hserver repository evidence for this note is commit `1f583b4`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
