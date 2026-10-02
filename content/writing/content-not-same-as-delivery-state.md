---
title: Content Is Not the Same Thing as Delivery State
url: /posts/content-not-same-as-delivery-state.html
date: '2026-09-14'
read_time: 1
excerpt: The authoritative article text can remain stable while each destination has
  its own mutable publishing lifecycle.
topic: production-engineering
tags:
- content-system
- source-of-truth
- publisher
- architecture
draft: false
featured: false
language: en
eyebrow: 'Hserver Failure Notes: Data Integrity and Publishing · intermediate'
outputs:
- url: /posts/content-not-same-as-delivery-state.html
  template: cms/templates/posts/posts--content-not-same-as-delivery-state.tpl
  source: cms/templates/posts/posts--content-not-same-as-delivery-state.json
---

The design keeps local content as the source of authored intent and tracks per-destination delivery separately with remote IDs and status.

The content automation stack connects authored material to external publishers. A post may be approved once but delivered to several destinations with different timing, identifiers and failure histories. Treating remote delivery as part of the content object would couple editorial truth to transport-specific state and make retries modify the wrong abstraction.

This is separation of concerns and event-driven integration. A stable domain object should not absorb every lifecycle of the systems that consume it.

Define ownership for each field: editorial content, scheduling intent, delivery attempt and provider response. Clear ownership prevents two integrations from overwriting each other's state. The concrete hserver evidence is commit f30248c, so this note is tied to an actual production change rather than a hypothetical failure.
