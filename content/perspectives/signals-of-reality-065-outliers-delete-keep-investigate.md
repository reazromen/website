---
title: "Outliers: Delete, Keep, or Investigate?"
url: /posts/signals-of-reality-065-outliers-delete-keep-investigate.html
date: '2026-05-23'
read_time: 7
excerpt: An outlier is a point that differs from the rest under some model. It can be an error, a rare valid event, a new regime, or evidence that the model is wrong.
topic: philosophy-science
tags:
- data-quality
- evidence
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · How Do We Know?'
editorial_batch: signals-of-reality-200
---

One point ruins the graph.

The temptation is immediate: remove it.

Sometimes removal is exactly right. A sensor disconnected, a decimal point shifted, a timestamp duplicated, or a parser turned missing data into an impossible value.

But an outlier can also be the most informative point in the dataset.

The word outlier describes a relationship to the rest of the observations. It does not tell us why the point is unusual.

That cause has to be investigated.

## Outlier according to which model?

A value can look extreme under one distribution and ordinary under another.

Suppose most measurements cluster tightly around a mean, with a few larger values. If the process truly has heavy tails, those values may be expected. If the process is supposed to be tightly controlled, the same values may indicate a fault.

The classification depends on a model of normal behavior.

That model should be explicit.

A rule such as delete anything more than three standard deviations from the mean sounds objective, but it assumes the mean and standard deviation meaningfully describe the process and that the extreme values did not distort those estimates.

Mechanical rules can hide assumptions as easily as human judgment.

## Ask whether the observation is physically possible

A useful first check is not statistical.

Is the value possible under the measurement system?

A reading outside the sensor's encoded range, a timestamp before the device was manufactured, or a negative count where only nonnegative counts exist points strongly toward data corruption or transformation error.

Physical and logical constraints can justify exclusion more strongly than visual inconvenience.

Even then, preserve the original record and document the reason.

Deletion should leave a trail.

## Compare independent evidence

Suppose one temperature sensor reports a sudden jump.

Did a nearby reference sensor move?

Did power consumption change?

Did the enclosure door open?

Did the raw ADC value jump, or only the converted engineering unit?

Did other channels on the same device change at the same moment?

Independent signals help separate a real event from an instrument artifact.

A single unusual point is ambiguous.

A coordinated change across independent measurements is harder to dismiss.

## Rare valid events matter

Many systems are defined by their tails.

A flood peak.

A latency spike.

A component failure.

An extreme weather event.

An average-focused analysis can treat these as annoying exceptions precisely when they are the events the system must survive.

Deleting rare valid observations can make a model look better while making the model less useful.

This is especially dangerous in reliability and environmental analysis, where extremes often dominate consequences.

## Outliers can mark a new regime

Sometimes a point is not an isolated error.

It is the first member of a new distribution.

A sensor begins drifting after damage.

A service changes behavior after deployment.

A physical system crosses a threshold.

An environmental variable enters conditions not represented in the historical baseline.

If we automatically compare every future point with the old regime, the system may produce a long sequence of outliers while the true problem is that normal has changed.

Anomaly detection and change-point detection answer different questions.

## Robust methods reduce the pressure to delete

Statistical methods can often be designed so a few extreme observations do not dominate the estimate.

Medians, trimmed estimators, robust regression, and explicit heavy-tailed models are examples.

The point is not that one method is universally best.

It is that we should not have to erase data merely to protect a fragile summary statistic.

A model should match the process.

## The most important question is causal

Before deleting an outlier, try to explain its path into the dataset.

Instrument failure?

Transmission error?

Real physical extreme?

Different population?

Protocol retry?

Human entry error?

Unit conversion?

New operating regime?

The cause determines what should happen next.

If it is corrupted, exclude it from the analysis and fix the pipeline.

If it is rare but real, keep it and perhaps change the model.

If the cause is unknown, preserve it and state the uncertainty.

Outlier is not a verdict.

It is an invitation to ask why this observation disagrees with our expectation.

Sometimes the answer improves the dataset.

Sometimes it improves the model.

Sometimes it reveals the phenomenon we were trying to find.
