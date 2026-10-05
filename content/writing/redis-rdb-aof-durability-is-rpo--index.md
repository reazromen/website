---
title: Redis RDB vs AOF Is Really an RPO Decision
url: /posts/redis-rdb-aof-durability-is-rpo/index.html
date: '2026-07-09'
read_time: 8
excerpt: RDB and AOF are not just file formats. They encode how much acknowledged
  state you are willing to lose, how much persistence overhead you accept, and how
  recovery should work.
topic: redis-systems
tags:
- redis
- rdb
- aof
- persistence
draft: false
featured: false
language: en
eyebrow: Redis Durability · Redis systems note
outputs:
- url: /posts/redis-rdb-aof-durability-is-rpo/index.html
  template: cms/templates/posts/posts--redis-rdb-aof-durability-is-rpo--index.tpl
  source: cms/templates/posts/posts--redis-rdb-aof-durability-is-rpo--index.json
---

The wrong way to choose Redis persistence is to ask whether RDB or AOF is better. The useful question is how much acknowledged state may disappear after a crash and how quickly the service must recover.

## RDB is a point-in-time snapshot

A snapshot is compact, portable and fast to load. The durability gap is the time since the last successful snapshot. If the host dies before the next snapshot, recent writes are not represented.

## AOF records the write stream

The Append Only File records mutating operations. Its fsync policy controls the loss window. The common every-second policy narrows potential loss dramatically compared with periodic snapshots, but it adds disk activity and rewrite work.

## Persistence is part of latency

Redis is in memory, but AOF fsync, RDB creation, fork and copy-on-write all interact with the operating system. Redis exposes delayed-fsync and latency events because persistence can show up in p99 response time.

## RDB and AOF can complement each other

Redis documentation recommends both for stronger data safety. AOF can provide a tighter recovery point; RDB remains useful for backups and restart/recovery workflows.

## Persistence is not backup

An AOF stored on the same failed disk is not an off-host backup. A snapshot replicated to an independent failure domain is a different control. Likewise, replication copies logical operations and can faithfully replicate accidental deletes.

## Define RPO and RTO

```
RPO = maximum acceptable acknowledged write loss
RTO = maximum acceptable recovery time
failure scope = process / host / AZ / operator / account
```

Then choose snapshot cadence, AOF fsync, replication and off-host backup around those requirements.

## Test abrupt failure, not graceful restart

Kill the process, simulate disk pressure, restore onto a clean host and measure load time with the real dataset size. Durability is not the config file; it is the observed recovery behavior.

## Sources and further reading

- [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
- [Redis Cloud persistence](https://redis.io/docs/latest/operate/rc/databases/configuration/data-persistence/)
