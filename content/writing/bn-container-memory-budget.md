---
title: Container Count Is Not a Memory Budget
date: '2025-04-13'
draft: false
language: en
url: /posts/bn-container-memory-budget.html
topic: production-engineering
tags:
- containers
- memory
featured: false
read_time: 2
excerpt: >-
  Counting containers does not tell you how much pressure a server is under. One container
  may do very little while another holds data, caches, and many threads. Two servers with
  the same container count can have very different resource needs.
editorial_batch: 20261003-100-niches
---

Counting containers does not tell you how much pressure a server is under. One container may do very little while another holds data, caches, and many threads. Two servers with the same container count can have very different resource needs. The workload has to come first.

Looking only at normal operation also hides peak behavior. Restarts, large queries, or backups may temporarily require much more memory. Several heavy jobs starting at the same time can push the host beyond its total limit even when each service looks safe in isolation.

A useful budget includes regular usage, expected bursts, and headroom for the operating system itself. Before enforcing limits, it is also important to know what happens when a limit is reached. One process should not drag every unrelated workload down with it.

Containers provide isolation, but they do not create resources. The physical capacity of the server is still shared. Once that sharing model is understood, the decision to add another service can be based on workload rather than container count.

Source: [official reference](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html).
