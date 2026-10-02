---
title: A Single Redis Hot Key Can Defeat the Point of a Cluster
url: /posts/redis-hot-key-can-beat-cluster/index.html
date: '2026-09-26'
read_time: 8
excerpt: Redis Cluster spreads hash slots across shards, not one key across shards.
  A single extremely popular key can saturate the shard that owns it while the rest
  of the cluster is mostly idle.
topic: redis-systems
tags:
- redis
- hot-key
- cluster
- sharding
draft: false
featured: false
language: en
eyebrow: Redis Cluster · Redis systems note
outputs:
- url: /posts/redis-hot-key-can-beat-cluster/index.html
  template: cms/templates/posts/posts--redis-hot-key-can-beat-cluster--index.tpl
  source: cms/templates/posts/posts--redis-hot-key-can-beat-cluster--index.json
---

Sharding is easy to overestimate. Redis Cluster distributes 16,384 hash slots across primaries, so independent keys can scale across nodes. But a single key still belongs to one slot and one primary.

If one global counter, leaderboard, session object, or cache entry receives a huge fraction of traffic, adding more unrelated shards does not divide that key's workload.

## Hot slot and hot key are not identical

A hot slot may contain many busy keys. One hot key can make its slot hot by itself. Redis has been improving tooling around both: slot statistics arrived earlier, atomic slot migration improved movement, and Redis 8.6 adds direct `HOTKEYS` detection.

## Cluster-wide CPU can hide the incident

Imagine six primaries at 20%, 18%, 22%, 19%, 21% and 98% CPU. The average looks survivable. The one shard owning the hot key has become the latency bottleneck for every other key in that shard.

## Read replicas are not a universal fix

Readonly traffic can sometimes be sent to replicas, but that changes consistency and routing. It does nothing for writes and may be wrong for reads that require the latest state.

## The data model may be too coarse

A global counter can often be striped into many counters and aggregated later. That gains write scalability by accepting more complex reads and temporarily distributed state.

```
counter:{global}:0
counter:{global}:1
...
counter:{global}:63
```

## Large values are a second kind of hot

A key can be hot by operations per second or by bytes per second. Repeatedly transferring a multi-megabyte object can saturate a shard even when command rate looks modest.

## Do not jump straight to MONITOR

Redis documentation warns that `MONITOR` is high impact. Start with shard CPU, slot statistics, `HOTKEYS`, key-size data, and client metrics. Sample commands only when the lower-impact evidence is insufficient.

## One indivisible key cannot be parallelized by adding nodes

If the application invariant requires one globally serialized object at extreme traffic, Redis is not failing to shard it. The data model itself requires concentration. The fix may be partitioning, batching, local caching, relaxed consistency, or a different coordination model.

## Sources and further reading

- [Redis 8.6 hot-key detection](https://redis.io/docs/latest/develop/whats-new/8-6/)
- [Redis observability: hot keys](https://redis.io/docs/latest/operate/rs/monitoring/observability/)
- [Redis Cluster scaling](https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/)
