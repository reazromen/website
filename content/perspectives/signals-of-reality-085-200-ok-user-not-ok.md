---
title: 200 OK Does Not Mean the User Is OK
url: /posts/signals-of-reality-085-200-ok-user-not-ok.html
date: '2026-03-09'
read_time: 6
excerpt: HTTP 200 says the request succeeded under HTTP semantics. It does not guarantee that the product, business operation, rendered page, or user goal succeeded.
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

A monitoring probe requests the homepage.

The server returns 200 OK.

The dashboard turns green.

A user opens the same site and sees:

Something went wrong.

This is not necessarily a protocol violation.

HTTP success and user success are different claims.

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) defines 200 as indicating that the request succeeded, with exact semantics depending on the request method. It does not certify that the application produced the right business outcome.

## The transport can succeed while semantics fail

Imagine an API that always returns 200 with a JSON body:

`{"success": false, "error": "payment rejected"}`

Whether that API design is wise is another question.

From HTTP's perspective, the server may have successfully processed the request and returned a representation describing an application-level failure.

The client has to inspect another layer.

This pattern appears everywhere.

A web page loads successfully but JavaScript crashes.

An API returns valid JSON containing stale data.

A request completes but the workflow cannot continue.

The protocol layer is healthy.

The product is not.

## Monitoring often stops one layer too early

A simple uptime check asks:

Can I connect and receive 200?

That is useful.

It tests DNS, network reachability, TLS, HTTP handling, and at least one application route.

But it cannot answer:

Can a user sign in?

Can they search?

Can they make a call?

Can they complete checkout?

Can data be written and read back?

A synthetic user journey tests a higher layer.

Both checks matter because they fail differently.

## 200 can serve an error page

Reverse proxies and applications sometimes return custom error HTML with status 200.

Now the status is misleading even within common web conventions.

Search engines may index the page as if it were valid content.

Monitoring may remain green.

Caches may retain it.

This is often called a soft 404 when the visible page says missing while the HTTP status says success.

The mismatch shows why content and status should agree whenever possible.

Interfaces become easier to reason about when layers tell compatible stories.

## Correct bytes can contain wrong facts

The problem extends deeper.

A database can return a query successfully while the row contains incorrect data.

A cache can return exactly what it stored while the value is stale.

A sensor endpoint can return a well-formed measurement produced by a miscalibrated instrument.

Success of retrieval says nothing about truth of content.

Integrity, freshness, accuracy, and semantic correctness are separate properties.

## User goals are end-to-end

A user does not care that seven internal layers succeeded if the eighth prevents the task.

That makes end-to-end monitoring essential.

The meaningful unit is often not the component but the journey.

Resolve the name.

Reach the service.

Authenticate.

Load dependencies.

Perform the operation.

Verify the resulting state.

A green 200 at the front door cannot substitute for this chain.

## Status codes remain valuable

None of this makes HTTP status useless.

Status codes are excellent when read at their intended layer.

They let clients reason about request handling without knowing internal implementation.

The mistake is asking one layer's vocabulary to certify the entire system.

200 OK means something precise enough to be useful.

It just does not mean everything is okay.

When the user says the product is broken and the monitor says 200, believe both observations until you identify which layer each one describes.
