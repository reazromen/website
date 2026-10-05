---
title: Full RAM and Memory Pressure Are Not the Same Thing
date: '2024-09-07'
draft: false
language: en
url: /posts/bn-linux-ram-pressure-question.html
topic: linux-homelab
tags:
- linux
- memory
featured: false
read_time: 2
excerpt: >-
  On Linux, a high used-memory number does not automatically mean the system is under
  pressure. Cache consumes memory too and can often be reclaimed. A full-looking memory
  graph and work actually stalling for memory are different events.
editorial_batch: 20261003-100-niches
---

On Linux, a high used-memory number does not automatically mean the system is under pressure. Cache consumes memory too and can often be reclaimed. A full-looking memory graph and work actually stalling for memory are different events. The useful question is how the number relates to the user's experience.

Suppose one server uses most of its RAM but completes work on time. Another uses slightly less, yet processes spend time waiting or repeatedly reclaiming memory. Calling the first server unhealthy from percentage alone misses the point. Work latency and memory pressure matter too.

Signals such as PSI help expose the waiting side of the problem. One metric never explains every cause, but it gets closer to the question of how much resource scarcity is actually stopping work. Per-process usage and system-wide pressure are most useful when read together.

When judging server health, I want an accounting of time as well as space. How much RAM exists is an important question. How long work waits because of the state of that RAM is equally important.

Source: [official reference](https://www.kernel.org/doc/html/latest/accounting/psi.html).
