---
title: DNS Answers Are Views of Reality
url: /posts/signals-of-reality-095-dns-answers-views-reality.html
date: '2026-01-05'
read_time: 7
excerpt: DNS answers depend on resolver caches, authority, geography, time, and policy. Two clients can receive different correct answers to the same name.
topic: networking
tags:
- dns
- cache
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

"What IP does this domain have?"

The question sounds singular.

DNS often answers in plural.

Different resolvers can return different addresses.

The same resolver can return a different answer later.

A CDN can intentionally vary answers by geography.

A cached answer can remain valid after the authoritative data changed.

DNS is not a global phone book read from one page at one instant.

It is a distributed naming system with time built into the answer.

## Authority and observation are different

An authoritative server publishes data for a zone.

A recursive resolver asks on behalf of clients and caches what it learns.

A client usually asks the resolver, not the authoritative server directly.

That means the client sees a resolver's current view.

The view can be completely standards-compliant while lagging behind a recent authoritative change until TTLs expire.

The answer is not false.

It is temporally scoped.

## TTL is an epistemic lease

DNS records carry time-to-live values.

A resolver may reuse a cached answer while the TTL remains valid.

Operationally, this reduces latency and load.

Conceptually, TTL says:

you may treat this information as sufficiently current for this long without asking again.

That is not a guarantee the world will not change.

It is a permission to tolerate bounded staleness.

Distributed systems are full of such leases.

## Different users can receive different addresses intentionally

Modern DNS often supports traffic steering.

A service can answer with endpoints near the client.

It can direct traffic away from unhealthy regions.

It can return different records for different networks.

Now two users ask the same name and receive different addresses at the same time.

Both answers can be correct under the service's policy.

The name identifies a service more abstractly than a single machine.

## Local configuration creates another view

Operating systems may have local hosts files.

Enterprise resolvers may implement split DNS.

VPNs may install different resolvers.

Containers may use internal names that do not exist publicly.

The phrase "DNS says X" therefore lacks a crucial detail:

which resolver from which network context?

A debugging command run on a laptop may not reproduce what a server inside a private network resolves.

Perspective is part of the result.

## Caches preserve history

A migration changes an A record.

Some clients switch quickly.

Others keep the old endpoint.

For a period, the network contains multiple presents.

Operators sometimes call this DNS propagation, but the mechanism is often more specifically cache expiry across distributed resolvers.

The old answer survives because the system was designed to remember.

Caching trades immediacy for efficiency.

## A DNS answer is evidence, not essence

The domain name is not identical to the returned IP.

The IP is not necessarily the only endpoint.

The answer is not necessarily current at the authority.

It is a structured response generated through a chain of authority, recursion, cache, policy, and time.

That chain is why DNS scales.

It is also why debugging requires context.

Ask:

Which record type?

Which resolver?

Authoritative or cached?

What TTL?

Which network?

Which time?

DNS answers are views of reality.

Reliable operations begin when we stop demanding that every distributed observer share the same view at the same instant.
