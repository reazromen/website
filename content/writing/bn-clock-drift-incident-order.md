---
title: When Clocks Drift, the Order of Events Can Drift Too
date: '2025-11-16'
draft: false
language: en
url: /posts/bn-clock-drift-incident-order.html
topic: observability-monitoring
tags:
- time
- logging
featured: false
read_time: 2
excerpt: >-
  When logs from several servers are compared side by side, timestamps are often used to
  reconstruct the incident. If the clocks differ, however, a later event can appear to
  have happened first. Sorting timestamps is not enough to prove causal order.
editorial_batch: 20261003-100-niches
---

When logs from several servers are compared side by side, timestamps are often used to reconstruct the incident. If the clocks differ, however, a later event can appear to have happened first. Sorting timestamps is not enough to prove causal order.

Suppose a request travels from server A to server B. If B's clock is behind, the response may appear to have been generated before the request arrived. That is not time travel; it is inconsistent measurement. Correlation identifiers are still needed to connect the events.

Monitor time synchronization, but do not assume a synchronized clock is perfect. For events that happen very close together, the uncertainty window matters. Measuring elapsed time inside one process and comparing wall clocks across multiple machines are different problems.

In an incident narrative, I prefer to separate confirmed order from inferred order. Logs contain a great deal of truth, but if we forget the limits of the clocks behind them, that truth can be arranged into the wrong story.

Source: [official reference](https://www.rfc-editor.org/rfc/rfc5905.html).
