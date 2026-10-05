---
title: A Growing Queue Is Growing Work Debt
date: '2020-08-10'
draft: false
language: en
url: /posts/bn-queue-backpressure-contract.html
topic: redis-systems
tags:
- queues
- capacity
featured: false
read_time: 2
excerpt: >-
  Queues let producers and workers move at different speeds for a while, but a queue that
  keeps growing is accumulating work debt against the future. More waiting space does
  not create more processing capacity.
editorial_batch: 20261003-100-niches
---

Queues let producers and workers move at different speeds for a while, but a queue that keeps growing is accumulating work debt against the future. More waiting space does not create more processing capacity.

Suppose work arrives faster than it can be completed. The problem may look small at first, but eventually waiting time crosses a user-visible limit. That is why queue length and the age of the oldest item are both useful.

Backpressure is how a system communicates its real capacity to producers. Limiting new work, dropping lower-priority work, or adding workers can all be valid responses depending on the workload. There is no single policy for every queue.

I think of a queue as a way to borrow time. Without a plan to repay that time debt, the queue merely delays the visible failure. Capacity becomes a real operational concept once acceptable waiting time is defined.

Source: [official reference](https://redis.io/docs/latest/develop/data-types/streams/).
