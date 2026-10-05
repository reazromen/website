---
title: Do Not Let Log History Block Current Work
date: '2025-06-24'
draft: false
language: en
url: /posts/bn-logs-retention-disk-budget.html
topic: observability-monitoring
tags:
- logging
- storage
featured: false
read_time: 2
excerpt: >-
  Logs are useful for future investigations, but unlimited retention can let the evidence
  system consume the resources required by the service itself. Observability needs its
  own storage budget.
editorial_batch: 20261003-100-niches
---

Logs are useful for future investigations, but unlimited retention can let the evidence system consume the resources required by the service itself. Once storage is exhausted, having a long history is little comfort if the current system cannot operate. Observability needs its own resource budget.

A failing process can write the same message extremely quickly. The longer the incident continues, the more storage pressure it creates. Retention therefore needs more than a number of days; maximum space and write rate matter too.

What you keep should come from operational need. Useful events, compact counters, and context that avoids unnecessary secrets can often explain more than raw volume. More data does not automatically create more understanding.

I think of log retention as choosing what the system remembers. It cannot remember everything forever. The job is to preserve enough history for decisions while protecting the resources needed for current work.

Source: [official reference](https://www.freedesktop.org/software/systemd/man/249/journald.conf.html).
