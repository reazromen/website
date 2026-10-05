---
title: Redis Functions Are Atomic — Which Is Exactly Why Slow Ones Hurt
url: /posts/redis-functions-atomic-does-not-mean-cheap/index.html
date: '2024-09-15'
read_time: 8
excerpt: Lua scripts and Redis Functions avoid races and network round trips by executing
  atomically on the server. The same property means long-running server-side code
  blocks unrelated work.
topic: redis-systems
tags:
- redis
- functions
- lua
- atomicity
draft: false
featured: false
language: en
eyebrow: Redis Programmability · Redis systems note
outputs:
- url: /posts/redis-functions-atomic-does-not-mean-cheap/index.html
  template: cms/templates/posts/posts--redis-functions-atomic-does-not-mean-cheap--index.tpl
  source: cms/templates/posts/posts--redis-functions-atomic-does-not-mean-cheap--index.json
---

Server-side code in Redis is valuable because it can read state, make a decision and update several structures without another client interleaving work in the middle.

The same atomicity has a direct cost: while a script is executing, Redis has to preserve that uninterrupted semantic.

## Move decisions, not workloads

Good server-side logic is usually small: read a handful of keys, check an invariant, update a counter/hash/set and return a compact result.

Bad server-side logic looks like analytics, large keyspace scanning or unbounded iteration.

## Functions improve deployment over EVAL

Redis Functions, introduced in Redis 7, provide managed libraries and named calls. That is operationally cleaner than clients shipping script bodies and recovering from script-cache misses.

## Atomic does not mean durable

A Function can perform several writes atomically relative to concurrent clients, while those writes still inherit Redis replication and persistence guarantees. Concurrency atomicity and crash durability are different properties.

## Cluster placement still matters

Multi-key Functions should normally operate on keys in the same hash slot. If the function keeps fighting CROSSSLOT rules, the data model probably disagrees with the cluster model.

## Declare read-only behavior when it is true

Read-only calls and flags help Redis enforce where code can execute, including replica/OOM conditions.

## Version functions like application code

Keep source in Git, test against realistic data sizes, deploy deliberately and record which library version is loaded. Do not let the only copy of production logic live inside a server.

Redis Functions are strongest when they encode a small atomic invariant. If the code is big enough that you have to ask how long the server can afford to be blocked, it is probably doing too much.

## Sources and further reading

- [Redis Functions](https://redis.io/docs/latest/develop/programmability/functions-intro/)
- [Redis Lua scripting](https://redis.io/docs/latest/develop/programmability/eval-intro/)
- [Redis Lua API](https://redis.io/docs/latest/develop/programmability/lua-api/)
