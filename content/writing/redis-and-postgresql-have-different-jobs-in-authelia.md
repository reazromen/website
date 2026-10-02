---
title: Redis and PostgreSQL Have Different Jobs in the Authelia Stack
url: /posts/redis-and-postgresql-have-different-jobs-in-authelia.html
date: '2026-09-14'
read_time: 1
excerpt: Persistent SSO works better when ephemeral session state and durable identity-provider
  state are not confused.
topic: security-identity
tags:
- authelia
- redis
- postgresql
- sessions
draft: false
featured: false
language: en
eyebrow: 'Identity Architecture: Authelia SSO · advanced'
outputs:
- url: /posts/redis-and-postgresql-have-different-jobs-in-authelia.html
  template: cms/templates/posts/posts--redis-and-postgresql-have-different-jobs-in-authelia.tpl
  source: cms/templates/posts/posts--redis-and-postgresql-have-different-jobs-in-authelia.json
---

The Authelia deployment uses both Redis and PostgreSQL, which can look redundant until their responsibilities are separated and each failure mode is traced to the state it actually owns.

Redis is configured as the session backend. That gives the SSO layer a shared, persistent place for session state instead of tying active sessions to the memory of one Authelia process. Recreating the Authelia container therefore does not automatically mean destroying every authenticated browser session.

PostgreSQL is Authelia's durable storage backend for identity-provider state. The user authentication backend in this deployment is still file-based, so I avoid describing PostgreSQL as the user directory. It stores the durable Authelia data required by the service while `users.yml` remains the current credential source.

This is a common architecture pattern: fast session state, durable application state and credential source can be separate systems. Knowing which layer owns which state makes backup, restart and incident recovery far less ambiguous.

## Engineering evidence

The hserver repository evidence for this note is commit `aa114a5`. The architecture is documented as current state or future phase explicitly; planned OIDC integration is not presented as already deployed.
