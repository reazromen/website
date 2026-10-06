---
title: The Three Signals See Different Worlds
url: /posts/signals-of-reality-108-three-signals-different-worlds.html
date: '2026-03-13'
read_time: 7
excerpt: Metrics, logs, and traces are not interchangeable telemetry formats. Each preserves a different projection of system behavior and loses different information.
topic: observability
tags:
- metrics
- logs
- traces
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

Metrics say error rate increased.

Logs say database timeout.

Traces say one downstream dependency consumed 92% of the request time.

Three signals.

Three views.

Observability discussions often group logs, metrics, and traces together as if they were three file formats containing equivalent information.

They are not.

Each compresses reality differently.

## Metrics see populations

Metrics are excellent for aggregation.

How many requests?

How much CPU?

What latency distribution?

How many errors per minute?

They scale because they discard event-level detail.

A time-series system can summarize billions of events into manageable series.

That makes metrics ideal for trends, alerting, and service-level indicators.

Their blind spot is identity.

The graph may show a problem without telling us which exact request experienced it.

## Logs see local events

Logs preserve event detail.

An application can record a specific error, identifier, configuration value, or state transition.

They are rich because developers choose what to remember.

They are also fragmented.

Without correlation IDs, logs from different services become piles of local memories.

A log can explain one component while hiding the distributed path.

## Traces see relationships

Traces preserve request context across service boundaries.

They show who called whom, in what order, and how long each span took.

They are excellent for causal reconstruction of distributed work.

Their blind spots come from sampling and instrumentation coverage.

A trace rarely tells us how common its pattern is without aggregate support.

One slow trace is an anecdote until metrics show prevalence.

## The same incident looks different

Imagine a database connection pool is exhausted.

Metrics:

pool usage hits maximum, latency rises.

Logs:

connection acquisition timeout messages appear.

Traces:

requests show long waits before database spans.

Each signal confirms a different relation.

Together they make the mechanism much harder to misread.

## One signal can remain green

Suppose application metrics report normal request count.

Logs quietly fill with retries.

Traces reveal every successful request now requires three attempts.

The user may not notice yet.

Which signal is correct?

All of them.

The system has entered a degraded regime before the top-level outcome fails.

This is why combining signals is valuable.

They detect different stages of failure.

## Telemetry design should match questions

Use metrics when the question is:

how much?

how often?

how fast across a population?

Use logs when the question is:

what local event occurred?

what value or error was recorded?

Use traces when the question is:

how did this unit of work move through the system?

The boundaries are not absolute, but the mental model prevents trying to force every question into one backend.

## Correlation is the multiplier

If a log contains trace context, a slow span can lead to the exact error.

If a metric contains exemplars, a spike can lead to representative traces.

If all signals share service name, version, region, and environment conventions, investigations become traversable.

The observability system becomes less like three databases and more like one evidence graph.

## Different worlds, one incident

Metrics, logs, and traces do not compete to be the true representation.

They are instruments with different response functions.

A thermometer and camera can both describe a room without either containing the room.

Telemetry works the same way.

The three signals see different worlds because they preserve different dimensions of the same system.

Observability improves when we stop asking which signal is best and start asking which missing dimension is preventing us from explaining the incident.
