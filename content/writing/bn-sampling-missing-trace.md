---
title: What Do We Lose When We Do Not Keep Every Trace?
date: '2025-01-09'
draft: false
language: en
url: /posts/bn-sampling-missing-trace.html
topic: observability-monitoring
tags:
- tracing
- capacity
featured: false
read_time: 2
excerpt: >-
  Keeping a complete trace for every request can be expensive. Sampling controls that
  cost, but it also defines what an investigation can and cannot see. A missing trace is
  not evidence that the event never happened.
editorial_batch: 20261003-100-niches
---

Keeping a complete trace for every request can be expensive. Sampling controls that cost, but it also defines what an investigation can and cannot see. A missing trace is not evidence that the event never happened.

A rare failure may not appear in a simple random sample. On the other hand, keeping only failures can make normal behavior harder to compare against. The questions you expect to ask should influence the sampling policy.

Query results should therefore be interpreted alongside collection rules. Check whether the visible count represents the actual total or only a sample of it. Metrics, logs, and traces can fill different gaps for one another.

I think of sampling as a controlled policy for forgetting. It is better to make that policy explicit than to pretend the system has complete memory. Once the limits of the evidence are known, the claims made from it can be more precise.

Source: [official reference](https://opentelemetry.io/docs/concepts/sampling/).
