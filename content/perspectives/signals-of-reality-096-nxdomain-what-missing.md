---
title: "NXDOMAIN: What Exactly Is Missing?"
url: /posts/signals-of-reality-096-nxdomain-what-missing.html
date: '2026-08-14'
read_time: 7
excerpt: NXDOMAIN is a DNS statement about a queried name, not a universal declaration that every related service, host, or record is absent.
topic: networking
tags:
- dns
- unknown
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

A resolver returns NXDOMAIN.

The name does not exist.

That sounds final.

But even in DNS, we need to ask what exactly the response is denying.

NXDOMAIN is a statement about the queried domain name in the DNS namespace. It is not a general-purpose declaration that the machine, organization, service, or idea associated with that name does not exist.

## Names are representations

Suppose `api.example.com` returns NXDOMAIN.

The company may still exist.

The API may still exist under another name.

The service may be reachable by IP.

An internal resolver may know a private version of the name.

A typo may have selected the wrong namespace.

The negative answer applies to a name under a particular DNS view.

It does not erase the underlying system.

## Negative answers can be cached

DNS supports negative caching. [RFC 2308](https://www.rfc-editor.org/rfc/rfc2308.html) specifies how resolvers can cache knowledge that a name or record does not exist.

That means absence has a lifetime.

A name can be created at the authoritative source while some resolvers continue serving an earlier negative result until cache rules permit refresh.

The resolver is not inventing an answer.

It is reusing a previously valid observation.

Distributed memory turns past absence into present behavior.

## Name error and missing record are not identical

DNS has an important distinction between a name that does not exist and an existing name that simply lacks the requested record type.

Ask for an AAAA record and receive no data: that is not necessarily the same as NXDOMAIN.

The name may exist with A, MX, TXT, or other records.

This is one of those details that becomes operationally important when people simplify every failed DNS lookup to "domain missing."

The response vocabulary contains more structure than the human summary.

## Resolver perspective matters

A corporate network can run split-horizon DNS.

Inside the network, `db.internal.example` resolves.

Outside, it returns NXDOMAIN.

Both answers can be intentional.

Which one is correct?

Correct for which client context?

DNS names do not have to produce one global answer for all observers.

The namespace can be deliberately partitioned by policy.

## DNSSEC changes confidence, not ontology

Authenticated denial of existence through DNSSEC can provide cryptographic evidence that the authoritative zone asserts a name or record is absent.

That is stronger evidence about origin and integrity.

It still does not make the DNS namespace identical to physical reality.

Cryptography can tell us who signed the statement and that it was not altered.

It cannot turn a naming claim into a universal fact about the world.

## Operational debugging should ask one level lower

When NXDOMAIN appears unexpectedly, inspect:

which resolver answered,

whether the response was cached,

whether the authoritative zone contains the name,

whether search domains changed the query,

whether a VPN or container changed resolver configuration,

and whether the intended name was actually queried.

The visible error is often only the last line of a longer resolution process.

NXDOMAIN is a strong and useful DNS answer.

It means the resolver is telling you that, for the relevant query and view, the domain name does not exist.

The word *name* matters.

The protocol is describing its map.

It is not declaring the territory empty.
