---
title: Multiple Paths Do Not Create Free Reliability
date: '2020-02-14'
draft: false
language: en
url: /posts/bn-biology-redundancy-cost.html
topic: biology-systems
tags:
- biology
- reliability
featured: false
read_time: 2
excerpt: >-
  Alternate paths can keep a system working after one path fails, but redundancy has a
  cost. Space, energy, and control requirements grow with it. Reliability is therefore
  also a resource question.
editorial_batch: 20261003-100-niches
---

Alternate paths can keep a system working after one path fails, but redundancy has a cost. Space, energy, and control requirements grow with it. Reliability is therefore also a resource question.

Biology contains many examples of overlapping or related functions, but it is risky to call every overlap an intentional backup. The evolutionary history of a trait and its current usefulness are different questions. Seeing a benefit today does not prove the trait was created for that benefit.

Engineering has a similar trap. Two servers do not provide full resilience if both depend on the same power source or the same broken configuration. What matters is not simply the number of components, but how independent their failure modes are.

The useful question for me is small: does the second path actually survive the failure that removes the first? Whether the system is living or engineered, counting more parts is not enough without a map of their dependencies.

Source: [official reference](https://openstax.org/books/biology-2e/pages/9-introduction).
