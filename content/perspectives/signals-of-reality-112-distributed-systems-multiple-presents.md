---
title: Distributed Systems Have Multiple Presents
url: /posts/signals-of-reality-112-distributed-systems-multiple-presents.html
date: '2026-03-05'
read_time: 7
excerpt: Different nodes observe events at different times and with different clocks. A distributed system does not automatically share one perfectly synchronized present.
topic: systems-thinking
tags:
- distributed-systems
- clock
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

Node A says the record exists.

Node B says it does not.

A monitoring dashboard says both statements were made at 10:00:00.

Which node is living in the present?

The question assumes a global now that distributed systems do not receive for free.

Messages take time.

Clocks drift.

Replication lags.

Observers learn about events in different orders.

The system contains multiple local presents.

## Wall clocks are not a universal ordering device

Computers synchronize clocks using protocols such as NTP, but synchronization is approximate.

Two clocks can differ.

Network delay varies.

A clock can step or slew.

If event A is stamped 10:00:00.100 on one host and event B is stamped 10:00:00.090 on another, we cannot automatically conclude B happened first.

The timestamp includes clock error.

Ordering needs more than displayed time.

## Messages define knowledge

Suppose A writes a value and sends an update to B.

Between the local commit and B receiving the message, two facts coexist:

A knows the new value.

B still knows the old value.

Neither node is hallucinating.

They have different information histories.

Distributed computing is built around this unavoidable delay.

Replication protocols decide how much divergence is acceptable and how it is reconciled.

## "Current" depends on observer

A user reading from one replica can see version 7.

Another user reads version 8.

A third writes version 9.

The phrase "current value" becomes ambiguous until we specify consistency guarantees and observation path.

Strong consistency mechanisms reduce this ambiguity by coordinating more.

That coordination costs latency, availability under some failures, or system complexity.

A shared present is expensive.

## Logical clocks capture relation, not time of day

Distributed systems use concepts such as Lamport clocks and vector clocks to reason about ordering without pretending wall clocks are perfect.

The goal is not to know exact universal time.

It is to know relationships such as:

this event happened before that one,

these events may be concurrent,

this version includes that update.

Causal order can matter more than clock time.

## Dashboards flatten local presents

An observability backend collects telemetry from many machines and draws one time axis.

That visualization is convenient.

It can also imply a precision the sources do not have.

Clock skew can make effects appear before causes.

Ingestion delay can place old events beside current ones.

Buffering can reorder logs.

A shared graph is a reconstruction of distributed time.

Good incident analysis considers clock and pipeline uncertainty when sequence matters.

## Users experience consistency as product behavior

A user changes a profile picture.

One screen updates immediately.

Another shows the old image for ten seconds.

The product has exposed multiple presents.

Sometimes that is acceptable.

Sometimes it feels broken.

Consistency is not merely a database property.

It is a user-visible decision about how quickly observers should converge.

## There is no magic global observer

A distributed system is made of components that communicate through delayed channels.

Any global view is itself constructed by collecting local views.

By the time the collector assembles them, the system has already changed.

This does not make distributed state unknowable.

It means knowledge comes with time and perspective.

Distributed systems have multiple presents.

Engineering is the art of deciding where those presents must agree, how quickly, and at what cost.
