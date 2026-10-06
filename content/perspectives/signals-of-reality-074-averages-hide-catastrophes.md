---
title: Averages Can Hide Catastrophes
url: /posts/signals-of-reality-074-averages-hide-catastrophes.html
date: '2026-06-07'
read_time: 7
excerpt: An average can describe a center while erasing tails, subgroups, timing, and rare events. Systems often fail in exactly the structure the mean discards.
topic: systems-thinking
tags:
- metrics
- uncertainty
draft: true
featured: false
language: en
eyebrow: 'Signals of Reality · How Do We Know?'
editorial_batch: signals-of-reality-200
---

A service has an average latency of 120 milliseconds.

That sounds healthy.

But what if almost every request is fast while a small fraction takes many seconds?

The average can remain respectable while some experiences are terrible.

This is not an argument against averages.

It is an argument against asking a one-number summary to describe a many-shaped system.

## The mean erases distribution

The arithmetic mean answers a precise question: what value would every observation have if the total were distributed evenly?

That can be useful.

But many systems are not evenly distributed.

Latency is often skewed.

Rainfall can arrive in bursts.

Failure durations can have heavy tails.

Averages can sit in regions where few actual observations occur.

The center is not the shape.

## Rare events can dominate consequence

Suppose a component has one severe failure in a very large number of otherwise successful operations.

The average state is excellent.

If that one event stops the whole system, the tail matters more than the center.

Reliability engineering therefore cares about quantiles, extreme-value behavior, failure modes, and conditional risk.

Environmental systems have the same issue.

Average river level may tell us little about flood risk.

Average wind may tell us little about structural design loads.

Average temperature can hide short extremes that matter to infrastructure.

Consequence is often nonlinear.

## Aggregation can erase subgroups

Imagine two device revisions with very different failure rates.

Combine their data and the fleet average looks moderate.

Split by hardware revision and the problem becomes obvious.

Aggregation can hide heterogeneity.

The remedy is not to subdivide data endlessly until a desired pattern appears.

It is to use domain knowledge to ask which groups correspond to plausible mechanisms.

Hardware revision, geography, software version, environment, and workload can all create meaningful strata.

The average should not erase the architecture.

## Time averages can hide sequencing

Two systems can have the same average utilization and completely different operational behavior.

One runs at 50% continuously.

Another alternates between 0% and 100%.

Same mean.

Different queues, thermal behavior, latency, and failure risk.

Time order matters.

Averages discard it.

That is why time-series plots, histograms, quantiles, and event timelines are often necessary companions to summary metrics.

## Median is not a universal rescue

The median is robust to extremes and often better for skewed distributions.

But it can hide tails even more aggressively.

A median latency of 20 milliseconds says nothing about the slowest fraction.

A median temperature says nothing about an extreme heat event.

No single statistic can preserve every property.

The right summary depends on the decision.

## Dashboards encourage one-number thinking

Operational interfaces have limited space.

Teams want a few KPIs.

That pressure makes aggregation inevitable.

The danger is when the number becomes the system.

A good dashboard lets users drill from aggregate to distribution, subgroup, and raw timeline.

It treats the summary as an index into evidence, not a replacement for evidence.

## Ask what the average cannot show

Whenever an average drives a decision, ask what the tails look like, whether there are distinct subgroups, how the variable changes over time, whether missing values cluster in extreme conditions, and whether a rare event dominates operational risk.

Those questions reveal whether the mean is summarizing or concealing.

Averages are maps.

Like every map, they leave things out.

For bursty, heterogeneous, thresholded, or high-consequence systems, the omissions can contain the entire story.

If the tail matters, measure the tail.
