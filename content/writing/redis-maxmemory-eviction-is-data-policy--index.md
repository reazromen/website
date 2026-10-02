---
title: Redis maxmemory Is Not a Capacity Setting — It Is a Data-Loss Policy
url: /posts/redis-maxmemory-eviction-is-data-policy/index.html
date: '2026-09-26'
read_time: 8
excerpt: When Redis reaches maxmemory, the eviction policy decides which data may
  disappear or whether new writes should fail. That makes memory configuration part
  of application correctness.
topic: redis-systems
tags:
- redis
- maxmemory
- eviction
- caching
draft: false
featured: false
language: en
eyebrow: Redis Memory · Redis systems note
outputs:
- url: /posts/redis-maxmemory-eviction-is-data-policy/index.html
  template: cms/templates/posts/posts--redis-maxmemory-eviction-is-data-policy--index.tpl
  source: cms/templates/posts/posts--redis-maxmemory-eviction-is-data-policy--index.json
---

Redis memory limits are often configured like container limits: pick a number, watch the graph, and scale when it approaches the top. That misses the important part.

`maxmemory` tells Redis when it must make a semantic decision. Once the limit is reached, the configured eviction policy determines whether keys are removed or writes are rejected.

## First classify the data

If Redis is only a cache for data that exists elsewhere, eviction is expected. If Redis holds sessions, queues, locks, counters, or workflow state, silent eviction can change application behavior.

The useful review question is simple: **can this key disappear without coordination?**

## allkeys and volatile are different contracts

`allkeys-*` policies can evict any key. `volatile-*` policies only consider keys with a TTL. Under a volatile policy, persistent keys are effectively protected, so a database may be nearly full while very little of it is actually evictable.

## LRU, LFU and LRM encode different assumptions

LRU keeps recently used data. LFU favors frequently used data. Redis 8.6 adds least-recently-modified policies, useful when modification recency matters more than read recency. These are workload models, not interchangeable switches.

## Cluster memory is per shard

A cluster can show comfortable aggregate memory while one shard reaches its own limit first because the key distribution is uneven. That shard can start evicting even though the database-wide number looks healthy.

## Eviction can overload the origin

A cache hit is cheap; a miss may trigger a database query, API call, or expensive recomputation. If memory pressure evicts a popular key and thousands of callers miss at once, Redis can indirectly create an outage in the system it was protecting.

This is why eviction design should include stampede protection, TTL jitter, stale serving, and source-side load shedding.

## Memory policy is business logic in disguise

I would classify keys into rebuildable cache, session/state, coordination, queue/stream, derived aggregate, and durable business data. Then decide which classes may disappear, which must reject writes instead, and which should not live in an evicting Redis at all.

Once memory is full, Redis must choose a failure mode. `maxmemory-policy` is where that choice becomes explicit.

## Sources and further reading

- [Redis eviction policy](https://redis.io/docs/latest/operate/rs/databases/memory-performance/eviction-policy/)
- [Redis 8.6 memory and eviction changes](https://redis.io/docs/latest/develop/whats-new/8-6/)
