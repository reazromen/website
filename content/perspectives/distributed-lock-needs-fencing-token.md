---
title: A Distributed Lock Without Fencing Can Let a Dead Worker Come Back and Corrupt
  State
url: /posts/distributed-lock-needs-fencing-token.html
date: '2026-09-26'
read_time: 8
excerpt: A lease can expire while its old owner is paused rather than dead. If that
  process later resumes, the lock service may have moved on—but the storage system
  can still accept stale writes unless it has a fencing mechanism.
topic: ''
tags:
- distributed-lock
- fencing
- leases
- consistency
draft: false
featured: false
language: en
eyebrow: Distributed Systems · systems note
outputs:
- url: /posts/distributed-lock-needs-fencing-token.html
  template: cms/templates/posts/posts--distributed-lock-needs-fencing-token.tpl
  source: cms/templates/posts/posts--distributed-lock-needs-fencing-token.json
---

The intuitive model of a lock is borrowed from one process.

Thread A holds a mutex. Thread B cannot enter the critical section. When A releases it, B proceeds.

A distributed lease looks similar in an API and behaves differently under failure because the lock service and the resource being protected do not share one clock or one failure detector.

## “Expired” does not mean the old worker stopped[#](#expired-does-not-mean-the-old-worker-stopped)

Imagine worker A acquires a 30-second lease and begins writing a file or updating an external service.

Then A pauses for 45 seconds because of a long GC pause, scheduler stall, VM suspension, network partition, or overloaded host.

The lock service expires A's lease. Worker B acquires the lock and starts correct new work.

Then A wakes up.

From A's local point of view, it can continue from the instruction after the pause. If it writes to the protected resource, two logical owners have now acted even though the lock service never believed both owned the lease at the same time.

## Renewal checks do not close every race[#](#renewal-checks-do-not-close-every-race)

You can renew leases frequently and check ownership before each operation.

But there is always a gap between “check succeeded” and “side effect reached the resource.” The process can pause or the network can delay the request inside that gap.

The protected resource needs a way to reject stale owners.

## Fencing tokens move the check to the resource[#](#fencing-tokens-move-the-check-to-the-resource)

A fencing token is a monotonically increasing number issued on lock acquisition.

```
A acquires -> token 33
A pauses
lease expires
B acquires -> token 34
B writes with 34
A resumes and writes with 33
storage rejects 33 because 34 was already seen
```

The critical property is that the storage/resource side remembers the highest accepted token and refuses older tokens.

Martin Kleppmann's classic distributed-lock analysis makes exactly this point: fencing only works if the resource participates.

## A perfect lock service cannot control an external resource by itself[#](#a-perfect-lock-service-cannot-control-an-external-resource-by-itself)

Even a linearizable lock service can tell you accurately who currently owns a lock.

It cannot reach backward in time and stop a stale request already delayed in a queue, TCP buffer, paused process, or downstream service.

That is why “our consensus system guarantees one lock owner” and “the critical resource cannot receive stale writes” are different properties.

## The token must be ordered, not merely unique[#](#the-token-must-be-ordered-not-merely-unique)

A UUID identifies an owner but does not let the resource determine which owner is newer.

Fencing requires monotonic ordering: 34 is newer than 33.

That order can come from the coordination service, a database sequence, an epoch number, or another strongly consistent monotonic source.

## The downstream interface has to carry the fence[#](#the-downstream-interface-has-to-carry-the-fence)

This is where designs often become difficult.

If the protected resource is your database table, adding a `fence_epoch` comparison may be straightforward.

If it is an object store, legacy filesystem, third-party API, or physical device that cannot validate tokens, the lock cannot give the same stale-writer guarantee by itself.

You may need an intermediary service that owns the resource and enforces epochs, or redesign the operation to be idempotent/commutative.

## Idempotency and fencing solve different failures[#](#idempotency-and-fencing-solve-different-failures)

An idempotency key prevents the same logical operation from being applied twice.

A fencing token prevents an older owner from applying a new stale operation after a newer owner has taken over.

Many systems benefit from both.

## Hazelcast exposes the concept directly[#](#hazelcast-exposes-the-concept-directly)

Hazelcast's `FencedLock` is a concrete example of a lock API designed around these distributed-system constraints. Its documentation emphasizes that asynchronous networks cannot perfectly distinguish a slow process from a failed one, and fencing tokens are used to make resource access safer.

The name is useful because it keeps the requirement visible at the API boundary.

## Leases are still valuable[#](#leases-are-still-valuable)

None of this means leases are broken.

They are excellent for leader election, work ownership, cleanup, and limiting how long failed owners block progress.

The mistake is assuming the lease alone makes all external side effects mutually exclusive.

## Model the pause explicitly[#](#model-the-pause-explicitly)

The easiest test for a distributed lock design is not “what if the worker crashes?”

Ask:

**What if the worker freezes long enough to lose the lease, another worker completes newer work, and the old worker resumes exactly where it stopped?**

If the answer is “the old write still succeeds,” the resource is not fenced.

## Sources and further reading[#](#sources-and-further-reading)

- [Martin Kleppmann: How to do distributed locking](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
- [Hazelcast FencedLock documentation](https://docs.hazelcast.com/hazelcast/5.0/data-structures/fencedlock)
- [Hazelcast CP Subsystem](https://docs.hazelcast.com/hazelcast/5.5/cp-subsystem/cp-subsystem)
