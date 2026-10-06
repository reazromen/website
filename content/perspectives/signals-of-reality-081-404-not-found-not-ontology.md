---
title: 404 Not Found Is Not Ontology
url: /posts/signals-of-reality-081-404-not-found-not-ontology.html
date: '2026-05-17'
read_time: 6
excerpt: HTTP 404 describes how an origin server answered a request. It does not prove that the thing named by the URL does not exist in every relevant sense.
topic: networking
tags:
- http
- status-codes
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

A browser asks for a resource.

The server replies:

404 Not Found.

The phrase feels metaphysical. Not found becomes not there.

But HTTP is more careful than ordinary language. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) says a 404 means the origin server did not find a current representation for the target resource **or is not willing to disclose that one exists**.

That second possibility changes the philosophy of the status code.

404 is a protocol statement, not an ontology.

## The response describes one interaction

A URL is a name inside a protocol and namespace.

A request reaches some server through DNS, routing, TLS, reverse proxies, caches, load balancers, and application logic. At the end of that chain, one component chooses a response.

The response tells us something about that request path at that time.

It does not automatically tell us whether a file exists on disk, whether a database row exists, whether another authenticated user can see the resource, or whether another server would answer differently.

The representation is what the protocol exposes.

The internal world can be larger.

## 404 can intentionally hide existence

A server may avoid returning 403 Forbidden because doing so reveals that a protected resource exists.

RFC 9110 explicitly permits an origin server to return 404 when it wishes to hide the current existence of a forbidden target.

From a security and privacy perspective, this can be useful.

From an epistemic perspective, it means the same observable response can correspond to multiple internal states.

No resource.

Resource exists but is hidden.

Wrong tenant.

Wrong route.

Expired mapping.

Authorization policy.

The outside observer receives one symbol for several possibilities.

## Protocols compress state

This is not a flaw unique to HTTP.

Every interface compresses internal complexity into a smaller vocabulary.

A process exit code reduces a complicated execution history to an integer.

A monitoring light reduces a system to red, amber, or green.

A SIP response reduces call-routing state to a code.

The compression is what makes interfaces usable.

The danger appears when the receiver forgets that compression happened.

404 is useful precisely because clients do not need to know every internal reason behind the response.

## Debugging requires another layer

When an operator sees a 404, the next question is not simply "where is the missing file?"

Ask which component generated it.

Was it the CDN?

Reverse proxy?

Framework router?

Application?

Object store?

Origin server?

Authorization layer?

A 404 from Cloudflare and a 404 from an application can look similar to the browser while having completely different causes.

Headers, traces, logs, request IDs, and direct-origin tests help identify the responding layer.

The code alone is insufficient.

## 410 exists for a stronger claim

HTTP even distinguishes 404 from 410 Gone.

RFC 9110 says 410 indicates that access is no longer available and the condition is likely permanent. A server that cannot determine permanence should generally use 404 instead.

That difference is revealing.

Protocols can express different degrees of knowledge.

404 is deliberately compatible with uncertainty.

410 makes a stronger temporal claim.

Neither is a statement about existence outside the protocol.

## The lesson generalizes

Human beings constantly receive status-like signals.

Unavailable.

Rejected.

Unknown.

Offline.

Not found.

It is easy to treat these labels as direct descriptions of reality.

Often they are descriptions of what one interface can currently say.

A reliable engineer asks what state space the interface collapses.

Which different worlds produce the same response?

What additional observation would separate them?

404 Not Found is not ontology.

It is a carefully defined sentence spoken by one layer of a system.
