---
title: Redis Cluster Hash Tags Are a Data-Model Decision, Not a Syntax Trick
url: /posts/redis-cluster-hash-tags-are-data-model/index.html
date: '2023-01-10'
read_time: 8
excerpt: Hash tags let related keys share one slot so multi-key commands and scripts
  can remain atomic. Overuse them and you can create hot slots that undo the cluster's
  distribution.
topic: redis-systems
tags:
- redis
- cluster
- hash-slots
- hash-tags
draft: false
featured: false
language: en
eyebrow: Redis Cluster · Redis systems note
outputs:
- url: /posts/redis-cluster-hash-tags-are-data-model/index.html
  template: cms/templates/posts/posts--redis-cluster-hash-tags-are-data-model--index.tpl
  source: cms/templates/posts/posts--redis-cluster-hash-tags-are-data-model--index.json
---

The braces in `user:{123}:profile` look like naming syntax. In Redis Cluster they are placement architecture.

## Cluster distributes hash slots

Redis maps keys into 16,384 slots. Multi-key commands, transactions and server-side scripts usually require the participating keys to live in one slot. A shared hash tag deliberately colocates them.

## Colocation spends distribution

If profile, settings and sessions for one user share `{123}`, per-user atomic operations become easy. But one extremely large or busy user can now concentrate all of that activity on one shard.

## A global tag builds a one-slot application

Putting `{app}` into every key can silence CROSSSLOT errors while sending the entire dataset to one hash slot. Functional tests pass; horizontal scale quietly disappears.

## Define the atomic boundary first

Ask which keys truly require one atomic operation. Keys that only need eventual coordination do not necessarily belong together.

## Moving the slot does not split the entity

Redis can migrate hot slots between primaries, but migration only relocates the hotspot. If one tenant has outgrown a shard, the application partition key itself may need to change.

## Scripts inherit the placement model

Functions and Lua scripts make multi-key atomic work convenient, which is exactly why key placement should be designed before scripting. Advanced cross-slot flags exist, but normal cluster design should keep atomic key groups in one slot.

I document every hash tag with its reason for colocation. If the reason is only “the client gave CROSSSLOT,” the key model probably deserves another look.

## Sources and further reading

- [Redis Cluster scaling and hash tags](https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/)
- [Redis Lua API cluster behavior](https://redis.io/docs/latest/develop/programmability/lua-api/)
