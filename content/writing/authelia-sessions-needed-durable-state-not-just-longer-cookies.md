---
title: Authelia Sessions Needed Durable State, Not Just Longer Cookies
url: /posts/authelia-sessions-needed-durable-state-not-just-longer-cookies.html
date: '2023-11-14'
read_time: 1
excerpt: A longer browser cookie does not help if the server forgets the session behind
  it.
topic: web-control-plane
tags:
- authelia
- redis
- sessions
- sso
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Authentication and Ingress · advanced'
outputs:
- url: /posts/authelia-sessions-needed-durable-state-not-just-longer-cookies.html
  template: cms/templates/posts/posts--authelia-sessions-needed-durable-state-not-just-longer-cookies.tpl
  source: cms/templates/posts/posts--authelia-sessions-needed-durable-state-not-just-longer-cookies.json
---

Operators were being sent back to the Authelia login portal more often than expected. Extending browser-side expiration alone would have treated the visible symptom without ensuring that the server-side session survived correctly.

Session identity is shared state between browser and authentication service. If the backend session store is memory-only or otherwise ephemeral, the cookie can outlive the state it references. The production design uses Redis as the Authelia session provider and PostgreSQL for durable Authelia storage, with explicit inactivity, expiration and remember-me windows.

Authelia recommends Redis for production and high-availability session storage rather than relying on the default in-memory provider. Authentication persistence should be designed as stateful infrastructure, not only a cookie setting. Monitor Redis and session-storage health, back up the durable identity data that matters, and test login persistence across container recreation before calling an SSO deployment stable. The concrete hserver evidence is commit aa114a5, so this note is tied to an actual production change rather than a hypothetical failure.
