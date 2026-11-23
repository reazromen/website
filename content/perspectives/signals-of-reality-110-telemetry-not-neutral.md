---
title: Telemetry Is Not Neutral
url: /posts/signals-of-reality-110-telemetry-not-neutral.html
date: '2026-05-24'
read_time: 7
excerpt: Instrumentation changes what a system records, costs resources, encodes priorities, and can influence behavior. Telemetry is a designed measurement system, not a transparent mirror.
topic: observability
tags:
- telemetry
- measurement
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

Add tracing to a service.

Latency changes slightly.

Add debug logging.

Disk and network load increase.

Add high-cardinality metrics.

Storage cost explodes.

Instrumentation observes the system by becoming part of the system.

Telemetry is not neutral.

## Measurement has cost

Every counter increment executes code.

Every span allocates data.

Every log line formats fields.

Every exporter uses CPU, memory, buffers, network, and storage.

Usually the overhead is small and worth paying.

At high scale or under failure, it can matter.

A telemetry pipeline can even amplify an incident if error storms generate enormous logs exactly when the system is most constrained.

Observation needs capacity planning.

## Instrumentation changes timing

In concurrent and real-time systems, timing matters.

Verbose logging can alter thread scheduling.

Tracing can add network calls or buffering.

Debug builds can change compiler optimization.

The classic observer effect in software is often mundane: measurement overhead perturbs the race condition we were trying to see.

This does not make debugging impossible.

It means measurements need an overhead model.

## What we instrument reflects what we value

A company may instrument request latency meticulously and user frustration poorly.

A device may report battery voltage but not temperature.

A call platform may expose SIP registration while ignoring RTP quality.

Telemetry architecture encodes priorities.

The absence of a metric is therefore not neutral either.

It can reflect historical attention.

What gets measured becomes easier to manage.

What remains unmeasured becomes easier to forget.

## Naming shapes interpretation

Call a metric `failed_calls` and people assume it represents failed calls.

But perhaps it counts only SIP final responses above 399.

Calls with 200 OK and no media may be excluded.

The name can overstate the measurement.

Telemetry schemas are semantic interfaces.

Definitions need precision.

## Sampling creates a point of view

Keep 1% of traces.

Keep all errors.

Drop health-check traffic.

Aggregate logs after one day.

These are rational choices.

They also create a dataset whose visible world differs from raw production.

If sampling policy changes, trend comparisons may change even when the application does not.

Telemetry configuration belongs in change history.

## Collection can influence behavior

Once teams are judged by a metric, behavior can adapt to the metric.

An SLO can improve reliability.

It can also encourage work that improves the measured indicator while leaving unmeasured user pain unchanged.

This is a form of Goodhart's law: when a measure becomes a target, its relationship to the underlying goal can weaken.

The response is not to abandon metrics.

It is to preserve several independent views and revisit definitions.

## Telemetry contains sensitive structure

Instrumentation can collect identifiers, payload fragments, URLs, locations, or account metadata.

More observability is not automatically better.

Data minimization, redaction, retention, and access controls belong in telemetry design.

An operator's desire for diagnostic detail must be balanced against privacy and risk.

## Observe the observer

A robust observability stack monitors itself.

Dropped logs.

Exporter queue size.

Scrape failures.

Trace sampling rates.

Ingestion delay.

Backend saturation.

Cardinality growth.

If the measurement system becomes unhealthy, its outputs should lose confidence visibly.

Telemetry is not neutral because it is another engineered subsystem with its own incentives, resource use, failure modes, and blind spots.

The goal is not a transparent mirror.

The goal is a characterized instrument.
