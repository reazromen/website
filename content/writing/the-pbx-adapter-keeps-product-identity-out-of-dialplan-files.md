---
title: The PBX Adapter Keeps Product Identity Out of Dialplan Files
url: /posts/the-pbx-adapter-keeps-product-identity-out-of-dialplan-files.html
date: '2026-09-14'
read_time: 1
excerpt: Asterisk should route calls, not become the only database of parent-approved
  relationships.
topic: loup-engineering
tags:
- pbx-adapter
- dialplan
- backend
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: PBX & Network · advanced'
outputs:
- url: /posts/the-pbx-adapter-keeps-product-identity-out-of-dialplan-files.html
  template: cms/templates/posts/posts--the-pbx-adapter-keeps-product-identity-out-of-dialplan-files.tpl
  source: cms/templates/posts/posts--the-pbx-adapter-keeps-product-identity-out-of-dialplan-files.json
---

The important detail in The PBX Adapter Keeps Product Identity Out of Dialplan Files was not the component name but the contract around it. LOUP separates backend identity and contact policy from PBX-specific extension and route configuration.

An adapter can materialize the telephony state the PBX needs while preserving the backend as the authority for pairing, contacts, blocking and ownership. This also makes migration to a different PBX less destructive because product concepts do not have to be reverse-engineered from dialplan rules.

The acceptance test was written around observable behaviour rather than whether a task, container or peripheral merely reported that it had started. Evidence marker: `pbx-adapter-boundary`.

Do not let infrastructure configuration silently become the product data model. That gives the team a concrete acceptance condition and a rollback point rather than a subjective sense that the build is probably better.

## Project evidence

LOUP engineering marker: `pbx-adapter-boundary`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
