---
title: A Server Can Hide Behind 404
url: /posts/signals-of-reality-083-server-can-hide-behind-404.html
date: '2026-03-23'
read_time: 6
excerpt: HTTP deliberately allows a server to answer 404 instead of revealing a forbidden resource. The same external observation can therefore conceal different internal states.
topic: networking
tags:
- http
- access-control
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

Imagine two requests for the same URL.

One comes from an authorized account.

The other comes from a stranger.

The first receives the document.

The second receives 404.

Did the document cease to exist for the second person?

No.

The interface chose not to disclose its existence.

This behavior is explicitly compatible with HTTP semantics. [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) allows an origin server that wants to hide a forbidden target to answer with 404.

The protocol gives a system permission to be strategically incomplete.

## Information can leak through error vocabulary

Suppose a private resource returns 403 Forbidden to unauthenticated callers.

An observer can now distinguish two cases:

404 means no such resource.

403 means a resource exists but I cannot access it.

That distinction may reveal names, identifiers, or account relationships the system would rather keep private.

Returning the same 404 for both cases reduces what the external observer can infer.

The response is still useful to the client: it cannot obtain the resource.

But it withholds the reason.

## Indistinguishable states are a design choice

This is a general security principle.

If two internal states should not be distinguishable to an external party, the interface can deliberately map them to the same observable outcome.

Authentication systems may avoid revealing whether a username exists.

Password reset flows may use generic responses.

APIs may normalize timing or error detail.

The goal is not to make the system dishonest in a moral sense.

It is to limit information exposure.

Interfaces are allowed to know more than they say.

## Operators need a richer truth

The same design that protects information from outsiders can make debugging harder for insiders.

A user reports 404.

Was the route absent?

Was authorization denied?

Was tenancy wrong?

Was the object deleted?

Was the request handled by a fallback?

The external status cannot answer.

Internal observability has to preserve distinctions that the public interface intentionally hides.

Structured logs, traces, authorization decision records, and request IDs become the operator's richer vocabulary.

The public interface compresses.

The internal diagnostic system decompresses.

## A status code is an audience-specific statement

This suggests a deeper way to think about protocols.

A message is not merely a fact.

It is a fact selected for a receiver.

The system may know more than the receiver is entitled to know.

The protocol response is therefore shaped by policy as well as mechanism.

This happens outside security too.

A service may return a generic 503 instead of exposing internal dependency names.

A database client may receive one error while server logs preserve a detailed stack.

Different audiences receive different representations of the same event.

## Hidden does not mean arbitrary

The server cannot return random meanings and remain interoperable.

HTTP still constrains what 404 means to clients: the requested current representation was not found or is not being disclosed.

That is enough for client behavior.

The ambiguity is intentional and bounded.

This is what makes protocols interesting epistemically.

They define not only how systems communicate, but how much one participant can legitimately infer from the other's words.

A server can hide behind 404.

The response is accurate at the interface while incomplete about the internal world.

And sometimes that incompleteness is exactly the feature.
