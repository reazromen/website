---
title: The Redis Streams Pending Entries List Is Your Work-in-Progress Ledger
url: /posts/redis-streams-pel-is-work-in-progress/index.html
date: '2026-09-26'
read_time: 8
excerpt: Consumer groups do not make a stream entry disappear when it is delivered.
  Until XACK succeeds, Redis tracks it as pending, which is what makes crashed-consumer
  recovery possible.
topic: redis-systems
tags:
- redis
- streams
- consumer-groups
- pel
draft: false
featured: false
language: en
eyebrow: Redis Streams · Redis systems note
outputs:
- url: /posts/redis-streams-pel-is-work-in-progress/index.html
  template: cms/templates/posts/posts--redis-streams-pel-is-work-in-progress--index.tpl
  source: cms/templates/posts/posts--redis-streams-pel-is-work-in-progress--index.json
---

Redis Streams consumer groups are often explained as “workers share messages.” The interesting state begins after a worker receives a message but before it finishes.

## Delivery is not acknowledgement

`XREADGROUP` with `>` delivers entries not previously delivered to another consumer in the group. Those entries become pending for that consumer until `XACK`.

```
stream entry
 -> delivered
 -> pending
 -> side effect
 -> XACK
 -> complete
```

## A crash leaves recoverable state

If the worker dies after delivery, the entry stays in the Pending Entries List. `XPENDING` shows pending ownership and idle time; `XAUTOCLAIM` can move sufficiently idle work to another consumer.

## At-least-once means duplicate effects are normal

If a worker writes to PostgreSQL and crashes before `XACK`, another consumer may process the same entry again. The queue recovered correctly; the application now needs idempotent side effects.

## PEL size is a production metric

A growing PEL can mean slow consumers, poison messages, downstream outages, repeated crashes or missing acknowledgements. Stream length alone will not reveal that because pending work has already been delivered.

## Retention and recovery are coupled

Streams can be trimmed to bound memory. If payloads are trimmed while group metadata still refers to pending IDs, recovery code must handle missing entries. Retention therefore needs to exceed realistic processing and retry windows.

## Consumer identity needs cleanup

Ephemeral pod names can create long lists of abandoned consumers. Use meaningful identities, monitor idle consumers and remove stale consumer records deliberately.

The stream tells you which events exist. The PEL tells you which events the system believes are currently being worked. Operate both as first-class state.

## Sources and further reading

- [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/)
- [Redis streaming use case](https://redis.io/docs/latest/develop/use-cases/streaming/)
