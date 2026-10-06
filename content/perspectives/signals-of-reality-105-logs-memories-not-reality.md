---
title: Logs Are Memories, Not Reality
url: /posts/signals-of-reality-105-logs-memories-not-reality.html
date: '2026-08-11'
read_time: 7
excerpt: Logs are records emitted by software about events it chose to remember. They can be missing, delayed, duplicated, misleading, or produced after interpretation.
topic: observability
tags:
- logs
- observability
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

The log says the request succeeded.

The database has no row.

Which one is reality?

Neither log line nor database row is reality in the philosophical sense.

They are different traces left by a process.

Logs are memories written by software.

Like memories, they are selective.

## Software decides what to remember

A program contains thousands of state transitions.

Only some become logs.

Developers choose:

which events,

which severity,

which fields,

which wording,

which IDs,

which errors.

OpenTelemetry describes a log as a timestamped record of an event, potentially structured and enriched with metadata.

The word *record* matters.

A log is produced by an observer inside the system.

It is not the event itself.

## The log can occur before the outcome

Consider:

1. application writes "saving order",
2. process crashes,
3. transaction rolls back.

If the wording later reads like confirmation—"order saved"—an operator may infer a state that never committed.

Logging location matters.

Before action.

After action.

After durable commit.

After acknowledgement from a dependency.

One line moved by a few instructions can change its evidential meaning.

## Logs can be lost

An application emits a log.

The process exits before buffers flush.

The collector is overloaded.

The network drops the batch.

The backend rejects it.

Retention removes it.

Now the event happened without a searchable log.

Absence of log is not automatically absence of event.

Telemetry pipelines need their own observability.

Dropped-log counters and ingestion freshness matter.

## Logs can be duplicated

Retries can resend batches.

Collectors can replay.

Applications can log the same event at several layers.

A search result showing three error lines may represent one failure.

Counting log lines as incidents without deduplication can exaggerate reality.

Identifiers and event semantics help distinguish repetition from duplication.

## Timestamps can lie accidentally

Distributed hosts have different clocks.

Buffers delay delivery.

Backends ingest out of order.

A line displayed at 10:00:02 may describe an event that occurred before another line shown at 10:00:01 from a different machine.

Ordering by displayed timestamp can create a false causal narrative.

Trace context and clock discipline improve reconstruction, but exact global ordering remains hard.

## Human-readable text hides structure

"Database error" is nearly useless.

Which database?

Which query?

Which host?

Which request?

Which retry?

Structured logs preserve fields that can be correlated with traces and metrics.

The goal is not more words.

It is more recoverable relationships.

## Logs are strongest when corroborated

A log says a request was sent.

A trace shows the span.

The downstream service has a corresponding record.

A metric shows traffic at the same time.

Packet capture confirms bytes crossed the interface.

Multiple independent signals create stronger evidence.

OpenTelemetry's effort to correlate logs with trace and span context reflects this principle.

## Keep the memory, question the memory

Logs are indispensable because they let systems leave narratives about their internal decisions.

But narratives are authored.

They can be incomplete, stale, mislabeled, or missing.

When an incident is difficult, ask of every log line:

Who emitted this?

At what point in the operation?

Was the log itself delivered reliably?

What state does it prove?

What state does it merely suggest?

Logs are memories, not reality.

Good observability treats them as evidence to reconstruct the event, not as scripture.
