---
title: What We Measure Is Not the Whole System
date: '2022-12-31'
draft: false
language: en
url: /posts/bn-observation-is-model.html
topic: observability-monitoring
tags:
- measurement
- systems-thinking
featured: false
read_time: 2
excerpt: >-
  A dashboard can create the feeling that we are looking at the entire system. In reality,
  we are looking at selected measurements. What we measure, where we measure it, and how
  often already forms a model.
editorial_batch: 20261003-100-niches
---

A dashboard can create the feeling that we are looking at the entire system. In reality, we are looking at selected measurements. What we measure, where we measure it, and how often already forms a model. The model and the system are not identical.

Suppose SIP request success is measured but audio quality is not. One layer of the phone system is visible while another remains hidden. A clean signaling graph cannot guarantee the health of the invisible media layer.

Before adding another metric, it helps to write down the unknown question it is supposed to answer. Not every unknown can be eliminated. Some limits have to be understood through tests, context, or reports from people using the system.

For me, the strength of observability is not a claim to omniscience. It becomes more honest when it can explain what is visible and where it remains blind. Knowing the boundary does not mean seeing less; it means understanding what the visible evidence actually says.

Source: [official reference](https://prometheus.io/docs/concepts/data_model/).
