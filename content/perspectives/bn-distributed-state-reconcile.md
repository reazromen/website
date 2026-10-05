---
title: "Reconcile: Returning Again and Again to the Gap Between Intent and Reality"
date: '2026-04-05'
draft: false
language: en
url: /posts/bn-distributed-state-reconcile.html
topic: production-engineering
tags:
- state
- distributed-systems
featured: false
read_time: 2
excerpt: >-
  We can declare a desired state, but real systems rarely arrive there instantly. Failure,
  delay, and change exist along the path. Reconciliation is interesting because it checks
  the relationship repeatedly instead of trusting a one-time command.
editorial_batch: 20261003-100-niches
---

We can declare a desired state, but real systems rarely arrive there instantly. Failure, delay, and change exist along the path. Reconciliation is interesting because it checks the relationship repeatedly instead of trusting a one-time command.

Desired state sits on one side and observed state on the other. When they differ, the controller tries to change reality and then observes again. Success is no longer defined only by sending a command; returning to the resulting state becomes part of the loop.

Observation can itself be stale or wrong, so freshness and operation identity matter. Whether an action can be retried safely also affects how useful reconciliation can be.

I would not claim that this software pattern maps directly onto every process in life or nature. It has a specific engineering meaning. But as a way of accepting the distance between intention and outcome, the concept is valuable to me.

Source: [official reference](https://kubernetes.io/docs/concepts/architecture/controller/).
