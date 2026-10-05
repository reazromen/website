---
title: A Jitter Buffer Should Absorb Arrival Variation, Not Become a Delay Bucket
url: /posts/a-jitter-buffer-should-absorb-arrival-variation-not-become-a-delay-bucket.html
date: '2023-09-03'
read_time: 1
excerpt: More buffering reduces underruns until it starts creating latency and hiding
  drift.
topic: loup-engineering
tags:
- rtp
- jitter-buffer
- latency
draft: false
featured: false
language: en
eyebrow: 'LOUP Engineering: Audio Pipeline · advanced'
outputs:
- url: /posts/a-jitter-buffer-should-absorb-arrival-variation-not-become-a-delay-bucket.html
  template: cms/templates/posts/posts--a-jitter-buffer-should-absorb-arrival-variation-not-become-a-delay-bucket.tpl
  source: cms/templates/posts/posts--a-jitter-buffer-should-absorb-arrival-variation-not-become-a-delay-bucket.json
---

The useful question in A Jitter Buffer Should Absorb Arrival Variation, Not Become a Delay Bucket was where the behaviour actually originated. LOUP testing pointed toward a larger jitter buffer, around four to six frames, after short network gaps continued to reach playout.

The goal was not to maximize queue depth. It was to create enough headroom for the observed burst pattern while keeping conversational delay controlled. Buffer depth, underrun count and rebuffer events have to be logged together; listening alone cannot distinguish a healthy buffer from one that is slowly accumulating latency.

I treated the known-good configuration as a control sample, changed only the layer under investigation, and recorded the regression or improvement before the next experiment. Evidence marker: `jitter-4-6-frames`.

Buffering is a control problem. The right size comes from measured arrival behavior and an explicit latency budget. Keeping the rule explicit means the same decision can be checked again on the next board revision or firmware branch.

## Project evidence

LOUP engineering marker: `jitter-4-6-frames`. This note records the design or debugging lesson without publishing device credentials, private keys, customer data or manufacturing secrets.
