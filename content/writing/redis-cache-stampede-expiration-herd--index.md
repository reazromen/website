---
title: A Redis Cache Miss Can Become a Database Outage
url: /posts/redis-cache-stampede-expiration-herd/index.html
date: '2021-08-02'
read_time: 8
excerpt: When a popular key expires, many callers can observe the same miss and rebuild
  the value simultaneously. Stampede protection is admission control for the source
  of truth.
topic: redis-systems
tags:
- redis
- cache-stampede
- singleflight
- ttl
draft: false
featured: false
language: en
eyebrow: Caching Architecture · Redis systems note
outputs:
- url: /posts/redis-cache-stampede-expiration-herd/index.html
  template: cms/templates/posts/posts--redis-cache-stampede-expiration-herd--index.tpl
  source: cms/templates/posts/posts--redis-cache-stampede-expiration-herd--index.json
---

A cache can remove most database traffic and still become the trigger for a database incident.

Imagine thousands of requests per second for one popular object. While the Redis key exists, the origin barely notices. At expiration, every caller can see the same miss before any one caller finishes rebuilding it.

## One loader, many waiters

A short-lived Redis lock can let one caller become the loader while others briefly wait, serve stale data or retry the cache. Redis's cache-aside examples include this pattern with `SET NX PX` and a Lua release check.

## Ownership matters on unlock

If the lock expires and another process acquires it, the old loader must not delete the new owner's lock. Store a unique token and atomically compare-and-delete.

## Soft TTL is often better than hard expiry

Keep an object available beyond its freshness window. After the soft TTL, one worker refreshes while other callers receive slightly stale data. The hard TTL is later and represents the actual “do not serve this anymore” boundary.

## Jitter prevents mass expiry

If thousands of keys receive the same TTL during one deployment, they can expire together later. Add random jitter so refresh load is spread over time.

## Negative caching protects the origin too

Repeated requests for nonexistent objects can generate the same thundering herd. A short negative-cache TTL can absorb that load when the product tolerates temporary staleness for new objects.

## Cold start needs global control

Per-key locking is not enough after a full cache flush because thousands of different keys can all miss once. Limit total rebuild concurrency, warm critical keys and keep a degraded/stale path when possible.

Cache hit ratio tells you steady-state efficiency. Miss amplification tells you whether one expiry can take the source database down.

## Sources and further reading

- [Redis cache-aside and stampede protection](https://redis.io/docs/latest/develop/use-cases/cache-aside/redis-py/)
- [Redis client-side caching](https://redis.io/docs/latest/develop/clients/client-side-caching/)
