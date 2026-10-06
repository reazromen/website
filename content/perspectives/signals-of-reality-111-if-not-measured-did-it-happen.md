---
title: If You Did Not Measure It, Did It Happen?
url: /posts/signals-of-reality-111-if-not-measured-did-it-happen.html
date: '2026-08-17'
read_time: 7
excerpt: Events do not depend on telemetry in order to occur. But without measurements, later reconstruction may be impossible or underdetermined.
topic: observability
tags:
- measurement
- telemetry
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

A service stalled for twelve seconds.

No alert fired.

No trace was sampled.

Logs contain nothing unusual.

The user remembers waiting.

Did the incident happen?

Of course it could have.

Reality does not need permission from our telemetry.

But operations has a second problem after the event: can we know enough about what happened to explain it?

That depends on measurement.

## Absence of telemetry is not absence of event

A monitoring system observes selected outputs.

It can miss:

short transients,

rare users,

unsampled traces,

dropped logs,

dimensions that were never instrumented,

or failures outside the monitored boundary.

"No evidence in telemetry" should therefore be interpreted carefully.

Sometimes it means the event was unlikely.

Sometimes it means the measurement system was blind.

Those are different conclusions.

## Instrumentation creates discoverability

Suppose a request stalls in a queue.

If queue wait time is recorded, the bottleneck can appear directly.

If only total latency is recorded, the stall appears but the location remains unknown.

If neither is recorded, a user's stopwatch may be the only surviving evidence.

Instrumentation determines which distinctions future investigators can recover.

This is why observability is partly an investment in future questions.

## Retention determines memory

An event was measured.

Then retention deleted the data.

A month later, the same pattern returns.

Now the first event exists only in an incident note.

Retention is another epistemic boundary.

High-resolution data often becomes downsampled with age.

Logs expire.

Traces are sampled or deleted.

Storage policy determines how far backward the system can remember with detail.

That policy should match the timescale on which failures recur.

## Users are external sensors

When machine telemetry is absent, user reports can still provide evidence.

Time.

Visible error.

Sequence of actions.

Device.

Network.

Screenshot.

Human reports can be inaccurate or incomplete.

So can machine records.

The right response is not to dismiss human evidence because it lacks a metric.

Correlate it.

A user may observe the highest layer the system failed to instrument.

## Unmeasured variables can dominate

Suppose every available metric looks normal.

The actual cause is radio interference near one device.

If no RF measurement exists, backend telemetry cannot reveal it directly.

Or a room's temperature changed but no environmental sensor was installed.

Or one DNS resolver served stale data but resolver identity was not recorded.

Some incidents remain underdetermined because the causal variable never entered the data.

A larger query cannot recover a missing variable.

## More measurement is not always better

Collecting everything is impossible and often irresponsible.

Cost grows.

Cardinality grows.

Privacy risk grows.

Noise grows.

Operators drown.

The goal is not total observation.

It is strategic observation: preserve the variables most likely to distinguish important states.

Architecture, failure modes, and user journeys should guide instrumentation.

## Unknown should remain a valid conclusion

Sometimes the honest postmortem says:

the user-visible stall is credible,

the available telemetry confirms elevated latency,

but the data cannot distinguish between queue contention and downstream delay.

That is better than inventing certainty.

An observability system should reduce unknowns, not make teams ashamed to admit them.

If you did not measure it, the event could still have happened.

What changes is not reality.

What changes is how much of reality can be reconstructed after the system has moved on.
