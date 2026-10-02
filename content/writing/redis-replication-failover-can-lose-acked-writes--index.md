---
title: Redis Replication Can Lose Acknowledged Writes During Failover
url: /posts/redis-replication-failover-can-lose-acked-writes/index.html
date: '2026-09-26'
read_time: 8
excerpt: Redis replication is asynchronous by default. WAIT reduces the risk window,
  but replica acknowledgements do not turn Sentinel or Cluster failover into a strongly
  consistent system.
topic: redis-systems
tags:
- redis
- replication
- sentinel
- failover
draft: false
featured: false
language: en
eyebrow: Redis High Availability · Redis systems note
outputs:
- url: /posts/redis-replication-failover-can-lose-acked-writes/index.html
  template: cms/templates/posts/posts--redis-replication-failover-can-lose-acked-writes--index.tpl
  source: cms/templates/posts/posts--redis-replication-failover-can-lose-acked-writes--index.json
---

A successful Redis write response is easy to interpret as “the data is safe.” In a replicated deployment, the default acknowledgement means something narrower.

## The primary normally does not wait

Redis sends a replication stream to replicas asynchronously. The primary can acknowledge a client write before every replica has processed it.

## Failover can select a replica that is behind

If the primary dies immediately after the acknowledgement, Sentinel or Cluster promotes an available replica. If the selected replica did not receive the latest write, the new primary can be behind what the client was told succeeded.

## WAIT narrows the window

`WAIT` lets a client wait until a chosen number of replicas acknowledge the relevant replication offset. That gives the write more copies before the application proceeds.

Redis documentation is explicit: this improves real-world safety but does not make the deployment a strongly consistent CP system. Some failover scenarios can still lose an acknowledged write.

## Replication is not persistence

A replica may have the write in memory while its AOF/RDB durability has a different failure window. Multi-node failure therefore depends on persistence too.

## Classify writes

Cache entries may be freely lost. Rate-limit counters may tolerate some inconsistency. Money movement or unique business events usually need a stronger source of truth than asynchronous Redis replication alone.

## Test under real write load

Generate unique sequence numbers, kill or isolate the primary, allow automatic failover, then compare the highest client-acknowledged sequence with the promoted primary. That gives you evidence for your exact configuration.

Failover time measures availability. Acknowledged-write loss measures consistency/durability. They deserve separate SLOs.

## Sources and further reading

- [Redis replication](https://redis.io/docs/latest/manual/replication/)
- [Redis WAIT](https://redis.io/docs/latest/commands/wait/)
- [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/)
