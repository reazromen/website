---
title: Running Is Not the Same as Healthy
url: /posts/running-is-not-the-same-as-healthy.html
date: '2025-12-02'
read_time: 1
excerpt: Container process state only proves that PID 1 exists; readiness has to test
  the behavior the dependency actually needs.
topic: production-engineering
tags:
- docker
- healthcheck
- readiness
- compose
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Reproducibility · intermediate'
outputs:
- url: /posts/running-is-not-the-same-as-healthy.html
  template: cms/templates/posts/posts--running-is-not-the-same-as-healthy.tpl
  source: cms/templates/posts/posts--running-is-not-the-same-as-healthy.json
---

Several hserver stacks have startup ordering where an application depends on PostgreSQL, Redis or another service. Starting the dependency container first is not enough if that service is still initializing or unable to answer useful requests.

Docker documents the distinction explicitly: short-form dependencies wait for startup, while `service_healthy` waits for the declared healthcheck. SRE practice similarly prefers behavior-oriented readiness signals over process existence. Process liveness and service readiness were being treated as the same signal. Docker can report a container as running while the database is replaying state, migrations are incomplete or the endpoint is returning errors.

Compose definitions use healthchecks and `depends_on` conditions such as `service_healthy` where startup ordering matters. Application health endpoints are also checked after deployment rather than trusting container state alone.

Define health around a minimal useful transaction and keep it cheap enough to run frequently. For a database that may be `pg_isready`; for an API it may be an authenticated or dependency-aware health endpoint. The concrete hserver evidence is commit 9d36c75, so this note is tied to an actual production change rather than a hypothetical failure.
