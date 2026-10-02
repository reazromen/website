---
title: A Secret Manager Is an Authorization System, Not Just Encrypted .env
url: /posts/secret-manager-is-authorization-system-not-encrypted-env.html
date: '2026-09-14'
read_time: 1
excerpt: OpenBao adds identity, policy, versioning, leases and audit around secrets
  instead of merely moving plaintext to a different file.
topic: security-identity
tags:
- openbao
- secrets
- acl
- architecture
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: OpenBao Secrets · advanced'
outputs:
- url: /posts/secret-manager-is-authorization-system-not-encrypted-env.html
  template: cms/templates/posts/posts--secret-manager-is-authorization-system-not-encrypted-env.tpl
  source: cms/templates/posts/posts--secret-manager-is-authorization-system-not-encrypted-env.json
---

Moving credentials from Git into one encrypted file would reduce accidental exposure, but it would not create a real secret control plane.

OpenBao changes the model because every request is authenticated and then authorized against policy. A workload does not receive “the secrets file”; it receives a token associated with specific capabilities on specific paths. The current hserver policies separate runtime read access, operator lifecycle access and backup snapshot access.

That gives secret handling an explicit security model. A runtime service can read the production values it needs without being able to rewrite them. The backup identity can read the Raft snapshot endpoint without becoming a general OpenBao administrator. The operator workflow can manage versioned application secrets without receiving root control over auth methods or audit devices.

The useful shift is from secret storage to secret authorization. Encryption protects data at rest; identity and policy determine who can ask for what while the system is running.

## Engineering evidence

The hserver repository evidence for this note is commit `1f583b4`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
