---
title: Status Is Not State
url: /posts/signals-of-reality-087-status-is-not-state.html
date: '2026-07-30'
read_time: 6
excerpt: A status is a representation emitted by some component at some time. The underlying system state can be richer, newer, or different.
topic: systems-thinking
tags:
- status
- state
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · Protocols Lie Carefully'
editorial_batch: signals-of-reality-200
---

"Online."

"Healthy."

"Busy."

"Ready."

These words look like states.

Usually they are statuses: compact representations of state chosen by an interface.

That distinction sounds linguistic until something goes wrong.

A service can report healthy while a dependency is unavailable.

A user can appear online while their device has disconnected.

A database can report a replica as running while it is minutes behind.

Status is not state.

## State is larger than the label

A process has memory usage, open sockets, pending work, locks, caches, configuration, recent errors, dependency connections, and internal queues.

A health endpoint might reduce all of that to:

`{"status":"ok"}`

The response can be perfectly correct under its own definition.

Perhaps "ok" means the process loop is responsive.

It says nothing about every other dimension unless the contract explicitly includes them.

The label is a projection.

## Status has a timestamp

A status also belongs to a moment.

A monitoring system samples every thirty seconds.

A failure begins one second after the last successful probe.

For the next twenty-nine seconds, the dashboard displays a true statement about the past as if it were a statement about the present.

This is unavoidable in sampled systems.

Freshness therefore belongs to status semantics.

A status without an observation time is less informative than it appears.

## Different observers can disagree

A load balancer sees a backend as healthy because its TCP check succeeds.

The application sees its database as unreachable.

A user sees requests timing out.

An orchestration system sees the container as running.

Which is the real state?

There is no single status label that contains all perspectives.

Each observer measures a different relation.

The system state includes the fact that those observers disagree.

## Derived status can hide thresholds

Many statuses are computed.

Green if error rate < 1%.

Amber if < 5%.

Red otherwise.

Now the status depends on thresholds, aggregation windows, and missing-data policy.

A service at 0.99% errors is green.

At 1.01%, amber.

The underlying process barely changed.

The classification did.

This is why dashboards should make it possible to inspect the measurement behind the status.

## State machines need explicit transitions

Protocols often handle status better than dashboards because they model state transitions.

A SIP dialog moves through defined stages.

A TCP connection moves through states.

A job can be queued, running, succeeded, failed, or cancelled.

The labels become useful because transition rules constrain what they mean.

Even then, the state machine is a model.

A "running" job may be blocked forever.

A "connected" socket may carry no useful data.

The model tells us which layer of state is represented.

## Operational systems need evidence beneath the label

When a status matters, preserve:

who produced it,

when,

from which measurements,

under which thresholds,

and what lower-level evidence supports it.

This turns a colored icon back into something testable.

A status is not useless because it is compressed.

Compression is why it is useful.

The mistake is treating the compressed representation as if nothing were lost.

Status is not state.

It is a statement about state, spoken by one observer through one interface at one time.
