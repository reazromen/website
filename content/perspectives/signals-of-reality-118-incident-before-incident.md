---
title: The Incident Before the Incident
url: /posts/signals-of-reality-118-incident-before-incident.html
date: '2026-06-16'
read_time: 7
excerpt: "Major failures often have weak precursors: rising retries, queue growth, clock drift, error diversity, or recovery frequency before user-visible collapse."
topic: observability
tags:
- incident
- early-warning
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

At 14:32 the service went down.

That is when the incident became undeniable.

The system may have started failing at 13:50.

Retries increased.

A queue grew slowly.

Cache hit rate changed.

One replica began lagging.

The service recovered from small faults more often.

Nothing crossed the alert threshold.

The incident existed before the incident page opened.

## Collapse is often the end of a process

Some failures are sudden.

A cable is cut.

A process crashes.

A power supply dies.

Others accumulate.

Memory leaks.

Backlogs.

Thermal stress.

Fragmentation.

Replication delay.

Certificate expiration approaching.

A system can spend a long time losing resilience before it loses availability.

The final outage is one transition in a longer trajectory.

## Recovery can hide deterioration

Suppose a service restarts automatically when memory is exhausted.

Users barely notice.

The dashboard returns green.

Restarts become more frequent over weeks.

The automation is working.

The underlying system is worsening.

Self-healing can convert visible incidents into hidden precursors.

This is why recovery frequency should itself be measured.

A system that needs more healing is giving a signal.

## Retry rates are often early warnings

A dependency becomes slightly unreliable.

Clients retry.

User success remains high.

Traffic increases because each logical operation now requires more attempts.

The extra load worsens the dependency.

Eventually retries contribute to collapse.

Top-level success can remain flat while internal effort rises sharply.

Work per successful outcome is a valuable health measure.

## Variance can rise before the mean

Average latency looks normal.

Tail latency widens.

Queue time becomes less stable.

Error types diversify.

Some nodes behave differently from others.

The system is becoming heterogeneous.

Averages often hide this early stage.

Variance, quantiles, and per-instance views can reveal loss of stability before headline metrics move.

## Incidents have a prehistory in change

Deployments.

Configuration edits.

Traffic growth.

Data migration.

Certificate rotation.

Dependency upgrade.

Hardware replacement.

Overlaying change events on telemetry gives incidents context.

A failure at 14:32 may have been enabled by a deployment at 10:00 and triggered by traffic four hours later.

The nearest event in time is not always the cause.

## Early warnings need action rules

A precursor is useless if nobody knows what to do.

If replication lag grows beyond a trend threshold:

reduce load?

block deployment?

investigate storage?

fail over?

Early-warning systems need response playbooks or they become anxiety generators.

The signal should connect to an action.

## Not every whisper predicts a scream

A retry spike may recover harmlessly.

A queue may drain.

A temperature excursion may remain within tolerance.

Precursors produce false positives if treated as deterministic prophecy.

The goal is not to alert on every wobble.

It is to identify patterns that increase risk and deserve attention.

## Postmortems should move the start time backward

After an incident, ask:

what was the earliest observable deviation?

Which signals changed before user impact?

Which automatic recovery masked symptoms?

Which trend could have been acted on?

This changes monitoring from outage detection to degradation detection.

The incident before the incident is often where the most valuable engineering work lives.

By the time the dashboard is red, the system has already told its story loudly.

The harder craft is learning to hear the earlier, quieter sentence.
