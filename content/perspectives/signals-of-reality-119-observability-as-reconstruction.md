---
title: Observability as Reconstruction
url: /posts/signals-of-reality-119-observability-as-reconstruction.html
date: '2026-03-02'
read_time: 8
excerpt: Operators rarely observe the full internal state directly. They reconstruct likely causes from telemetry, topology, timing, change history, and user-visible effects.
topic: observability
tags:
- observability
- evidence
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · The System Behind the Dashboard'
editorial_batch: signals-of-reality-200
---

An incident is over before the investigation begins.

The request timed out.

The queue drained.

The process restarted.

The packet disappeared.

Now the engineer is looking at traces left behind.

Observability is reconstruction.

## Production does not wait for the detective

A live system changes continuously.

By the time an operator opens a dashboard, the state that produced the symptom may no longer exist.

Caches have changed.

Connections closed.

Schedulers moved work.

Autoscaling added instances.

Retries succeeded.

The investigation therefore resembles historical science more than direct inspection.

We infer past state from surviving evidence.

## Telemetry is the fossil record

Metrics preserve aggregate motion.

Logs preserve selected events.

Traces preserve paths.

Packet captures preserve network interactions when available.

Deployment records preserve change.

Configuration repositories preserve intent.

User reports preserve experienced outcome.

No source is complete.

Together they form a partial record of what the system did.

The quality of reconstruction depends on how independent and well-characterized those sources are.

## Time alignment builds narrative

Put all evidence on one timeline.

14:01 deployment.

14:04 cache miss rate rises.

14:05 database latency rises.

14:06 retries increase.

14:07 user errors begin.

14:10 rollback.

14:12 recovery.

Sequence does not prove causation, but it constrains stories.

A proposed cause occurring after the effect becomes less plausible.

A mechanism predicting the observed order becomes stronger.

Time is one of the most useful structures in incident reasoning.

## Counterfactual tests strengthen reconstruction

A postmortem can move beyond storytelling.

Reproduce the configuration in a test environment.

Reapply the change.

Disable the suspected feature.

Replay traffic.

Compare before and after.

If the proposed mechanism predicts new behavior and the experiment matches, the reconstruction gains credibility.

Production history generates hypotheses.

Controlled tests interrogate them.

## Missing evidence should remain visible

Many postmortems become too clean.

The team knows the ending, so every earlier event is rewritten as if it obviously pointed there.

That is hindsight bias.

A better report marks uncertainty.

We know the queue rose.

We infer this was caused by connection contention.

We could not verify one branch because detailed traces were not retained.

This preserves the difference between evidence and interpretation.

## Observability quality determines postmortem quality

If clocks are wrong, ordering becomes uncertain.

If logs omit identifiers, correlation becomes difficult.

If metrics are overaggregated, affected subgroups disappear.

If traces are unsampled during the critical period, causal paths vanish.

Instrumentation is not only for real-time dashboards.

It determines how much future explanation is possible.

## The goal is not a perfect movie

No telemetry system can record every internal state at full resolution forever.

Nor should it.

The practical goal is enough evidence to distinguish the most important competing explanations.

Which component?

Which version?

Which path?

Which user cohort?

Which dependency?

Which failure mode?

Observability should preserve discriminating structure.

## Reconstruction is a scientific habit

Observe traces.

Form hypotheses.

Check consistency.

Seek independent evidence.

Run experiments.

State uncertainty.

Revise the story.

This is the logic of incident investigation at its best.

Observability is not a magic property that lets us see inside a distributed system directly.

It is the infrastructure that lets us reconstruct what probably happened after the moment itself is gone.
