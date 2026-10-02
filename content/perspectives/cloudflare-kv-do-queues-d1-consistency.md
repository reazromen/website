---
title: Cloudflare KV, Durable Objects, Queues, and D1 Fail Differently Because Their
  Consistency Models Differ
url: /posts/cloudflare-kv-do-queues-d1-consistency.html
date: '2026-09-26'
read_time: 9
excerpt: A lost counter, duplicate job, stale read, or runaway write bill is usually
  not 'a Cloudflare bug.' Each storage primitive makes different consistency and delivery
  promises, so the same application pattern fails differently on each one.
topic: ''
tags:
- cloudflare
- durable-objects
- workers-kv
- queues
draft: false
featured: false
language: en
eyebrow: Edge & Distributed Systems · systems note
outputs:
- url: /posts/cloudflare-kv-do-queues-d1-consistency.html
  template: cms/templates/posts/posts--cloudflare-kv-do-queues-d1-consistency.tpl
  source: cms/templates/posts/posts--cloudflare-kv-do-queues-d1-consistency.json
---

Cloudflare's edge primitives make it easy to put state close to application code. They do not make state semantics disappear.

The fastest way to create a confusing system is to choose KV, Durable Objects, Queues, or D1 because the API looks convenient and then assume they all behave like a single strongly consistent database.

## Workers KV is optimized for read distribution[#](#workers-kv-is-optimized-for-read-distribution)

Workers KV is globally distributed and eventually consistent.

Cloudflare documents that changes may take 60 seconds or more to become visible at other locations, especially where an older value was recently cached.

That is an excellent trade for configuration, assets, feature metadata, or read-heavy data tolerant of staleness.

It is a bad primitive for a global increment implemented as:

```
v = KV.get("counter")
KV.put("counter", v + 1)
```

Two locations can read the same old value and overwrite each other.

## Durable Objects give one logical owner a serialization point[#](#durable-objects-give-one-logical-owner-a-serialization-point)

A Durable Object routes requests for a given object identity to one logical instance, making it useful for coordination, per-room state, counters, sessions, rate limits, or workflows that need a consistent owner.

That changes the race model. Instead of many edge locations independently updating cached KV state, requests for the same object can be serialized through one owner.

The tradeoff is hot-key concentration: if the entire world maps to one object ID, you built a single coordination bottleneck on purpose.

## Queues are about delivery, not uniqueness[#](#queues-are-about-delivery-not-uniqueness)

Cloudflare Queues provides at-least-once delivery by default.

That means a message can be delivered more than once. Retries can also redeliver an entire batch unless individual messages have already been acknowledged.

So consumers should be idempotent whenever duplicate side effects matter.

Use a stable event ID as a database primary key or idempotency key when sending email, charging payments, provisioning resources, or triggering external APIs.

## Retries can become a cost amplifier[#](#retries-can-become-a-cost-amplifier)

A broken consumer that repeatedly retries is not just a reliability problem. Each retry is work and can be billable.

A worse pattern is recursion: a queue consumer accidentally writes the same logical job back to the queue unconditionally, multiplying messages.

Cost observability therefore belongs beside error observability. Track messages produced, consumed, retried, sent to DLQ, and downstream writes per original event.

## D1 is a relational database, not a replacement for every coordination primitive[#](#d1-is-a-relational-database-not-a-replacement-for-every-coordination-primitive)

D1 gives SQL tables and transactional database operations, which is the right model for many relational application states.

But using a SQL database does not automatically solve global workflow ownership, queue redelivery, or cached configuration semantics.

You can combine the primitives:

```
Queue -> Durable Object coordination -> D1 transaction
                                  -> KV read cache / distribution
```

The point is not that this exact chain is universally correct. The point is that each layer has a reason to exist.

## Choose by invariant[#](#choose-by-invariant)

Start from what must be true.

- “All locations can tolerate stale reads” -> KV may fit.
- “Updates for one entity must be serialized” -> Durable Object may fit.
- “Work must eventually be processed and duplicates are acceptable/idempotent” -> Queue may fit.
- “I need relational constraints and transactions” -> D1 may fit.

Do not start from product names.

## Hot keys are architecture[#](#hot-keys-are-architecture)

A global counter mapped to one Durable Object gets strong coordination at the price of one owner handling that key's traffic.

Sharding the counter improves throughput but changes read semantics because totals now require aggregation.

That is the same distributed-systems tradeoff in a convenient serverless form: stronger coordination narrows concurrency; distribution requires reconciliation.

## Make side effects idempotent[#](#make-side-effects-idempotent)

At-least-once delivery, client retries, network timeouts, and ambiguous responses all create cases where “did the write happen?” is uncertain.

Attach operation IDs to side effects and make the receiving system reject duplicates when possible.

This is cheaper than trying to prove every request is delivered exactly once across multiple distributed systems.

## Consistency models become cost models[#](#consistency-models-become-cost-models)

Choosing the wrong primitive produces more than wrong data.

It can create repeated retries, write amplification, hot-object contention, excessive reads, or cache churn.

Correctness and cost often fail together because both are consequences of the same state model.

The useful question is not “which Cloudflare database is fastest?” It is “what invariant does this piece of state require, and which primitive actually promises it?”

## Sources and further reading[#](#sources-and-further-reading)

- [Cloudflare Workers KV: consistency model](https://developers.cloudflare.com/kv/concepts/how-kv-works/)
- [Cloudflare Queues: delivery guarantees](https://developers.cloudflare.com/queues/reference/delivery-guarantees/)
- [Cloudflare Queues: batching, retries and delays](https://developers.cloudflare.com/queues/configuration/batching-retries/)
- [Cloudflare Durable Objects documentation](https://developers.cloudflare.com/durable-objects/)
