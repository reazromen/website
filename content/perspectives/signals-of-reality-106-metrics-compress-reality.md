---
title: Metrics Compress Reality
url: /posts/signals-of-reality-106-metrics-compress-reality.html
date: '2026-10-06'
read_time: 7
excerpt: Metrics reduce streams of events into numerical summaries. That compression makes systems observable at scale while inevitably discarding context.
topic: observability
tags:
- metrics
- observability
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

A million requests become one number:

error rate = 0.4%.

That number is extraordinarily useful.

It is also a dramatic act of compression.

The individual users disappear.

The order of events disappears.

The exact error bodies disappear.

The paths disappear unless we preserve them as dimensions.

Metrics let us operate systems too large to watch directly by throwing detail away.

The important question is whether we know which detail was sacrificed.

## Counters turn events into totals

A counter can tell us how many requests occurred.

It does not tell us which requests.

A rate computed from the counter adds a time relation.

Now we can see bursts and trends.

But the operation still compresses.

Ten errors in ten seconds can mean one broken user retrying repeatedly or ten independent users failing once.

Same count.

Different incident.

## Histograms preserve distributions imperfectly

Latency averages hide tails, so we often use histograms or quantiles.

That improves the representation.

It does not recreate the raw events.

Histogram bucket boundaries decide which distinctions remain visible.

A 199 ms request and a 101 ms request may land in the same bucket.

Quantiles tell us useful distribution positions while discarding identity and ordering.

Every metric type is a choice about which question deserves cheap answers.

## Labels recover context at a cost

Add labels:

region,

endpoint,

status code,

device type,

version.

Now the metric becomes much more diagnostic.

It also becomes more expensive.

High-cardinality dimensions can explode storage and query cost.

Observability architecture therefore faces a permanent tension:

preserve enough context to explain incidents,

but not so much that the metric system collapses under the detail.

Traces and logs often preserve dimensions that metrics intentionally cannot.

## Aggregation can reverse the story

A global success rate can improve while one region degrades.

An average CPU metric can remain stable while one node saturates.

A fleet-wide packet-loss value can hide one carrier path that is unusable.

Aggregation is mathematically correct and operationally misleading when it crosses a boundary that matters.

The metric is not wrong.

The grouping is wrong for the question.

## Missing data can look like improvement

Suppose a failing service stops exporting error metrics entirely.

The dashboard's total error count may drop.

The system got worse.

The metric got better.

This is why denominator health and telemetry freshness matter.

A rate without knowing whether all expected sources are reporting can be dangerous.

"No errors" and "no measurements" must remain distinguishable.

## Metrics are strongest for known questions

How many?

How fast?

How often?

How full?

These are metric-shaped questions.

Metrics support alerting, trends, capacity planning, and SLOs extremely well.

They are weaker for:

what exactly happened to this one request?

Which service caused this user's delay?

What sequence led to this rare failure?

That is where traces and logs become valuable.

OpenTelemetry treats metrics, traces, and logs as distinct but correlatable signals because their compression properties differ.

## A metric name is a model

`requests_failed_total` sounds objective.

But what counts as failed?

HTTP 5xx only?

Timeouts?

Application errors returned as 200?

Cancelled requests?

Retries?

The metric definition embeds a theory of failure.

A number cannot be interpreted without that definition.

Good observability documents metric semantics as carefully as API semantics.

## Compression is not the enemy

Without compression, large systems are invisible.

Nobody can inspect every packet, request, syscall, database operation, and user event in real time.

Metrics work because they discard detail while preserving selected structure.

The danger begins when the compressed output is treated as complete.

Metrics compress reality.

The craft of observability is deciding which information must survive the compression and keeping other evidence available when the summary stops being enough.
