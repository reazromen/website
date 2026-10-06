---
title: 410 Gone vs 404 Not Found
url: /posts/signals-of-reality-084-410-gone-vs-404-not-found.html
date: '2026-10-02'
read_time: 6
excerpt: 404 and 410 differ not mainly in severity but in what the server claims to know about permanence and history.
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

Two URLs return no usable resource.

One returns 404 Not Found.

The other returns 410 Gone.

To a hurried user they look equivalent.

To HTTP they make different claims.

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) describes 404 as meaning the origin server did not find a current representation or does not wish to disclose one. It describes 410 as indicating that access is no longer available and the condition is likely permanent.

The distinction is about knowledge and time.

## 404 preserves uncertainty

A 404 can mean:

the resource never existed,

the path is wrong,

the resource is temporarily unavailable,

the server does not know whether the condition is permanent,

or the server is hiding the resource.

It is a deliberately broad answer.

Clients can react sensibly without learning the internal history.

That makes 404 a practical default.

## 410 makes a stronger temporal claim

Gone contains memory.

The server is saying, in effect:

I know this target used to be available or was intentionally addressable, and I have reason to believe the absence is permanent.

RFC 9110 notes that 410 is intended to help web maintenance by indicating that remote links should be removed.

That is more than lookup failure.

It is a claim about lifecycle.

## Stronger claims need stronger knowledge

Why not return 410 for every missing page?

Because the server may not know enough.

A reverse proxy may have no database of deleted routes.

A static host may only know whether a file exists now.

A dynamic application may intentionally treat unknown and deleted identifiers the same.

The protocol can only express what the component can justify.

This is a recurring systems principle: the most precise status is not always the most truthful if the sender lacks the state needed to support it.

## Caches remember absence

Both 404 and 410 can interact with caching.

A negative answer can persist beyond the moment that generated it.

That creates an interesting edge case: the origin's state changes, but an intermediary continues serving a representation of earlier absence until caching rules permit revalidation.

The receiver is observing a remembered claim.

This is not unique to errors. Caches always separate the time of origin state from the time of delivered state.

But with 410 the temporal semantics are especially visible.

## Lifecycle should be modeled explicitly

Content systems often treat deletion as a boolean.

Exists.

Does not exist.

Real systems have richer histories.

Draft.

Published.

Moved.

Archived.

Temporarily hidden.

Deleted accidentally.

Deleted intentionally.

Legally removed.

Replaced.

HTTP cannot encode that entire lifecycle in one status code.

But 404 and 410 demonstrate that even simple protocols benefit from distinguishing current absence from known permanent removal.

## The philosophical difference is modest but useful

404 says:

I cannot give you a current representation, and I am not making a stronger promise about why or for how long.

410 says:

I know enough to tell you this is gone in a way that should influence future behavior.

Neither code tells us everything.

Both are interface-level claims.

The interesting part is not that 410 is "more missing."

It is that 410 contains more asserted knowledge.

Protocols become clearer when we read status codes as statements with evidential scope, not as labels attached directly to reality.
