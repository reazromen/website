---
title: Long Calls Expose Drift That Short Calls Hide
url: /posts/long-calls-expose-drift-that-short-calls-hide.html
date: '2025-07-14'
read_time: 1
excerpt: A 30-second audio test can pass while two clocks slowly walk apart over several
  minutes.
topic: loup-engineering
tags:
- clock-drift
- long-call
- audio
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Audio Pipeline · advanced'
outputs:
- url: /posts/long-calls-expose-drift-that-short-calls-hide.html
  template: cms/templates/posts/posts--long-calls-expose-drift-that-short-calls-hide.tpl
  source: cms/templates/posts/posts--long-calls-expose-drift-that-short-calls-hide.json
---

The important detail in Long Calls Expose Drift That Short Calls Hide was not the component name but the contract around it. An AEC-off AB run stayed stable for about 175.6 seconds while showing roughly 0.05 percent drift per 100 seconds.

That measurement matters because independent sender and receiver clocks rarely run at exactly the same frequency. A small mismatch can gradually fill or drain a jitter buffer even when packet loss is near zero. Long-duration tests turn the vague report of lag into a measurable rate that can guide playout correction.

The acceptance test was written around observable behaviour rather than whether a task, container or peripheral merely reported that it had started. Evidence marker: `drift-005-per-100s`.

Real-time systems need duration in their test plan. Stability is not proven until the slow variables have had time to move. That gives the team a concrete acceptance condition and a rollback point rather than a subjective sense that the build is probably better.

## Project evidence

LOUP engineering marker: `drift-005-per-100s`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
