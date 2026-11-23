---
title: Running Is Not Healthy
url: /posts/signals-of-reality-104-running-not-healthy.html
date: '2026-07-04'
read_time: 7
excerpt: A running process has satisfied a very low bar. It can be deadlocked, saturated, disconnected, stale, or unable to make useful progress.
topic: observability
tags:
- health-checks
- runtime
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

`systemctl status` says active.

The container says running.

The process has a PID.

The product is unusable.

There is no contradiction.

Running is a process state.

Healthy is an operational claim.

## A process can live without making progress

A deadlocked process still exists.

A worker blocked forever on one resource still exists.

A server with an exhausted connection pool still accepts some signals from the operating system.

A loop can spin at 100% CPU while doing no useful work.

Liveness at the OS level is intentionally primitive.

It tells us the process has not exited.

That is not enough for a service.

## Readiness is about useful work

A service may need time to load configuration, warm caches, connect to dependencies, or become leader before handling traffic.

Readiness checks answer:

should new work be sent here?

That is different from:

should this process be restarted?

Conflating the two can cause restart loops during dependency outages.

A good system separates "alive" from "able to serve."

## Progress is a third property

Even readiness can miss stalled work.

A queue worker may accept jobs but never complete them.

A replication process may be connected while lag grows without bound.

A call service may accept SIP requests while media sessions never establish.

Progress metrics ask whether the system is advancing.

Completed jobs.

Replication offset.

Processed events.

Successful transactions.

Fresh timestamps.

A system can be alive, ready, and still not progress.

## Health is multidimensional

The word healthy often compresses:

availability,

correctness,

latency,

capacity,

freshness,

dependency state,

and recoverability.

No single check proves all of them.

The monitoring design should match the service's failure modes.

For a database replica, lag may matter.

For a real-time audio path, packet loss and jitter matter.

For an environmental pipeline, data freshness may matter more than process uptime.

Health follows purpose.

## Restarting can hide the real problem

Operations culture sometimes treats restart as repair.

It works surprisingly often because restart resets state.

Memory leaks disappear.

Locks release.

Connections reopen.

Caches clear.

But if the mechanism remains, the failure returns.

A self-healing system that repeatedly restarts without exposing recurrence can make the dashboard look stable while accumulating risk.

Recovery should generate evidence.

How often?

After which condition?

What state grew before the restart?

## Healthy for whom?

A service can work for internal users and fail externally.

One tenant can be healthy while another is broken.

One region can succeed while another times out.

Health always has a population and perspective.

A probe from inside the cluster does not establish internet reachability.

A probe using one account does not establish every authorization path.

The observer belongs in the statement.

## Use narrow words

Instead of saying:

service healthy,

say:

process running,

readiness passing,

synthetic login passing,

p99 latency within SLO,

replication lag under threshold.

The narrower statements sound less elegant.

They are far more actionable.

Running is not healthy.

It is one small piece of evidence that the service has not stopped existing as a process.

Useful life begins above that layer.
