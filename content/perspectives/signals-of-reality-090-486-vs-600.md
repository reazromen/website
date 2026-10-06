---
title: 486 Busy Here vs 600 Busy Everywhere
url: /posts/signals-of-reality-090-486-vs-600.html
date: '2026-05-02'
read_time: 7
excerpt: SIP 486 and 600 differ by scope. One reports local busyness; the other claims the caller should stop searching because all relevant locations are known to be busy.
topic: telecom-voip
tags:
- sip
- status-codes
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

Two SIP responses contain the same everyday word:

Busy.

One says 486 Busy Here.

The other says 600 Busy Everywhere.

The human-language difference sounds small.

Operationally, it is substantial.

[RFC 3261](https://www.rfc-editor.org/rfc/rfc3261.html) treats 486 as a local response when an end system cannot or will not accept the call. A 600 response is appropriate when the server knows no other end system can accept it.

The protocol is encoding scope.

## 486 leaves the search open

Imagine a SIP proxy has three registered contacts for one address.

Contact A returns 486.

That response says A is busy.

The proxy can still try B and C.

A caller may ultimately reach the user through another device.

If 486 were treated as a universal statement, the proxy would terminate the search too early.

The word *Here* preserves possibility.

## 600 tries to close the search

A 600 response is a global failure class in SIP.

Its meaning is stronger: the sender claims the user is busy everywhere relevant to the request.

That claim can justify stopping further attempts.

But a stronger response requires stronger knowledge.

An endpoint with visibility into only itself should not casually speak for every other possible contact.

Protocol correctness depends partly on matching message scope to knowledge scope.

## Distributed systems rarely have global knowledge for free

This is the deeper issue.

To say "everywhere" in a distributed system, some component has to know the relevant universe.

Which contacts exist?

Are they current?

Did registrations expire?

Are there alternative routes?

Could another domain accept the request?

Has state changed while the query was running?

Global statements are expensive because global knowledge is expensive.

SIP exposes this reality in its status vocabulary.

## A final response may be synthesized

Real PBXs and carriers do not always pass codes transparently.

A proxy can aggregate branches.

A B2BUA can terminate one dialog and create another.

A gateway can map PSTN causes into SIP responses.

A carrier can normalize outcomes to a smaller set.

The 600 or 486 received by the caller may therefore be a claim produced by an intermediary, not a direct report from the human's device.

That is why troubleshooting needs hop-by-hop traces.

The final code contains less history than the network experienced.

## Human language overstates the result

Both responses are often rendered as:

User busy.

That display is useful for people.

It also erases the distinction between local and global knowledge.

A user interface can compress because most callers do not need SIP semantics.

An engineer debugging routing absolutely does.

This is the recurring tension between usability and observability.

## Scope should travel with assertions

The lesson generalizes to monitoring and distributed data.

"Database unavailable"—from which client?

"Service down"—from which region?

"User offline"—according to which presence server?

"Record missing"—from which replica?

A statement without scope invites false universality.

SIP's 486 and 600 pair is useful because the protocol exposes the scope directly in the semantics.

Busy Here.

Busy Everywhere.

The difference is not vocabulary.

It is a statement about how much of the world the sender claims to know.
