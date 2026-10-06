---
title: Unknown Unknowns and Observability
url: /posts/signals-of-reality-109-unknown-unknowns-observability.html
date: '2026-07-10'
read_time: 7
excerpt: Monitoring asks predefined questions. Observability aims to let operators ask new questions after unfamiliar failures appear.
topic: observability
tags:
- observability
- unknown
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

An alert answers a question you thought to ask yesterday.

An incident often asks a question nobody anticipated.

That gap is where observability becomes more than monitoring.

OpenTelemetry's observability primer describes observability in terms of understanding a system from its outputs and handling novel problems—often called unknown unknowns.

The phrase is fashionable.

The engineering problem behind it is real.

## Monitoring encodes expectations

CPU > 90%.

Error rate > 2%.

Queue depth > 10,000.

These alerts are powerful because expected failure modes have been translated into rules.

The system knows what to watch.

This is not inferior to observability.

Known failures deserve direct monitoring.

The problem is that a novel failure may not cross any existing threshold.

## Unknown failures appear as disagreement

A user complains while dashboards are green.

One region slows but global averages remain normal.

A particular device revision resets only after roaming between networks.

No alert was designed for these stories.

The first evidence is often contradiction.

Something in the model and something in experience do not agree.

Observability should let us slice, correlate, and trace until the missing dimension becomes visible.

## Rich context creates future questions

Telemetry cannot answer a question about a dimension it never recorded.

If logs omit firmware version, later analysis cannot group by firmware.

If metrics aggregate all regions together, the original regional distinction may be gone.

If traces never propagate device identity, cross-service debugging loses that connection.

Unknown-unknown readiness therefore depends on retaining useful context before knowing exactly how it will be used.

This is expensive.

Cardinality and storage are real constraints.

The art is choosing dimensions that map to architecture, users, releases, and likely failure domains.

## High cardinality can be diagnostic gold

Traditional metrics systems struggle with labels such as user ID or request ID because they create enormous numbers of series.

Traces and event-oriented stores can preserve higher-cardinality context more naturally.

That does not mean collect everything.

It means match representation to question.

A single unique identifier may be useless for aggregate alerting and essential for reconstructing one failed workflow.

The information has value at a different layer.

## Unknown unknowns become known after the incident

Once a novel failure is understood, it should not remain novel forever.

Add a metric.

Add a regression test.

Add a health check.

Add a runbook.

Add a synthetic probe.

The observability system learns.

This is how incidents improve future detection.

An unknown unknown becomes a known known failure mode with an explicit signal.

## Telemetry cannot create missing reality

Observability has limits.

If no instrument recorded the event, later tools cannot reconstruct every detail.

If logs were dropped, traces unsampled, and metrics aggregated away the relevant dimension, the incident may remain partly unknowable.

No query language can recover information destroyed upstream.

This is why capture and retention architecture matter.

## Ask whether the system can surprise you legibly

A mature observability design is not one with the most dashboards.

It is one where unfamiliar failures leave enough evidence to form new questions.

Can we connect user impact to service versions?

Can we move from an aggregate anomaly to specific examples?

Can we reconstruct a request path?

Can we distinguish no data from zero?

Can we see deployment, topology, and dependency changes on the same timeline?

These capabilities create investigative freedom.

Unknown unknowns will always exist.

The goal is not to predict every failure.

It is to make surprise leave fingerprints.
