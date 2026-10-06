---
title: Traces Tell Stories Across Services
url: /posts/signals-of-reality-107-traces-stories-across-services.html
date: '2026-05-03'
read_time: 7
excerpt: Distributed traces reconstruct one request as it crosses service boundaries, preserving causal context that aggregate metrics and isolated logs often lose.
topic: observability
tags:
- traces
- distributed-systems
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

A user presses a button.

The frontend calls an API.

The API calls authentication, a database, a queue, and another service.

One request becomes a small distributed story.

Without shared context, each service remembers only its own paragraph.

A distributed trace tries to reconnect them.

## Trace context creates continuity

OpenTelemetry traces consist of spans representing units of work, connected by identifiers and parent-child relationships.

A trace can show:

request entered gateway,

authentication took 40 ms,

database query took 12 ms,

downstream service waited 800 ms,

retry occurred,

response returned.

The value is not merely timing.

It is relational timing.

We can see where one operation depends on another.

## A trace is not the whole system

One trace follows one sampled path.

It does not automatically tell us fleet-wide frequency.

It may not include unsampled requests.

Instrumentation can miss asynchronous work.

Context propagation can break.

A trace is detailed evidence about an execution, not a complete population summary.

This is why traces and metrics complement each other.

Metrics tell us how widespread.

Traces tell us what one path looked like.

## Causality is suggested, not guaranteed

Parent-child span structure reflects instrumentation and execution relationships.

If span B is called from span A, that is useful causal evidence.

But traces can still be misleading.

An asynchronous queue may separate cause and execution.

Background work can share resources without appearing as a direct child.

Clock errors can distort timing.

Missing spans can create apparent gaps.

Trace structure is a model of causality built from propagated context.

It should be interpreted with system architecture.

## Tail latency becomes visible

A metric says p99 latency increased.

A trace can show why one slow request spent most of its life waiting.

DNS.

Connection establishment.

Queueing.

Database lock.

External API.

Retry.

Serialization.

The trace turns "slow" into a path.

That makes it one of the most useful tools for distributed performance work.

## Sampling is an epistemic decision

Tracing every request can be expensive.

So systems sample.

Maybe one percent of normal traffic.

Maybe every error.

Maybe tail-based sampling keeps slow traces.

Sampling changes which stories survive.

If rare failures are not preferentially kept, the exact events we need can disappear.

If only errors are kept, we lose comparison with normal paths.

Sampling policy is part of observability semantics.

## Correlation gives traces more power

A trace ID inside a structured log lets us jump from path to local detail.

A metric exemplar can connect an aggregate spike to a representative trace.

A deployment version attached to spans can reveal a regression.

The signals become more valuable when they share context.

OpenTelemetry's common semantic conventions aim at this kind of interoperability.

## Traces can expose architecture we forgot

Documentation drifts.

Services are added.

Dependencies change.

A distributed trace can reveal the runtime dependency graph actually exercised by requests.

That graph is not the whole architecture, but it is evidence about architecture in motion.

Unexpected calls often reveal hidden coupling.

## Stories are reconstructions

The metaphor of a trace as a story is useful because stories have sequence and actors.

It is dangerous if we forget that instrumentation edits the story.

Uninstrumented work disappears.

Sampling chooses which stories are saved.

Span naming shapes interpretation.

Still, traces solve a problem that neither metrics nor isolated logs solve well:

they preserve enough context to follow one piece of work through a distributed system.

The system remains larger than the trace.

But for one request, the trace gives the closest thing operations has to a travel diary.
