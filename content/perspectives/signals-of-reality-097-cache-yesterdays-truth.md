---
title: "Cache: Yesterday’s Truth Served Today"
url: /posts/signals-of-reality-097-cache-yesterdays-truth.html
date: '2026-04-23'
read_time: 7
excerpt: Caching deliberately allows a system to serve remembered state instead of consulting the source every time. Performance improves by tolerating bounded staleness.
topic: systems-thinking
tags:
- cache
- staleness
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

A user sees an old page after you have deployed the new one.

The origin is correct.

The file on disk is correct.

The Git commit is correct.

The browser still shows yesterday.

Nothing supernatural happened.

A cache remembered a version of truth and was permitted to reuse it.

## Caching is a bargain with time

Without caches, every request would travel to the original source.

That can be slow, expensive, and unnecessary.

Caching says:

if the answer is unlikely to change too quickly, keep a copy nearby and reuse it for some period.

The system trades perfect freshness for performance, scalability, and resilience.

This is one of the foundational bargains of distributed computing.

## A cache can be correct and stale

Suppose an HTTP response is cached for ten minutes.

At minute two, the origin changes.

At minute five, a user requests the resource and receives the old version.

The cache has not necessarily violated its contract.

It may still be inside the freshness lifetime granted by the origin or policy.

The user's statement "this is outdated" and the cache's statement "this is reusable" can both be true.

They describe different contracts.

## Invalidation is hard because memory is distributed

Once copies exist in browsers, CDNs, reverse proxies, application caches, and databases, changing the source does not instantly rewrite every copy.

Each layer can have its own key, TTL, invalidation mechanism, and revalidation rules.

A deployment that updates HTML but not asset hashes may combine new references with old resources.

A purge that targets one cache may leave another untouched.

A debugging session needs a map of memory.

Where can old state survive?

## Cache keys define alternate realities

A cache does not store only "the page."

It stores a representation under a key.

The key may include URL, headers, language, query parameters, device class, authorization state, or other dimensions.

If the key is incomplete, one user's representation can be served to another context.

If the key is too broad, hit rate collapses.

Cache design is therefore an exercise in deciding which differences matter.

Two requests considered equivalent by the key will share a remembered answer.

## Stale data can be deliberately useful

Some systems intentionally serve stale content when the origin is unavailable.

A slightly old weather tile, documentation page, or static asset can be better than total failure.

Other systems cannot tolerate the same staleness.

A bank balance, authorization decision, or active incident state may require stricter freshness.

There is no universal correct TTL.

Freshness is a product and risk decision.

## Caches make time part of correctness

In a non-cached mental model, correctness sounds timeless:

Is this value right?

With caching, the better question is:

Was this value valid when stored, and is it still acceptable to reuse under the freshness contract?

That is a more complicated definition of truth.

It is also how large systems remain practical.

## The fix is often provenance

When a stale result appears, operators need to know:

which cache served it,

how old the object is,

which key selected it,

which origin version produced it,

what freshness policy applies,

and whether revalidation occurred.

Headers, cache-status fields, object metadata, and deployment IDs turn mysterious staleness into a traceable history.

A cache is memory.

Memory is powerful because it lets the system avoid asking the same question repeatedly.

Memory is dangerous because the world can change while the memory remains valid under old rules.

Caching is yesterday's truth served today.

The engineering problem is deciding how old truth is allowed to become before it stops being useful.
